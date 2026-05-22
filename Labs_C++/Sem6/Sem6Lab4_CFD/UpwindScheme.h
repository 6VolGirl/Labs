//
// Created by 6anna on 16.05.2026.
//

#ifndef UPWINDSCHEME_H
#define UPWINDSCHEME_H


#include "FaceInterpolationScheme.h"

namespace cfd {

    class UpwindScheme : public FaceInterpolationScheme {
    public:
        double faceValue(const geom::Face& face,
                         const ScalarField& phi,
                         const TransportCoefficients& coeffs) const override;
    };

} // namespace cfd



#endif //UPWINDSCHEME_H
