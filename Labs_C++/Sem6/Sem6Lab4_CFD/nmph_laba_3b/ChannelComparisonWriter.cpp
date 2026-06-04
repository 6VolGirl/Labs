//
// Created by 6anna on 30.05.2026.
//

#include "ChannelComparisonWriter.h"


#include <cmath>
#include <fstream>
#include <stdexcept>

namespace cfd3b {

    double ChannelComparisonWriter::poiseuilleUFromMean(double y,
                                                        double H,
                                                        double meanVelocity) {
        if (H <= 0.0) {
            throw std::runtime_error("ChannelComparisonWriter: H must be positive");
        }

        const double eta = y / H;
        return 6.0 * meanVelocity * eta * (1.0 - eta);
    }

    void ChannelComparisonWriter::writeProfileComparisonCsv(
        const std::vector<ChannelProfileSample>& profile,
        double H,
        double meanVelocity,
        const std::string& fileName) {

        std::ofstream out(fileName);
        if (!out) {
            throw std::runtime_error("ChannelComparisonWriter: cannot open " + fileName);
        }

        out << "x,y,u_numeric,v_numeric,speed_numeric,p,u_theory,abs_error\n";

        for (auto s : profile) {
            s.uTheory = poiseuilleUFromMean(s.y, H, meanVelocity);
            const double absError = std::abs(s.u - s.uTheory);

            out << s.x << ','
                << s.y << ','
                << s.u << ','
                << s.v << ','
                << s.speed << ','
                << s.p << ','
                << s.uTheory << ','
                << absError << '\n';
        }
    }

} // namespace cfd3b