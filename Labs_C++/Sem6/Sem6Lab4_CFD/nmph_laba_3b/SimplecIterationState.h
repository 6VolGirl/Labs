//
// Created by 6anna on 29.05.2026.
//

#ifndef SIMPLECITERATIONSTATE_H
#define SIMPLECITERATIONSTATE_H


#pragma once

namespace cfd3b {


    class SimplecIterationState {
    public:
        int iteration{0};

        double uResidual{0.0};
        double vResidual{0.0};
        double pResidual{0.0};
        double continuityResidual{0.0};

        bool converged{false};
    };

} // namespace cfd3b



#endif //SIMPLECITERATIONSTATE_H
