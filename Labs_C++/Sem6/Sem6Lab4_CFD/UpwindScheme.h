//
// Created by 6anna on 16.05.2026.
//

#ifndef UPWINDSCHEME_H
#define UPWINDSCHEME_H


#include "FaceInterpolationScheme.h"

namespace cfd {
    // UpwindScheme — противопоточная схема первого порядка.
    // Значение на грани берётся из наветренней ячейки
    // в зависимости от направления конвективного потока через грань.
    class UpwindScheme : public FaceInterpolationScheme {
    public:
        // Возвращает значение скалярного поля на грани по upwind-правилу.
        // Если поток через грань направлен от owner к neighbour,
        // используется значение в owner.
        // Если поток направлен в owner через внутреннюю грань,
        // используется значение в neighbour.
        // Для граничной грани без neighbour возвращается значение owner.
        double faceValue(const geom::Face& face,
                         const ScalarField& phi,
                         const TransportCoefficients& coeffs) const override;
    };

} // namespace cfd



#endif //UPWINDSCHEME_H
