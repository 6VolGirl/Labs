//
// Created by 6anna on 29.05.2026.
//

#ifndef FACEMASSFLUXCALCULATOR_H
#define FACEMASSFLUXCALCULATOR_H


#pragma once

#include <vector>

#include "NavierStokesProblem.h"
#include "VelocityBoundaryConditionSet.h"
#include "Face.h"
#include "Vec2.h"

namespace cfd3b {

    // Класс для вычисления массовых потоков через грани:
    // F_f = rho * (U_f · n_f) * |S_f|
    // в будущем легко заменить простую интерполяцию на более аккуратную.
    class FaceMassFluxCalculator {
    public:
        FaceMassFluxCalculator() = default;

        // Вычислить скорость на конкретной грани.
        geom::Vec2 faceVelocity(const NavierStokesProblem& problem,
                                const VelocityBoundaryConditionSet& velocityBcs,
                                const geom::Face& face) const;

        // Вычислить массовый поток через конкретную грань.
        double faceMassFlux(const NavierStokesProblem& problem,
                            const VelocityBoundaryConditionSet& velocityBcs,
                            const geom::Face& face) const;

        // Вычислить потоки через все грани сетки.
        std::vector<double> computeAll(const NavierStokesProblem& problem,
                                       const VelocityBoundaryConditionSet& velocityBcs) const;
    };

} // namespace cfd3b


#endif //FACEMASSFLUXCALCULATOR_H
