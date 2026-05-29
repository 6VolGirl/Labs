//
// Created by 6anna on 29.05.2026.
//

#include "PoiseuilleInletProfile.h"


namespace cfd3b {

    PoiseuilleInletProfile::PoiseuilleInletProfile(double halfHeight, double uMax)
        : h_(halfHeight), umax_(uMax) {
    }

    double PoiseuilleInletProfile::value(double, double y) const {
        if (h_ <= 0.0) {
            return 0.0;
        }

        const double eta = y / h_;
        const double profile = 1.0 - eta * eta;

        if (profile <= 0.0) {
            return 0.0;
        }

        return umax_ * profile;
    }

} // namespace cfd3b