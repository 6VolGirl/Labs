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
    private:
        double meanVelocity{1.0};
        double channelHeight{1.0};

    public:
        PoiseuilleInletProfile() = default;

        PoiseuilleInletProfile(double meanVelocity_,
                               double channelHeight_)
            : meanVelocity(meanVelocity_), channelHeight(channelHeight_) {}

        double value(double x, double y) const  override;
    };

} // namespace cfd3b


#endif //POISEUILLEINLETPROFILE_H
