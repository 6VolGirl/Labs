//
// Created by 6anna on 30.05.2026.
//

#ifndef STUDYSUMMARYWRITER_H
#define STUDYSUMMARYWRITER_H


#pragma once

#include <string>
#include <vector>

namespace cfd3b {

    struct CaseRunSummary {
        std::string caseName;
        std::string inletType;

        double length{};
        double height{};
        double rho{};
        double mu{};
        double meanInletU{};
        double bulkU{};
        double reynolds{};

        double pIn{};
        double pOut{};
        double pressureDrop{};

        int iterations{};
        bool converged{};

        double uResidual{};
        double vResidual{};
        double pResidual{};
        double continuityResidual{};
    };

    class StudySummaryWriter {
    public:
        static void writeCsv(const std::vector<CaseRunSummary>& rows,
                             const std::string& fileName);
    };

} // namespace cfd3b


#endif //STUDYSUMMARYWRITER_H
