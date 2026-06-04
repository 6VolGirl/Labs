//
// Created by 6anna on 29.05.2026.
//

#ifndef PRESSURECORRECTIONASSEMBLER_H
#define PRESSURECORRECTIONASSEMBLER_H


#pragma once

#include <vector>

#include "FvMatrix.h"
#include "NavierStokesProblem.h"
#include "PressureBoundaryConditionSet.h"

namespace cfd3b {

    // Сборщик уравнения коррекции давления.
    //
    // На вход подаются:
    // - предсказанные массовые потоки через грани,
    // - диагонали momentum-матриц для Ux и Uy.
    class PressureCorrectionAssembler {
    private:
        const PressureBoundaryConditionSet* pressureBcs{};

    public:
        explicit PressureCorrectionAssembler(const PressureBoundaryConditionSet& pressureBcs_);

        cfd::FvMatrix assemble(const NavierStokesProblem& problem,
                               const std::vector<double>& predictedFaceFluxes,
                               const std::vector<double>& aPu,
                               const std::vector<double>& aPv) const;

    };

} // namespace cfd3b



#endif //PRESSURECORRECTIONASSEMBLER_H
