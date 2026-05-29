//
// Created by 6anna on 16.05.2026.
//

#include "TvdScheme.h"
#include "SchemeStencilUtils.h"
#include "Vec2.h"

#include <cmath>

namespace cfd {

    TvdScheme::TvdScheme(LimiterType limiter_) : limiter(limiter_) {}

    TvdScheme::TvdScheme(LimiterType limiter_, bool boundFaceValue_)
    : limiter(limiter_), boundFaceValue(boundFaceValue_) {}

    double TvdScheme::faceValue(const geom::Face& face,
                                const ScalarField& phi,
                                const TransportCoefficients& coeffs) const {

        //const auto U = coeffs.velocityAt(face.center[0], face.center[1]);
        //const double F = geom::dot(U, face.normal) * face.length;

        const int P = face.owner;

        if (!face.neighbour.has_value()) {
            return phi[P];
        }

        const int N = *face.neighbour;
        const double phiP = phi[P];
        const double phiN = phi[N];
        const double d = phiN - phiP;
        const double F = detail::faceMassFlux(face, coeffs);
        const double eps = 1e-14;

        if (std::abs(F) <= eps) {
            return 0.5 * (phiP + phiN);
        }

        const auto [U, D] = detail::upwindDownwind(face, coeffs);
        const double phiU = phi[U];
        const double phiD = phi[D];

        double r = 0.0;

        if (const auto UU = detail::farUpwindCell(face, phi, coeffs); UU.has_value()) {
            const double phiUU = phi[*UU];
            const double denom = phiD - phiU;
            if (std::abs(denom) > eps) {
                r = (phiU - phiUU) / denom;
            }
        }

        const double psi = limiterValue(limiter, r);

        double phiF = phiU + 0.5 * psi * (phiD - phiU);
        if (boundFaceValue) {
            phiF = detail::clampToBounds(phiF, phiU, phiD);
        }


        return phiF;
    }


    //     if (std::abs(phiN - phiP) > 1e-14) {
    //         r = 1.0;
    //     }
    //
    //     const double psi = limiterValue(limiter, r);
    //
    //     if (F >= 0.0) {
    //         return phiP + 0.5 * psi * (phiN - phiP);
    //     }
    //
    //     return phiN - 0.5 * psi * (phiN - phiP);
    // }

} // namespace cfd