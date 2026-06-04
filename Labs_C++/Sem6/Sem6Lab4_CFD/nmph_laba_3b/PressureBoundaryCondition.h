//
// Created by 6anna on 29.05.2026.
//

#ifndef PRESSUREBOUNDARYCONDITION_H
#define PRESSUREBOUNDARYCONDITION_H


#pragma once

#include <functional>
#include <string>

namespace cfd3b {

    // Типы граничных условий для давления
    // - Dirichlet
    // - Neumann
    enum class PressureBoundaryConditionType {
        Dirichlet,
        Neumann
    };

    // Функция, задающая давление в точке границы
    using PressureBoundaryFunction = std::function<double(double, double)>;

    // Класс одного граничного условия для давления.
    class PressureBoundaryCondition {
    public:
        PressureBoundaryConditionType type{PressureBoundaryConditionType::Neumann};
        std::string patchName;

        PressureBoundaryFunction function;

        PressureBoundaryCondition() = default;

        PressureBoundaryCondition(PressureBoundaryConditionType type_,
                                  std::string patchName_,
                                  PressureBoundaryFunction function_);

        // Вернуть значение BC в точке
        double value(double x, double y) const;

        static PressureBoundaryCondition constant(PressureBoundaryConditionType type,
                                                  const std::string& patchName,
                                                  double value);
    };

} // namespace cfd3b


#endif //PRESSUREBOUNDARYCONDITION_H
