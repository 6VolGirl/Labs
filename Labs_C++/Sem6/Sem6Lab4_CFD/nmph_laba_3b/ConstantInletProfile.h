//
// Created by 6anna on 29.05.2026.
//

#ifndef CONSTANTINLETPROFILE_H
#define CONSTANTINLETPROFILE_H


#pragma once

#include "InletProfile.h"

namespace cfd3b {

    // Профиль входной скорости с постоянным значением по всей высоте канала
    // на inlet задаётся одна и та же скорость
    class ConstantInletProfile : public InletProfile {
    public:
        explicit ConstantInletProfile(double uIn);

        double value(double x, double y) const override;

    private:
        double u0_{0.0};
    };

} // namespace cfd3b



#endif //CONSTANTINLETPROFILE_H
