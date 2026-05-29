//
// Created by 6anna on 16.05.2026.
//

#ifndef LINEARSOLVER_H
#define LINEARSOLVER_H

#include "FvMatrix.h"
#include <vector>

namespace cfd {

    // LinearSolver — абстрактный интерфейс линейного решателя.
    // Любой конкретный решатель должен уметь решать систему FvMatrix
    // и возвращать вектор решения.
    class LinearSolver {
    public:
        virtual ~LinearSolver() = default;
        virtual std::vector<double> solve(const FvMatrix& M) const = 0;
    };

    // DenseGaussSolver — плотный решатель СЛАУ методом Гаусса
    // с частичным выбором главного элемента.
    class DenseGaussSolver : public LinearSolver {
    public:
        std::vector<double> solve(const FvMatrix& M) const override;
    };

} // namespace cfd


#endif //LINEARSOLVER_H
