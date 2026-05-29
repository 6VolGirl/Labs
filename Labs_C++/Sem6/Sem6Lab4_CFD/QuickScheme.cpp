//
// Created by 6anna on 29.05.2026.
//

#include "QuickScheme.h"
#include "SchemeStencilUtils.h"

#include <cmath>

namespace cfd {

    QuickScheme::QuickScheme(bool bounded_) : bounded(bounded_) {}

    double QuickScheme::faceValue(const geom::Face& face,
                                  const ScalarField& phi,
                                  const TransportCoefficients& coeffs) const {
        if (!face.neighbour.has_value()) {
            return phi[face.owner];
        }

        const double F = detail::faceMassFlux(face, coeffs);
        const auto [U, D] = detail::upwindDownwind(face, coeffs);
        const double phiU = phi[U];
        const double phiD = phi[D];

        if (std::abs(F) <= 1e-14) {
            return 0.5 * (phiU + phiD);
        }

        const auto UU = detail::farUpwindCell(face, phi, coeffs);
        if (!UU.has_value()) {
            return phiU;
        }

        const double phiUU = phi[*UU];
        double phiF = 0.75 * phiU + 0.375 * phiD - 0.125 * phiUU;

        if (bounded) {
            phiF = detail::clampToBounds(phiF, phiUU, phiU, phiD);
        }

        return phiF;
    }
} // namespace cfd
