//
// Created by 6anna on 16.05.2026.
//

#ifndef FACEINTERPOLATIONSCHEME_H
#define FACEINTERPOLATIONSCHEME_H


#include "Mesh.h"
#include "ScalarField.h"
#include "TransportCoefficients.h"


namespace cfd {
    // FaceInterpolationScheme — базовый интерфейс схемы интерполяции
    // значения скалярного поля на грани.
    // По геометрии грани, полю phi и транспортным коэффициентам
    // схема должна вернуть значение phi_f на грани.
    class FaceInterpolationScheme {
    public:
        virtual ~FaceInterpolationScheme() = default;

        virtual double faceValue(const geom::Face& face,
                                 const ScalarField& phi,
                                 const TransportCoefficients& coeffs) const = 0;
    };

} // namespace cfd


#endif //FACEINTERPOLATIONSCHEME_H
