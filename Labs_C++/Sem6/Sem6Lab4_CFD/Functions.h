//
// Created by 6anna on 16.05.2026.
//

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "Vec2.h"
#include <functional>

namespace cfd {

    using ScalarFunction = std::function<double(double, double)>;
    using VectorFunction = std::function<geom::Vec2(double, double)>;

} // namespace cfd


#endif //FUNCTIONS_H
