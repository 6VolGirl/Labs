//
// Created by 6anna on 29.05.2026.
//

#include "PressureBoundaryCondition.h"

namespace cfd3b {

    PressureBoundaryCondition::PressureBoundaryCondition(
        PressureBoundaryConditionType type_,
        std::string patchName_,
        PressureBoundaryFunction function_)
        : type(type_),
          patchName(std::move(patchName_)),
          function(std::move(function_)) {
    }

    double PressureBoundaryCondition::value(double x, double y) const {
        if (function) {
            return function(x, y);
        }
        return 0.0;
    }

    PressureBoundaryCondition PressureBoundaryCondition::constant(
                              PressureBoundaryConditionType type,
                              const std::string& patchName,
                              double value) {

      return PressureBoundaryCondition(type, patchName,
                                      [value](double, double)
                                       {  return value;  }
                                       );
    }

} // namespace cfd3b