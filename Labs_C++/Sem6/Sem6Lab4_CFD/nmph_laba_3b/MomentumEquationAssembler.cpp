//
// Created by 6anna on 29.05.2026.
//

#include "MomentumEquationAssembler.h"

#include <algorithm>
#include <stdexcept>

namespace cfd3b {

    MomentumEquationAssembler::MomentumEquationAssembler(
        const VelocityBoundaryConditionSet& velocityBcs_,
        const PressureBoundaryConditionSet& pressureBcs_)
        : velocityBcs(&velocityBcs_),
          pressureBcs(&pressureBcs_) {
    }

    double MomentumEquationAssembler::componentValue(const geom::Vec2& v,
                                                     VelocityComponent component) const {
        return (component == VelocityComponent::X) ? v[0] : v[1];
    }

    double MomentumEquationAssembler::boundaryPressureValue(const NavierStokesProblem& problem,
                                                            const geom::Face& face) const {
        const int P = face.owner;

        if (pressureBcs && pressureBcs->has(face.patchName)) {
            const auto& bc = pressureBcs->get(face.patchName);

            if (bc.type == PressureBoundaryConditionType::Dirichlet) {
                return bc.value(face.center[0], face.center[1]);
            }
        }

        // Если давление явно не задано на границе, берём значение owner cell.
        return problem.p[P];
    }

    cfd::FvMatrix MomentumEquationAssembler::assemble(const NavierStokesProblem& problem,
                                                      const std::vector<double>& faceMassFluxes,
                                                      VelocityComponent component) const {
        if (!problem.mesh) {
            throw std::runtime_error("MomentumEquationAssembler: problem has no mesh");
        }
        if (!velocityBcs) {
            throw std::runtime_error("MomentumEquationAssembler: velocity BC set is not specified");
        }
        if (faceMassFluxes.size() != problem.mesh->faces.size()) {
            throw std::runtime_error("MomentumEquationAssembler: faceMassFluxes size mismatch");
        }

        const auto& mesh = *problem.mesh;
        cfd::FvMatrix M(mesh.cells.size());

        // В этом стартовом варианте объёмных источников нет.
        for (const auto& cell : mesh.cells) {
            M.rhs(cell.id) += 0.0 * cell.area;
        }

        for (std::size_t f = 0; f < mesh.faces.size(); ++f) {
            const auto& face = mesh.faces[f];
            const int P = face.owner;
            const double F = faceMassFluxes[f];

            const double mu = problem.mu;

            // Внутренние грани
            if (face.neighbour.has_value()) {
                const int N = *face.neighbour;

                const double D = (face.dOwnerToNeighbour > 1e-14)
                    ? mu * face.length / face.dOwnerToNeighbour
                    : 0.0;

                // Базовая upwind + diffusion матрица
                M.coeff(P, P) += std::max(F, 0.0) + D;
                M.coeff(P, N) += std::min(F, 0.0) - D;
                M.coeff(N, N) += std::max(-F, 0.0) + D;
                M.coeff(N, P) += std::min(-F, 0.0) - D;

                // Давление как поверхностная сила:
                // -∮ p n dS
                const double pFace = 0.5 * (problem.p[P] + problem.p[N]);
                const double nComp = (component == VelocityComponent::X)
                    ? face.normal[0]
                    : face.normal[1];
                const double pressureForce = pFace * nComp * face.length;

                M.rhs(P) -= pressureForce;
                M.rhs(N) += pressureForce;
            }
            // Граничные грани
            else {
                if (!velocityBcs->has(face.patchName)) {
                    throw std::runtime_error("Missing velocity BC for patch: " + face.patchName);
                }

                const auto& bc = velocityBcs->get(face.patchName);
                const double nComp = (component == VelocityComponent::X)
                    ? face.normal[0]
                    : face.normal[1];

                const double pFace = boundaryPressureValue(problem, face);
                const double pressureForce = pFace * nComp * face.length;
                M.rhs(P) -= pressureForce;

                if (bc.type == VelocityBoundaryConditionType::Dirichlet) {
                    const double phiB = componentValue(
                        bc.value(face.center[0], face.center[1]),
                        component
                    );

                    const double db = (face.dOwnerToFace > 1e-14)
                        ? mu * face.length / face.dOwnerToFace
                        : 0.0;

                    M.coeff(P, P) += std::max(F, 0.0) + db;
                    M.rhs(P) += (db + std::max(-F, 0.0)) * phiB;
                } else {
                    // Для Neumann считаем, что bc.value() хранит производную компоненты.
                    const double gradB = componentValue(
                        bc.value(face.center[0], face.center[1]),
                        component
                    );

                    M.rhs(P) += mu * gradB * face.length;

                    if (F < 0.0) {
                        M.rhs(P) += (-F) * componentValue(problem.U[P], component);
                    } else {
                        M.coeff(P, P) += F;
                    }
                }
            }
        }

        return M;
    }

} // namespace cfd3b