//
// Created by 6anna on 30.05.2026.
//

#include "ChannelProfileExtractor.h"


#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace cfd3b {

    std::vector<ChannelProfileSample>
    ChannelProfileExtractor::extractVerticalLine(const NavierStokesProblem& problem,
                                                 double xSection) {
        if (!problem.mesh) {
            throw std::runtime_error("ChannelProfileExtractor: problem.mesh is null");
        }

        const auto& mesh = *problem.mesh;
        std::vector<ChannelProfileSample> result;

        double bestDx = 1e100;
        for (const auto& cell : mesh.cells) {
            bestDx = std::min(bestDx, std::abs(cell.center[0] - xSection));
        }

        const double tol = bestDx + 1e-12;

        for (const auto& cell : mesh.cells) {
            if (std::abs(cell.center[0] - xSection) > tol) {
                continue;
            }

            const int i = cell.id;
            const double u = problem.U[i][0];
            const double v = problem.U[i][1];

            ChannelProfileSample s;
            s.x = cell.center[0];
            s.y = cell.center[1];
            s.u = u;
            s.v = v;
            s.speed = std::sqrt(u * u + v * v);
            s.p = problem.p[i];
            result.push_back(s);
        }

        std::sort(result.begin(), result.end(),
                  [](const ChannelProfileSample& a, const ChannelProfileSample& b) {
                      return a.y < b.y;
                  });

        return result;
    }

} // namespace cfd3b