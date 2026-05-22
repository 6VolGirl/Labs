//
// Created by 6anna on 16.05.2026.
//

#include "TransportCoefficients.h"
namespace cfd {

    TransportCoefficients::TransportCoefficients(double rho_,
                                                 double gamma_,
                                                 double source_,
                                                 const geom::Vec2& velocity_)
        : rho(rho_),
          gamma(gamma_),
          source(source_),
          velocity(velocity_) {}


    void TransportCoefficients::setRho(double value) {
        rho = value;
        rhoFunction = nullptr;
    }

    void TransportCoefficients::setRho(ScalarFunction function) {
        rhoFunction = function;
    }


    void TransportCoefficients::setGamma(double value) {
        gamma = value;
        gammaFunction = nullptr;
    }

    void TransportCoefficients::setGamma(ScalarFunction function) {
        gammaFunction = function;
    }


    void TransportCoefficients::setSource(double value) {
        source = value;
        sourceFunction = nullptr;
    }

    void TransportCoefficients::setSource(ScalarFunction function) {
        sourceFunction = function;
    }


    void TransportCoefficients::setVelocity(const geom::Vec2& value) {
        velocity = value;
        velocityFunction = nullptr;
    }

    void TransportCoefficients::setVelocity(VectorFunction function) {
        velocityFunction = function;
    }


    double TransportCoefficients::rhoAt(double x, double y) const {
        if (rhoFunction) {
            return rhoFunction(x, y);
        }
        return rho;
    }

    double TransportCoefficients::gammaAt(double x, double y) const {
        if (gammaFunction) {
            return gammaFunction(x, y);
        }
        return gamma;
    }

    double TransportCoefficients::sourceAt(double x, double y) const {
        if (sourceFunction) {
            return sourceFunction(x, y);
        }
        return source;
    }

    geom::Vec2 TransportCoefficients::velocityAt(double x, double y) const {
        if (velocityFunction) {
            return velocityFunction(x, y);
        }
        return velocity;
    }

} // namespace cfd