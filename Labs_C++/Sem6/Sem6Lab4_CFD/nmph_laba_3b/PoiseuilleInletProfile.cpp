//
// Created by 6anna on 29.05.2026.
//

#include "PoiseuilleInletProfile.h"
#include <algorithm>
#include <stdexcept>

namespace cfd3b {

    double PoiseuilleInletProfile::value(double, double y) const {
        if (channelHeight <= 0.0) {
            throw std::runtime_error("PoiseuilleInletProfile: channelHeight must be positive");
        }

        const double eta = y / channelHeight;

        if (eta < 0.0 || eta > 1.0) {
            return 0.0;
        }

        return 1.5 * meanVelocity * (1.0 - eta * eta);
    }

} // namespace cfd3b