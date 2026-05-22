//
// Created by 6anna on 16.05.2026.
//

#include "LinearSolver.h"
#include <cmath>
#include <stdexcept>

namespace cfd {

    std::vector<double> DenseGaussSolver::solve(const FvMatrix& M) const {
        std::vector<std::vector<double>> A = M.A;
        std::vector<double> b = M.b;
        const int n = static_cast<int>(A.size());

        for (int k = 0; k < n; ++k) {
            int pivot = k;
            for (int i = k + 1; i < n; ++i) {
                if (std::abs(A[i][k]) > std::abs(A[pivot][k])) {
                    pivot = i;
                }
            }

            if (std::abs(A[pivot][k]) < 1e-14) {
                throw std::runtime_error("Singular matrix in DenseGaussSolver");
            }

            if (pivot != k) {
                std::swap(A[pivot], A[k]);
                std::swap(b[pivot], b[k]);
            }

            for (int i = k + 1; i < n; ++i) {
                const double factor = A[i][k] / A[k][k];
                for (int j = k; j < n; ++j) {
                    A[i][j] -= factor * A[k][j];
                }
                b[i] -= factor * b[k];
            }
        }

        std::vector<double> x(n, 0.0);
        for (int i = n - 1; i >= 0; --i) {
            double sum = b[i];
            for (int j = i + 1; j < n; ++j) {
                sum -= A[i][j] * x[j];
            }
            x[i] = sum / A[i][i];
        }

        return x;
    }

} // namespace cfd