//
// Created by 6anna on 16.05.2026.
//

#include "UpwindScheme.h"
#include "SchemeStencilUtils.h"
#include "Vec2.h"

namespace cfd {

    double UpwindScheme::faceValue(const geom::Face& face,
                                   const ScalarField& phi,
                                   const TransportCoefficients& coeffs) const {
        const double F = detail::faceMassFlux(face, coeffs);

        if (!face.neighbour.has_value()) {
            return phi[face.owner];
        }

        if (F > 1e-14) {
            return phi[face.owner];
        }
        if (F < -1e-14) {
            return phi[*face.neighbour];
        }

        return 0.5 * (phi[face.owner] + phi[*face.neighbour]);
    }

} // namespace cfd