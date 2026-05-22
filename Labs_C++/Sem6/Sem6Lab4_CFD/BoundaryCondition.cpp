//
// Created by 6anna on 16.05.2026.
//

#include "BoundaryCondition.h"
#include <utility>

namespace cfd {

    BoundaryCondition::BoundaryCondition(std::string patchName_, BoundaryConditionType type_)
        : patchName(std::move(patchName_)), type(type_) {}

    DirichletBC::DirichletBC(const std::string& patchName_, double value_)
        : BoundaryCondition(patchName_, BoundaryConditionType::Dirichlet),
          prescribedValue(value_) {}

    double DirichletBC::value(double, double) const {
        return prescribedValue;
    }

    NeumannBC::NeumannBC(const std::string& patchName_, double gradient_)
        : BoundaryCondition(patchName_, BoundaryConditionType::Neumann),
          prescribedGradient(gradient_) {}

    double NeumannBC::value(double, double) const {
        return prescribedGradient;
    }

    FunctionalDirichletBC::FunctionalDirichletBC(
    const std::string& patchName_,
    std::function<double(double, double)> func_)
    : BoundaryCondition(patchName_, BoundaryConditionType::Dirichlet),
      func(func_) {}

    double FunctionalDirichletBC::value(double x, double y) const {
        return func(x, y);
    }

} // namespace cfd