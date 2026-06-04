//
// Created by 6anna on 29.05.2026.
//

#include "PressureCorrectionAssembler.h"


#include <algorithm>
#include <stdexcept>

namespace cfd3b {

    PressureCorrectionAssembler::PressureCorrectionAssembler(
        const PressureBoundaryConditionSet& pressureBcs_)
        : pressureBcs(&pressureBcs_) {
    }

    cfd::FvMatrix PressureCorrectionAssembler::assemble(
        const NavierStokesProblem& problem,
        const std::vector<double>& predictedFaceFluxes,
        const std::vector<double>& aPu,
        const std::vector<double>& aPv) const {
        if (!problem.mesh) {
            throw std::runtime_error("PressureCorrectionAssembler: problem has no mesh");
        }
        if (!pressureBcs) {
            throw std::runtime_error("PressureCorrectionAssembler: pressure BC set is not specified");
        }

        const auto& mesh = *problem.mesh;

        if (predictedFaceFluxes.size() != mesh.faces.size()) {
            throw std::runtime_error("PressureCorrectionAssembler: predictedFaceFluxes size mismatch");
        }
        if (aPu.size() != mesh.cells.size() || aPv.size() != mesh.cells.size()) {
            throw std::runtime_error("PressureCorrectionAssembler: momentum diagonal size mismatch");
        }

        cfd::FvMatrix M(mesh.cells.size());
        const double eps = 1e-14;

        for (std::size_t f = 0; f < mesh.faces.size(); ++f) {
            const auto& face = mesh.faces[f];
            const int P = face.owner;
            const double Fstar = predictedFaceFluxes[f];

            // Всегда учитываем дисбаланс потока в уравнении непрерывности RHS
            M.rhs(P) -= Fstar;

            if (face.neighbour.has_value()) {
                const int N = *face.neighbour;
                M.rhs(N) += Fstar;

                const double invAuP = (aPu[P] > eps) ? 1.0 / aPu[P] : 0.0;
                const double invAuN = (aPu[N] > eps) ? 1.0 / aPu[N] : 0.0;
                const double invAvP = (aPv[P] > eps) ? 1.0 / aPv[P] : 0.0;
                const double invAvN = (aPv[N] > eps) ? 1.0 / aPv[N] : 0.0;

                const double invAuFace = 0.5 * (invAuP + invAuN);
                const double invAvFace = 0.5 * (invAvP + invAvN);

                const double dFace =
                    invAuFace * face.normal[0] * face.normal[0] +
                    invAvFace * face.normal[1] * face.normal[1];

                const double coeff = (face.dOwnerToNeighbour > eps)
                    ? problem.rho * face.length * face.length * dFace / face.dOwnerToNeighbour
                    : 0.0;

                M.coeff(P, P) += coeff;
                M.coeff(P, N) -= coeff;
                M.coeff(N, N) += coeff;
                M.coeff(N, P) -= coeff;
            } else {
                if (!pressureBcs->has(face.patchName)) {
                    throw std::runtime_error("Missing pressure BC for patch: " + face.patchName);
                }

                const auto& bc = pressureBcs->get(face.patchName);

                if (bc.type == PressureBoundaryConditionType::Dirichlet) {
                    const double invAuP = (aPu[P] > eps) ? 1.0 / aPu[P] : 0.0;
                    const double invAvP = (aPv[P] > eps) ? 1.0 / aPv[P] : 0.0;

                    const double dOwner =
                        invAuP * face.normal[0] * face.normal[0] +
                        invAvP * face.normal[1] * face.normal[1];

                    const double coeff = (face.dOwnerToFace > eps)
                        ? problem.rho * face.length * face.length * dOwner / face.dOwnerToFace
                        : 0.0;

                    M.coeff(P, P) += coeff;
                    //M.rhs(P) += coeff * bc.value(face.center[0], face.center[1]);
                }

                // Для Neumann ничего в матрицу не добавляем:
                // continuity residual уже учтён через Fstar.
            }
        }

        return M;
    }

} // namespace cfd3b