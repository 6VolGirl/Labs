//
// Created by 6anna on 16.05.2026.
//

#ifndef SCALARTRANSPORTPROBLEM_H
#define SCALARTRANSPORTPROBLEM_H




#include "ScalarField.h"
#include "TransportCoefficients.h"

#include <string>

namespace cfd {

    class ScalarTransportProblem {
    public:
        geom::Mesh* mesh{};
        std::string unknownName{"phi"};
        ScalarField phi;
        TransportCoefficients coefficients;
        ScalarFunction exactSolution;

        ScalarTransportProblem() = default;
        explicit ScalarTransportProblem(geom::Mesh& mesh_, const std::string& unknownName_ = "phi");
        ScalarTransportProblem(geom::Mesh& mesh_, const TransportCoefficients& coefficients_, const std::string& unknownName_ = "phi");

        bool hasExactSolution() const;
        double exactAt(double x, double y) const;
    };
}

#endif //SCALARTRANSPORTPROBLEM_H
