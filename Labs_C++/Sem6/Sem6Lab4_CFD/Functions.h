//
// Created by 6anna on 16.05.2026.
//

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "Vec2.h"
#include <functional>

namespace cfd {
    // ScalarFunction — скалярная функция от координат (x, y).
    // Используется для задания аналитического распределения скалярного поля
    // или коэффициентов, зависящих от координат.
    using ScalarFunction = std::function<double(double, double)>;

    // VectorFunction — векторная функция от координат (x, y).
    // Используется для задания аналитического векторного поля,
    // например поля скорости.
    using VectorFunction = std::function<geom::Vec2(double, double)>;

} // namespace cfd


#endif //FUNCTIONS_H
