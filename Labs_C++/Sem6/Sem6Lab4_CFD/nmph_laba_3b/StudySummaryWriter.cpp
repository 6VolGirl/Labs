//
// Created by 6anna on 30.05.2026.
//

#include "StudySummaryWriter.h"



#include <fstream>
#include <stdexcept>

namespace cfd3b {

    void StudySummaryWriter::writeCsv(const std::vector<CaseRunSummary>& rows,
                                      const std::string& fileName) {
        std::ofstream out(fileName);
        if (!out) {
            throw std::runtime_error("StudySummaryWriter: cannot open " + fileName);
        }

        out << "caseName,inletType,length,height,rho,mu,meanInletU,bulkU,reynolds,"
               "pIn,pOut,pressureDrop,iterations,converged,"
               "uResidual,vResidual,pResidual,continuityResidual\n";

        for (const auto& r : rows) {
            out << r.caseName << ','
                << r.inletType << ','
                << r.length << ','
                << r.height << ','
                << r.rho << ','
                << r.mu << ','
                << r.meanInletU << ','
                << r.bulkU << ','
                << r.reynolds << ','
                << r.pIn << ','
                << r.pOut << ','
                << r.pressureDrop << ','
                << r.iterations << ','
                << (r.converged ? 1 : 0) << ','
                << r.uResidual << ','
                << r.vResidual << ','
                << r.pResidual << ','
                << r.continuityResidual << '\n';
        }
    }

} // namespace cfd3b