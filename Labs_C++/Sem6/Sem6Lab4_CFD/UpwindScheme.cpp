//
// Created by 6anna on 16.05.2026.
//

#include "UpwindScheme.h"
#include "Vec2.h"

namespace cfd {

    double UpwindScheme::faceValue(const geom::Face& face,
                                   const ScalarField& phi,
                                   const TransportCoefficients& coeffs) const {
        const auto U = coeffs.velocityAt(face.center[0], face.center[1]);
        const double F = geom::dot(U, face.normal) * face.length;

        if (F >= 0.0) {
            return phi[face.owner];
        }

        if (face.neighbour.has_value()) {
            return phi[*face.neighbour];
        }

        return phi[face.owner];
    }

} // namespace cfd