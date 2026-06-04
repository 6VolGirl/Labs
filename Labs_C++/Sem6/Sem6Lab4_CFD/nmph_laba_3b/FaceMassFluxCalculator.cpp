//
// Created by 6anna on 29.05.2026.
//

#include "FaceMassFluxCalculator.h"

#include "FaceMassFluxCalculator.h"

#include <stdexcept>

namespace cfd3b {

    geom::Vec2 FaceMassFluxCalculator::faceVelocity(const NavierStokesProblem& problem,
                                                    const VelocityBoundaryConditionSet& velocityBcs,
                                                    const geom::Face& face) const {
        const int P = face.owner;

        // Внутренняя грань: простая линейная интерполяция между ячейками.
        if (face.neighbour.has_value()) {
            const int N = *face.neighbour;
            return geom::Vec2{
                0.5 * (problem.U[P][0] + problem.U[N][0]),
                0.5 * (problem.U[P][1] + problem.U[N][1])
            };
        }

        // Граничная грань: если BC задано как Dirichlet, берём значение BC.
        if (velocityBcs.has(face.patchName)) {
            const auto& bc = velocityBcs.get(face.patchName);

            if (bc.type == VelocityBoundaryConditionType::Dirichlet) {
                return bc.value(face.center[0], face.center[1]);
            }

            // Для Neumann на первом шаге используем owner-cell value
            // как простую аппроксимацию zero-gradient.
            return problem.U[P];
        }

        // Если BC не найден, используем owner value как fallback.
        return problem.U[P];
    }

    double FaceMassFluxCalculator::faceMassFlux(const NavierStokesProblem& problem,
                                                const VelocityBoundaryConditionSet& velocityBcs,
                                                const geom::Face& face) const {
        const auto Uf = faceVelocity(problem, velocityBcs, face);
        return problem.rho * geom::dot(Uf, face.normal) * face.length;
    }

    std::vector<double> FaceMassFluxCalculator::computeAll(const NavierStokesProblem& problem,
                                                           const VelocityBoundaryConditionSet& velocityBcs) const {
        if (!problem.mesh) {
            throw std::runtime_error("FaceMassFluxCalculator: problem has no mesh");
        }

        std::vector<double> fluxes(problem.mesh->faces.size(), 0.0);

        for (std::size_t f = 0; f < problem.mesh->faces.size(); ++f) {
            fluxes[f] = faceMassFlux(problem, velocityBcs, problem.mesh->faces[f]);
        }

        return fluxes;
    }

} // namespace cfd3b