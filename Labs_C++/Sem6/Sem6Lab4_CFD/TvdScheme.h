//
// Created by 6anna on 16.05.2026.
//

#ifndef TVDSCHEME_H
#define TVDSCHEME_H

#include "FaceInterpolationScheme.h"
#include "Limiter.h"

namespace cfd {

    class TvdScheme : public FaceInterpolationScheme {
    public:
        LimiterType limiter{LimiterType::VanLeer};

        TvdScheme() = default;
        explicit TvdScheme(LimiterType limiter_);

        double faceValue(const geom::Face& face,
                         const ScalarField& phi,
                         const TransportCoefficients& coeffs) const override;
    };

} // namespace cfd


#endif //TVDSCHEME_H
