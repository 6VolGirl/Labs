//
// Created by 6anna on 16.05.2026.
//

#ifndef ADVECTIONDIFFUSIONASSEMBLER_H
#define ADVECTIONDIFFUSIONASSEMBLER_H

#include "BoundaryConditionSet.h"
#include "FaceInterpolationScheme.h"
#include "FvMatrix.h"
#include "ScalarTransportProblem.h"

namespace cfd {

    class AdvectionDiffusionAssembler {
    public:
        const FaceInterpolationScheme* scheme{};
        const BoundaryConditionSet* boundaryConditions{};

        AdvectionDiffusionAssembler() = default;
        AdvectionDiffusionAssembler(const FaceInterpolationScheme& scheme_,
                                    const BoundaryConditionSet& boundaryConditions_);

        FvMatrix assemble(const ScalarTransportProblem& problem) const;
    };

} // namespace cfd


#endif //ADVECTIONDIFFUSIONASSEMBLER_H
