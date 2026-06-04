//
// Created by 6anna on 29.05.2026.
//

#include "SimplecSolver.h"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <stdexcept>

namespace cfd3b {

    SimplecSolver::SimplecSolver(const VelocityBoundaryConditionSet& velocityBcs_,
                                 const PressureBoundaryConditionSet& pressureBcs_,
                                 const SimplecSettings& settings_)
        : velocityBcs(&velocityBcs_),
          pressureBcs(&pressureBcs_),
          settings(settings_),
          momentumAssembler(velocityBcs_, pressureBcs_),
          pressureCorrectionAssembler(pressureBcs_) {
    }

    const SimplecIterationState& SimplecSolver::state() const {
        return iterationState;
    }

    std::vector<double> SimplecSolver::extractDiagonal(const cfd::FvMatrix& M) const {
        std::vector<double> diag(M.size(), 0.0);

        for (std::size_t i = 0; i < M.size(); ++i) {
            diag[i] = M.coeff(i, i);
        }

        return diag;
    }

    double SimplecSolver::computeMaxDifference(const cfd::ScalarField& field,
                                               const std::vector<double>& values) const {
        double maxDiff = 0.0;

        for (std::size_t i = 0; i < values.size(); ++i) {
            maxDiff = std::max(maxDiff, std::abs(values[i] - field[i]));
        }

        return maxDiff;
    }

    double SimplecSolver::computeMaxDifferenceComponent(const cfd::VectorField& field,
                                                        const std::vector<double>& values,
                                                        VelocityComponent component) const {
        double maxDiff = 0.0;
        const int c = (component == VelocityComponent::X) ? 0 : 1;

        for (std::size_t i = 0; i < values.size(); ++i) {
            maxDiff = std::max(maxDiff, std::abs(values[i] - field[i][c]));
        }

        return maxDiff;
    }

    double SimplecSolver::computeContinuityResidual(const cfd::FvMatrix& pressureMatrix) const {
        double maxAbsRhs = 0.0;

        for (std::size_t i = 0; i < pressureMatrix.size(); ++i) {
            maxAbsRhs = std::max(maxAbsRhs, std::abs(pressureMatrix.rhs(i)));
        }

        return maxAbsRhs;
    }

    void SimplecSolver::writeComponentToField(cfd::VectorField& field,
                                              const std::vector<double>& values,
                                              VelocityComponent component,
                                              double relaxation) {
        const int c = (component == VelocityComponent::X) ? 0 : 1;

        for (std::size_t i = 0; i < values.size(); ++i) {
            const double oldValue = field[i][c];
            field[i][c] = (1.0 - relaxation) * oldValue + relaxation * values[i];
        }
    }

    void SimplecSolver::correctPressure(NavierStokesProblem& problem,
                                        const std::vector<double>& pCorrSolution) const {
        for (std::size_t i = 0; i < pCorrSolution.size(); ++i) {
            problem.pCorr[i] = pCorrSolution[i];

            problem.p[i] += settings.pressureRelaxation * pCorrSolution[i];
        }
    }

    void SimplecSolver::correctVelocity(NavierStokesProblem& problem,
                                        const std::vector<double>& aPu,
                                        const std::vector<double>& aPv) const {
        if (!problem.mesh) {
            throw std::runtime_error("SimplecSolver::correctVelocity: problem has no mesh");
        }

        const auto& mesh = *problem.mesh;
        const double eps = settings.small;

        std::vector<double> gradPcX(mesh.cells.size(), 0.0);
        std::vector<double> gradPcY(mesh.cells.size(), 0.0);

        for (const auto& face : mesh.faces) {
            const int P = face.owner;
            double pFace = problem.pCorr[P];

            if (face.neighbour.has_value()) {
                const int N = *face.neighbour;
                pFace = 0.5 * (problem.pCorr[P] + problem.pCorr[N]);

                gradPcX[P] += pFace * face.normal[0] * face.length;
                gradPcY[P] += pFace * face.normal[1] * face.length;

                gradPcX[N] -= pFace * face.normal[0] * face.length;
                gradPcY[N] -= pFace * face.normal[1] * face.length;
            } else {
                if (pressureBcs && pressureBcs->has(face.patchName)) {
                    const auto& bc = pressureBcs->get(face.patchName);
                    if (bc.type == PressureBoundaryConditionType::Dirichlet) {
                        pFace = 0.0; // для p' на pressure outlet
                    }
                }

                gradPcX[P] += pFace * face.normal[0] * face.length;
                gradPcY[P] += pFace * face.normal[1] * face.length;
            }
        }

        for (const auto& cell : mesh.cells) {
            const int P = cell.id;
            const double invA = 1.0 / std::max(cell.area, eps);

            const double gx = gradPcX[P] * invA;
            const double gy = gradPcY[P] * invA;

            if (aPu[P] > eps) {
                problem.U[P][0] -= cell.area * gx / aPu[P];
            }
            if (aPv[P] > eps) {
                problem.U[P][1] -= cell.area * gy / aPv[P];
            }
        }

        // const auto& mesh = *problem.mesh;
        // const double eps = settings.small;
        //
        // for (const auto& cell : mesh.cells) {
        //     const int P = cell.id;
        //     double gradPcX = 0.0;
        //     double gradPcY = 0.0;
        //
        //     // Очень простая face-based оценка градиента поправки давления
        //     for (const auto& face : mesh.faces) {
        //         if (face.owner != P) {
        //             continue;
        //         }
        //
        //         double pFace = problem.pCorr[P];
        //
        //         if (face.neighbour.has_value()) {
        //             const int N = *face.neighbour;
        //             pFace = 0.5 * (problem.pCorr[P] + problem.pCorr[N]);
        //         } else if (pressureBcs && pressureBcs->has(face.patchName)) {
        //             const auto& bc = pressureBcs->get(face.patchName);
        //             if (bc.type == PressureBoundaryConditionType::Dirichlet) {
        //                 pFace = bc.value(face.center[0], face.center[1]);
        //             }
        //         }
        //
        //         gradPcX += pFace * face.normal[0] * face.length;
        //         gradPcY += pFace * face.normal[1] * face.length;
        //     }
        //
        //     gradPcX /= std::max(cell.area, eps);
        //     gradPcY /= std::max(cell.area, eps);
        //
        //     if (aPu[P] > eps) {
        //         problem.U[P][0] -= cell.area * gradPcX / aPu[P];
        //     }
        //     if (aPv[P] > eps) {
        //         problem.U[P][1] -= cell.area * gradPcY / aPv[P];
        //     }
        // }
    }

    void SimplecSolver::logIteration() const {
        std::cout
            << "iter = " << iterationState.iteration
            << ", uRes = " << iterationState.uResidual
            << ", vRes = " << iterationState.vResidual
            << ", pRes = " << iterationState.pResidual
            << ", contRes = " << iterationState.continuityResidual
            << '\n';
    }

    void SimplecSolver::solve(NavierStokesProblem& problem) {
    if (!problem.mesh) {
        throw std::runtime_error("SimplecSolver::solve: problem has no mesh");
    }
    if (!velocityBcs) {
        throw std::runtime_error("SimplecSolver::solve: velocity BC set is not specified");
    }
    if (!pressureBcs) {
        throw std::runtime_error("SimplecSolver::solve: pressure BC set is not specified");
    }

    iterationState = SimplecIterationState{};
    problem.resetPressureCorrection();
    problem.Ustar = problem.U;

    for (int iter = 0; iter < settings.maxIterations; ++iter) {
        iterationState.iteration = iter + 1;

        problem.Ustar = problem.U;

        cfd::ScalarField oldPCorr = problem.pCorr;

        // ШАГ 1: вычислить потоки на гранях по текущему полю скорости
        const std::vector<double> faceFluxes =
            fluxCalculator.computeAll(problem, *velocityBcs);

        // ШАГ 2: собрать и решить momentum для Ux
        const cfd::FvMatrix Mu =
            momentumAssembler.assemble(problem, faceFluxes, VelocityComponent::X);
        const std::vector<double> uSolution = linearSolver.solve(Mu);
        const std::vector<double> aPu = extractDiagonal(Mu);

        iterationState.uResidual =
            computeMaxDifferenceComponent(problem.U, uSolution, VelocityComponent::X);

        writeComponentToField(problem.Ustar,
                              uSolution,
                              VelocityComponent::X,
                              settings.momentumRelaxation);

        // ШАГ 3: собрать и решить momentum для Uy
        const cfd::FvMatrix Mv =
            momentumAssembler.assemble(problem, faceFluxes, VelocityComponent::Y);
        const std::vector<double> vSolution = linearSolver.solve(Mv);
        const std::vector<double> aPv = extractDiagonal(Mv);

        iterationState.vResidual =
            computeMaxDifferenceComponent(problem.U, vSolution, VelocityComponent::Y);

        writeComponentToField(problem.Ustar,
                              vSolution,
                              VelocityComponent::Y,
                              settings.momentumRelaxation);

        // переносим предсказанную скорость в основное поле перед pressure step
        problem.U = problem.Ustar;

        // ШАГ 4: пересчитать потоки по предсказанной скорости
        const std::vector<double> predictedFluxes =
            fluxCalculator.computeAll(problem, *velocityBcs);

        // ШАГ 5: собрать и решить pressure correction
        const cfd::FvMatrix MpCorr =
            pressureCorrectionAssembler.assemble(problem, predictedFluxes, aPu, aPv);

        iterationState.continuityResidual = computeContinuityResidual(MpCorr);

        const std::vector<double> pCorrSolution = linearSolver.solve(MpCorr);

        iterationState.pResidual =
            computeMaxDifference(oldPCorr, pCorrSolution);

        // ВАЖНО: записываем решение в поле pCorr
        for (std::size_t i = 0; i < pCorrSolution.size(); ++i) {
            problem.pCorr[i] = pCorrSolution[i];
        }

        // ШАГ 6: скорректировать давление
        correctPressure(problem, pCorrSolution);

        // ШАГ 7: скорректировать скорость через grad(p')
        correctVelocity(problem, aPu, aPv);

        const bool converged =
            iterationState.uResidual < settings.velocityTolerance &&
            iterationState.vResidual < settings.velocityTolerance &&
            iterationState.pResidual < settings.pressureTolerance &&
            iterationState.continuityResidual < settings.continuityTolerance;

        iterationState.converged = converged;

        if ((iter + 1) % settings.logFrequency == 0 || converged || iter == 0) {
            logIteration();
        }

        if (converged) {
            break;
        }
    }
}

} // namespace cfd3b
