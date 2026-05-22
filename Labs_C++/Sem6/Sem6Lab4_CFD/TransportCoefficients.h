//
// Created by 6anna on 16.05.2026.
//

#ifndef TRANSPORTCOEFFICIENTS_H
#define TRANSPORTCOEFFICIENTS_H


#include "Vec2.h"
#include <functional>

namespace cfd {

// Функция для скалярного коэффициента от координат (x, y)
using ScalarFunction = std::function<double(double, double)>;

// Функция для векторного коэффициента от координат (x, y)
using VectorFunction = std::function<geom::Vec2(double, double)>;

class TransportCoefficients {
public:
    // Плотность rho = 1.
    double rho{1.0};

    // Коэффициент диффузии Gamma = 0.
    double gamma{0.0};

    // Источник S
    double source{0.0};

    // Поле скорости
    geom::Vec2 velocity{0.0, 0.0};

    ScalarFunction rhoFunction;
    ScalarFunction gammaFunction;
    ScalarFunction sourceFunction;
    VectorFunction velocityFunction;


    TransportCoefficients() = default;

    TransportCoefficients(double rho_,
                          double gamma_,
                          double source_,
                          const geom::Vec2& velocity_);


    void setRho(double value);
    void setRho(ScalarFunction function);
    void setGamma(double value);
    void setGamma(ScalarFunction function);
    void setSource(double value);
    void setSource(ScalarFunction function);
    void setVelocity(const geom::Vec2& value);
    void setVelocity(VectorFunction function);

    // Возвращает rho в точке (x, y)
    double rhoAt(double x, double y) const;

    // Возвращает gamma в точке (x, y)
    double gammaAt(double x, double y) const;

    // Возвращает источник S в точке (x, y)
    double sourceAt(double x, double y) const;

    // Возвращает скорость v в точке (x, y)
    geom::Vec2 velocityAt(double x, double y) const;
};

} // namespace cfd



#endif //TRANSPORTCOEFFICIENTS_H
