//
// Created by 6anna on 29.05.2026.
//

#include "ConstantInletProfile.h"


namespace cfd3b {

    ConstantInletProfile::ConstantInletProfile(double uIn)
        : u0_(uIn) {
    }

    double ConstantInletProfile::value(double, double) const {
        return u0_;
    }

} // namespace cfd3b