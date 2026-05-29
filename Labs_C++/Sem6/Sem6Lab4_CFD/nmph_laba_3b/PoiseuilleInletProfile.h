//
// Created by 6anna on 29.05.2026.
//

#ifndef POISEUILLEINLETPROFILE_H
#define POISEUILLEINLETPROFILE_H


#pragma once

#include "InletProfile.h"

namespace cfd3b {

    // Аналитический параболический профиль скорости для течения в плоском канале
    // на входе задаётся теоретическое распределение Пуазейля
    class PoiseuilleInletProfile : public InletProfile {
    public:
        PoiseuilleInletProfile(double halfHeight, double uMax);

        double value(double x, double y) const override;

    private:
        double h_{1.0};
        double umax_{1.0};
    };

} // namespace cfd3b


#endif //POISEUILLEINLETPROFILE_H
