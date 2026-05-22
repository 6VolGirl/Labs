//
// Created by 6anna on 16.05.2026.
//

#ifndef BOUNDARYCONDITION_H
#define BOUNDARYCONDITION_H



#include "Mesh.h"

#include <memory>
#include <string>
#include <functional>
#include <unordered_map>

namespace cfd {

    enum class BoundaryConditionType {
        Dirichlet,
        Neumann
    };

    class BoundaryCondition {
    public:
        std::string patchName;
        BoundaryConditionType type{BoundaryConditionType::Dirichlet};

        BoundaryCondition() = default;
        BoundaryCondition(std::string patchName_, BoundaryConditionType type_);
        virtual ~BoundaryCondition() = default;

        virtual double value(double x, double y) const = 0;
    };

    class DirichletBC : public BoundaryCondition {
    public:
        double prescribedValue{0.0};

        DirichletBC() = default;
        DirichletBC(const std::string& patchName_, double value_);

        double value(double x, double y) const override;
    };

    class NeumannBC : public BoundaryCondition {
    public:
        double prescribedGradient{0.0};

        NeumannBC() = default;
        NeumannBC(const std::string& patchName_, double gradient_);

        double value(double x, double y) const override;
    };

    class FunctionalDirichletBC : public BoundaryCondition {
    public:
        std::function<double(double, double)> func;

        FunctionalDirichletBC(const std::string& patchName_,
                              std::function<double(double, double)> func_);

        double value(double x, double y) const override;
    };

} // namespace cfd


#endif //BOUNDARYCONDITION_H
