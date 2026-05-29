//
// Created by 6anna on 16.05.2026.
//

#include "AdvectionDiffusionAssembler.h"

#include "Vec2.h"
#include "UpwindScheme.h"

#include <stdexcept>

namespace cfd {

AdvectionDiffusionAssembler::AdvectionDiffusionAssembler(
    const FaceInterpolationScheme& scheme_,
    const BoundaryConditionSet& boundaryConditions_)
    : scheme(&scheme_), boundaryConditions(&boundaryConditions_) {}

FvMatrix AdvectionDiffusionAssembler::assemble(const ScalarTransportProblem& problem) const {
    if (!problem.mesh) {
        throw std::runtime_error("Problem has no mesh");
    }
    if (!scheme) {
        throw std::runtime_error("Interpolation scheme is not set");
    }
    if (!boundaryConditions) {
        throw std::runtime_error("Boundary conditions are not set");
    }

    const auto& mesh = *problem.mesh;
    FvMatrix M(mesh.cells.size());

    for (const auto& cell : mesh.cells) {
        const int P = cell.id;
        const double xP = cell.center[0];
        const double yP = cell.center[1];

        M.rhs(P) += problem.coefficients.sourceAt(xP, yP) * cell.area;
    }

    const bool isUpwind = (dynamic_cast<const UpwindScheme*>(scheme) != nullptr);


    for (const auto& face : mesh.faces) {
        const int P = face.owner;
        const auto U = problem.coefficients.velocityAt(face.center[0], face.center[1]);
        const double rho = problem.coefficients.rhoAt(face.center[0], face.center[1]);
        const double gamma = problem.coefficients.gammaAt(face.center[0], face.center[1]);

        const double F = rho * geom::dot(U, face.normal) * face.length;
        const double D = (face.dOwnerToNeighbour > 1e-14)
            ? gamma * face.length / face.dOwnerToNeighbour
            : 0.0;

        if (face.neighbour.has_value()) {
            const int N = *face.neighbour;

            M.coeff(P, P) += std::max(F, 0.0) + D;
            M.coeff(P, N) += std::min(F, 0.0) - D;
            M.coeff(N, N) += std::max(-F, 0.0) + D;
            M.coeff(N, P) += std::min(-F, 0.0) - D;

            if (!isUpwind) {
                const double phiF_upwind = (F >= 0.0) ? problem.phi[P] : problem.phi[N];
                const double phiF_high = scheme->faceValue(face, problem.phi, problem.coefficients);
                const double corr = F * (phiF_high - phiF_upwind);

                M.rhs(P) -= corr;
                M.rhs(N) += corr;
            }
        } else {
            if (!boundaryConditions->has(face.patchName)) {
                throw std::runtime_error("Missing BC for patch: " + face.patchName);
            }

            const auto& bc = boundaryConditions->get(face.patchName);
            const double bcValue = bc.value(face.center[0], face.center[1]);

            if (bc.type == BoundaryConditionType::Dirichlet) {
                const double db = (face.dOwnerToFace > 1e-14)
                    ? gamma * face.length / face.dOwnerToFace
                    : 0.0;

                M.coeff(P, P) += std::max(F, 0.0) + db;
                M.rhs(P) += (db + std::max(-F, 0.0)) * bcValue;
            } else if (bc.type == BoundaryConditionType::Neumann) {
                M.rhs(P) += gamma * bcValue * face.length;
                if (F < 0.0) {
                    M.rhs(P) += (-F) * problem.phi[P];
                } else {
                    M.coeff(P, P) += F;
                }
            }
        }
    }

    return M;
}

} // namespace cfd