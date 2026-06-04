//
// Created by 6anna on 29.05.2026.
//

#include "VelocityBoundaryCondition.h"


namespace cfd3b {

    VelocityBoundaryCondition::VelocityBoundaryCondition(
        VelocityBoundaryConditionType type_,
        std::string patchName_,
        VelocityBoundaryFunction function_)
        : type(type_),
          patchName(std::move(patchName_)),
          function(std::move(function_)) {
    }

    geom::Vec2 VelocityBoundaryCondition::value(double x, double y) const {
        if (function) {
            return function(x, y);
        }
        return geom::Vec2{0.0, 0.0};
    }

    VelocityBoundaryCondition VelocityBoundaryCondition::constant(
        VelocityBoundaryConditionType type,
        const std::string& patchName,
        const geom::Vec2& value) {
        return VelocityBoundaryCondition(
            type,
            patchName,
            [value](double, double) {
                return value;
            }
        );
    }

} // namespace cfd3b
