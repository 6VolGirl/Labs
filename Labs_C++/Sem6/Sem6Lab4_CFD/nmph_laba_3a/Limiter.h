//
// Created by 6anna on 16.05.2026.
//

#ifndef LIMITER_H
#define LIMITER_H


#include <algorithm>
#include <cmath>

namespace cfd {

    enum class LimiterType {
        Minmod,
        VanLeer,
        Superbee
    };

    inline double limiterValue(LimiterType type, double r) {
        switch (type) {
            case LimiterType::Minmod:
                return std::max(0.0, std::min(1.0, r));
            case LimiterType::VanLeer:
                return (r + std::abs(r)) / (1.0 + std::abs(r));
            case LimiterType::Superbee:
                return std::max(0.0, std::max(std::min(2.0 * r, 1.0), std::min(r, 2.0)));
            default:
                return 0.0;
        }
    }

} // namespace cfd


#endif //LIMITER_H
