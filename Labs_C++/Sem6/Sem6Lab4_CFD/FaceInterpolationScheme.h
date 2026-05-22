//
// Created by 6anna on 16.05.2026.
//

#ifndef FACEINTERPOLATIONSCHEME_H
#define FACEINTERPOLATIONSCHEME_H


#include "Mesh.h"
#include "ScalarField.h"
#include "TransportCoefficients.h"


namespace cfd {

    class FaceInterpolationScheme {
    public:
        virtual ~FaceInterpolationScheme() = default;

        virtual double faceValue(const geom::Face& face,
                                 const ScalarField& phi,
                                 const TransportCoefficients& coeffs) const = 0;
    };

} // namespace cfd


#endif //FACEINTERPOLATIONSCHEME_H
