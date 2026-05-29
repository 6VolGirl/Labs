//
// Created by 6anna on 29.05.2026.
//

#ifndef SCHEMESTENCILUTILS_H
#define SCHEMESTENCILUTILS_H

#include "ScalarField.h"
#include "TransportCoefficients.h"
#include "Vec2.h"

#include <algorithm>
#include <cmath>
#include <limits>
#include <optional>

namespace cfd::detail {

inline double faceMassFlux(const geom::Face& face,
                           const TransportCoefficients& coeffs) {
    const double xF = face.center[0];
    const double yF = face.center[1];
    const auto U = coeffs.velocityAt(xF, yF);
    const double rho = coeffs.rhoAt(xF, yF);
    return rho * geom::dot(U, face.normal) * face.length;
}

inline std::pair<int, int> upwindDownwind(const geom::Face& face,
                                          const TransportCoefficients& coeffs) {
    const double F = faceMassFlux(face, coeffs);
    if (F >= 0.0 || !face.neighbour.has_value()) {
        return {face.owner, face.neighbour.has_value() ? *face.neighbour : face.owner};
    }
    return {*face.neighbour, face.owner};
}

inline std::optional<int> farUpwindCell(const geom::Face& face,
                                        const ScalarField& phi,
                                        const TransportCoefficients& coeffs) {
    if (!phi.mesh || !face.neighbour.has_value()) {
        return std::nullopt;
    }

    const auto& mesh = *phi.mesh;
    const double xF = face.center[0];
    const double yF = face.center[1];
    const auto U = coeffs.velocityAt(xF, yF);
    const double speed = geom::norm(U);
    if (speed < 1e-14) {
        return std::nullopt;
    }

    const geom::Vec2 dir = geom::vmul(U, 1.0 / speed);
    const auto [upId, downId] = upwindDownwind(face, coeffs);
    const auto& upCell = mesh.cell(upId);

    std::optional<int> bestId;
    double bestScore = -std::numeric_limits<double>::infinity();

    for (int nb : upCell.neighbourIds) {
        if (nb == downId || nb == upId) {
            continue;
        }

        const geom::Vec2 d = geom::vsub(mesh.cell(nb).center, upCell.center);
        const double along = geom::dot(d, geom::vmul(dir, -1.0));
        if (along <= 1e-12) {
            continue;
        }

        const double lateral = std::abs(geom::cross(d, dir));
        const double score = along - 0.35 * lateral;
        if (score > bestScore) {
            bestScore = score;
            bestId = nb;
        }
    }

    return bestId;
}

inline double clampToBounds(double value, double a, double b) {
    const double lo = std::min(a, b);
    const double hi = std::max(a, b);
    return std::clamp(value, lo, hi);
}

inline double clampToBounds(double value, double a, double b, double c) {
    const double lo = std::min({a, b, c});
    const double hi = std::max({a, b, c});
    return std::clamp(value, lo, hi);
}

} // namespace cfd::detail



#endif //SCHEMESTENCILUTILS_H
