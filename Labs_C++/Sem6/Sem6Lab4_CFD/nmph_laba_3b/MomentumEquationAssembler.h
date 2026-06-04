//
// Created by 6anna on 29.05.2026.
//

#ifndef MOMENTUMEQUATIONASSEMBLER_H
#define MOMENTUMEQUATIONASSEMBLER_H


#pragma once

#include <vector>

#include "FvMatrix.h"
#include "NavierStokesProblem.h"
#include "PressureBoundaryConditionSet.h"
#include "VelocityBoundaryConditionSet.h"

namespace cfd3b {

    enum class VelocityComponent {
        X,
        Y
    };

    // Сборщик одного скалярного кравнения импульса:
    // отдельно для Ux и отдельно для Uy.
    class MomentumEquationAssembler {
    private:
        const VelocityBoundaryConditionSet* velocityBcs{};
        const PressureBoundaryConditionSet* pressureBcs{};

        double componentValue(const geom::Vec2& v, VelocityComponent component) const;
        double boundaryPressureValue(const NavierStokesProblem& problem,
                                     const geom::Face& face) const;

    public:
        MomentumEquationAssembler(const VelocityBoundaryConditionSet& velocityBcs_,
                                  const PressureBoundaryConditionSet& pressureBcs_);

        // Собрать матрицу для одной компоненты скорости.
        cfd::FvMatrix assemble(const NavierStokesProblem& problem,
                               const std::vector<double>& faceMassFluxes,
                               VelocityComponent component) const;

       };

} // namespace cfd3b



#endif //MOMENTUMEQUATIONASSEMBLER_H
