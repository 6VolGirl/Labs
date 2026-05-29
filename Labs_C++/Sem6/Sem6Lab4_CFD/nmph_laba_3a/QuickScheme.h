//
// Created by 6anna on 29.05.2026.
//

#ifndef QUICKSCHEME_H
#define QUICKSCHEME_H


#include "FaceInterpolationScheme.h"

namespace cfd {

    class QuickScheme : public FaceInterpolationScheme {
    public:
        bool bounded{true};

        QuickScheme() = default;
        explicit QuickScheme(bool bounded_);

        double faceValue(const geom::Face& face,
                         const ScalarField& phi,
                         const TransportCoefficients& coeffs) const override;
    };

} // namespace cfd


#endif //QUICKSCHEME_H
