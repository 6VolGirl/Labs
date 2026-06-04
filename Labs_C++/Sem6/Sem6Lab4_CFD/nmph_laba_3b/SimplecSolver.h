//
// Created by 6anna on 29.05.2026.
//

#ifndef SIMPLECSOLVER_H
#define SIMPLECSOLVER_H



#pragma once

#include <vector>

#include "LinearSolver.h"
#include "NavierStokesProblem.h"
#include "FaceMassFluxCalculator.h"
#include "MomentumEquationAssembler.h"
#include "PressureCorrectionAssembler.h"
#include "PressureBoundaryConditionSet.h"
#include "SimplecIterationState.h"
#include "SimplecSettings.h"
#include "VelocityBoundaryConditionSet.h"

namespace cfd3b {

    // Итерационный решатель SIMPLEC/SIMPLE-подобного типа.
    //
    // без полноценной Rhie-Chow-интерполяции!!!!!!!!!!
    class SimplecSolver {
    private:
        const VelocityBoundaryConditionSet* velocityBcs{};
        const PressureBoundaryConditionSet* pressureBcs{};
        SimplecSettings settings;

        FaceMassFluxCalculator fluxCalculator;
        MomentumEquationAssembler momentumAssembler;
        PressureCorrectionAssembler pressureCorrectionAssembler;
        cfd::DenseGaussSolver linearSolver;

        SimplecIterationState iterationState;

        std::vector<double> extractDiagonal(const cfd::FvMatrix& M) const;

        double computeMaxDifference(const cfd::ScalarField& field, const std::vector<double>& values) const;

        double computeMaxDifferenceComponent(const cfd::VectorField& field,
                                             const std::vector<double>& values,
                                             VelocityComponent component) const;

        double computeContinuityResidual(const cfd::FvMatrix& pressureMatrix) const;

        void writeComponentToField(cfd::VectorField& field,
                                   const std::vector<double>& values,
                                   VelocityComponent component,
                                   double relaxation);

        void correctPressure(NavierStokesProblem& problem, const std::vector<double>& pCorrSolution) const;

        void correctVelocity(NavierStokesProblem& problem,
                             const std::vector<double>& aPu,
                             const std::vector<double>& aPv) const;

        void logIteration() const;


    public:
        SimplecSolver(const VelocityBoundaryConditionSet& velocityBcs_,
                      const PressureBoundaryConditionSet& pressureBcs_,
                      const SimplecSettings& settings_);

        void solve(NavierStokesProblem& problem);

        // Получить состояние последней итерации
        const SimplecIterationState& state() const;


    };

} // namespace cfd3b


#endif //SIMPLECSOLVER_H
