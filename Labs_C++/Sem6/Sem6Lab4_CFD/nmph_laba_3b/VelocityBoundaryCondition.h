//
// Created by 6anna on 29.05.2026.
//

#ifndef VELOCITYBOUNDARYCONDITION_H
#define VELOCITYBOUNDARYCONDITION_H


#pragma once

#include <functional>
#include <string>

#include "Vec2.h"

namespace cfd3b {

    // Типы граничных условий для скорости.
    // - Dirichlet: заданная скорость
    // - Neumann: заданный градиент скорости
    enum class VelocityBoundaryConditionType {
        Dirichlet,
        Neumann
    };

    // Функция, задающая векторную скорость в точке границы
    using VelocityBoundaryFunction = std::function<geom::Vec2(double, double)>;

    // Класс одного граничного условия для скорости на одном patch.
    class VelocityBoundaryCondition {
    public:
        VelocityBoundaryConditionType type{VelocityBoundaryConditionType::Dirichlet};
        std::string patchName;

        VelocityBoundaryFunction function;

        VelocityBoundaryCondition() = default;

        VelocityBoundaryCondition(VelocityBoundaryConditionType type_,
                                  std::string patchName_,
                                  VelocityBoundaryFunction function_);

        // Вернуть значение BC в точке границы
        geom::Vec2 value(double x, double y) const;

        static VelocityBoundaryCondition constant(VelocityBoundaryConditionType type,
                                                 const std::string& patchName,
                                                 const geom::Vec2& value);
    };

} // namespace cfd3b



#endif //VELOCITYBOUNDARYCONDITION_H
