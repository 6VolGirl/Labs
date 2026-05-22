//
// Created by 6anna on 16.05.2026.
//

#include "TvdScheme.h"
#include "Vec2.h"

#include <cmath>

namespace cfd {

    TvdScheme::TvdScheme(LimiterType limiter_) : limiter(limiter_) {}

    double TvdScheme::faceValue(const geom::Face& face,
                                const ScalarField& phi,
                                const TransportCoefficients& coeffs) const {
        const auto U = coeffs.velocityAt(face.center[0], face.center[1]);
        const double F = geom::dot(U, face.normal) * face.length;

        const int P = face.owner;
        const int N = face.neighbour.value_or(face.owner);

        if (!face.neighbour.has_value()) {
            return phi[P];
        }

        const double phiP = phi[P];
        const double phiN = phi[N];

        double r = 0.0;
        if (std::abs(phiN - phiP) > 1e-14) {
            r = 1.0;
        }

        const double psi = limiterValue(limiter, r);

        if (F >= 0.0) {
            return phiP + 0.5 * psi * (phiN - phiP);
        }

        return phiN - 0.5 * psi * (phiN - phiP);
    }

} // namespace cfd