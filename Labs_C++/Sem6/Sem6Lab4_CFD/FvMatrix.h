//
// Created by 6anna on 16.05.2026.
//

#ifndef FVMATRIX_H
#define FVMATRIX_H



#include <cstddef>
#include <vector>

namespace cfd {

    class FvMatrix {
    public:
        std::vector<std::vector<double>> A;
        std::vector<double> b;

        FvMatrix() = default;
        explicit FvMatrix(std::size_t n);

        std::size_t size() const;

        double& coeff(std::size_t i, std::size_t j);
        const double& coeff(std::size_t i, std::size_t j) const;

        double& rhs(std::size_t i);
        const double& rhs(std::size_t i) const;
    };

} // namespace cfd



#endif //FVMATRIX_H
