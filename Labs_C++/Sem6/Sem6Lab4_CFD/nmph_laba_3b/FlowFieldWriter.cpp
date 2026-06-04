//
// Created by 6anna on 30.05.2026.
//

#include "FlowFieldWriter.h"


#include <cmath>
#include <fstream>
#include <stdexcept>

namespace cfd3b {

    void FlowFieldWriter::writeCellFieldCsv(const NavierStokesProblem& problem,
                                            const std::string& fileName) {
        if (!problem.mesh) {
            throw std::runtime_error("FlowFieldWriter: problem.mesh is null");
        }

        std::ofstream out(fileName);
        if (!out) {
            throw std::runtime_error("FlowFieldWriter: cannot open output file: " + fileName);
        }

        out << "cellId,x,y,u,v,speed,p,pCorr\n";

        const auto& mesh = *problem.mesh;
        for (const auto& cell : mesh.cells) {
            const int i = cell.id;
            const double u = problem.U[i][0];
            const double v = problem.U[i][1];
            const double speed = std::sqrt(u * u + v * v);

            out << i << ','
                << cell.center[0] << ','
                << cell.center[1] << ','
                << u << ','
                << v << ','
                << speed << ','
                << problem.p[i] << ','
                << problem.pCorr[i] << '\n';
        }
    }

} // namespace cfd3b