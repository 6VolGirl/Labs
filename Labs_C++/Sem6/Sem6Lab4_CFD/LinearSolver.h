//
// Created by 6anna on 16.05.2026.
//

#ifndef LINEARSOLVER_H
#define LINEARSOLVER_H

#include "FvMatrix.h"
#include <vector>

namespace cfd {

    class LinearSolver {
    public:
        virtual ~LinearSolver() = default;
        virtual std::vector<double> solve(const FvMatrix& M) const = 0;
    };

    class DenseGaussSolver : public LinearSolver {
    public:
        std::vector<double> solve(const FvMatrix& M) const override;
    };

} // namespace cfd


#endif //LINEARSOLVER_H
