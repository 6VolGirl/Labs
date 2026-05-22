//
// Created by 6anna on 16.05.2026.
//

#include "FvMatrix.h"

namespace cfd {

    FvMatrix::FvMatrix(std::size_t n)
        : A(n, std::vector<double>(n, 0.0)), b(n, 0.0) {}

    std::size_t FvMatrix::size() const {
        return A.size();
    }

    double& FvMatrix::coeff(std::size_t i, std::size_t j) {
        return A[i][j];
    }

    const double& FvMatrix::coeff(std::size_t i, std::size_t j) const {
        return A[i][j];
    }

    double& FvMatrix::rhs(std::size_t i) {
        return b[i];
    }

    const double& FvMatrix::rhs(std::size_t i) const {
        return b[i];
    }

} // namespace cfd