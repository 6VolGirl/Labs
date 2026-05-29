//
// Created by 6anna on 16.05.2026.
//

#include "ScalarTransportProblem.h"
#include <stdexcept>

namespace cfd {

    ScalarTransportProblem::ScalarTransportProblem(geom::Mesh& mesh_,
                                                   const std::string& unknownName_)
        : mesh(&mesh_),
          unknownName(unknownName_),
          phi(mesh_, unknownName_, FieldLocation::Cell) {}

    ScalarTransportProblem::ScalarTransportProblem(
        geom::Mesh& mesh_,
        const TransportCoefficients& coefficients_,
        const std::string& unknownName_)
        : mesh(&mesh_),
          unknownName(unknownName_),
          phi(mesh_, unknownName_, FieldLocation::Cell),
          coefficients(coefficients_) {}

    bool ScalarTransportProblem::hasExactSolution() const {
        return static_cast<bool>(exactSolution);
    }

    double ScalarTransportProblem::exactAt(double x, double y) const {
        if (!exactSolution) {
            throw std::runtime_error("Exact solution is not set");
        }
        return exactSolution(x, y);
    }

} // namespace cfd