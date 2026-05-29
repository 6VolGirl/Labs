//
// Created by 6anna on 29.05.2026.
//

#include <iostream>
#include <memory>
#include <string>

#include "Mesh.h"
#include "Vec2.h"

#include "ChannelCaseConfig.h"
#include "FlowRunConfig.h"
#include "InletProfile.h"
#include "ConstantInletProfile.h"
#include "PoiseuilleInletProfile.h"
#include "NavierStokesProblem.h"
#include "SimplecSettings.h"

namespace {

void printCaseInfo(const cfd3b::ChannelCaseConfig& cfg,
                   const cfd3b::FlowRunConfig& runCfg,
                   const cfd3b::SimplecSettings& settings,
                   const geom::Mesh& mesh) {
    std::cout << "=== 3B test case ===\n";
    std::cout << "Case name           : " << runCfg.caseName << "\n";
    std::cout << "Cells               : " << mesh.cells.size() << "\n";
    std::cout << "Faces               : " << mesh.faces.size() << "\n";
    std::cout << "Channel length      : " << cfg.length << "\n";
    std::cout << "Channel half-height : " << cfg.halfHeight << "\n";
    std::cout << "rho                 : " << cfg.rho << "\n";
    std::cout << "mu                  : " << cfg.mu << "\n";
    std::cout << "u_in                : " << cfg.inletVelocity << "\n";
    std::cout << "p_out               : " << cfg.outletPressure << "\n";
    std::cout << "SIMPLEC max iters   : " << settings.maxIterations << "\n";
    std::cout << std::endl;
}

void assignInitialVelocityFromProfile(cfd3b::NavierStokesProblem& problem,
                                      const cfd3b::InletProfile& profile) {
    if (!problem.mesh) {
        return;
    }

    for (std::size_t i = 0; i < problem.mesh->cells.size(); ++i) {
        const auto& cell = problem.mesh->cells[i];
        const double x = cell.center[0];
        const double y = cell.center[1];
        const double u = profile.value(x, y);

        problem.U[i] = geom::Vec2{u, 0.0};
        problem.Ustar[i] = geom::Vec2{u, 0.0};
    }
}

void printSampleValues(const geom::Mesh& mesh,
                       const cfd3b::NavierStokesProblem& problem,
                       const cfd3b::InletProfile& constantProfile,
                       const cfd3b::InletProfile& poiseuilleProfile,
                       double halfHeight) {
    std::cout << "=== Profile samples ===\n";
    std::cout << "Constant inlet at y = 0      : " << constantProfile.value(0.0, 0.0) << "\n";
    std::cout << "Poiseuille inlet at y = 0    : " << poiseuilleProfile.value(0.0, 0.0) << "\n";
    std::cout << "Poiseuille inlet at y = h/2  : " << poiseuilleProfile.value(0.0, 0.5 * halfHeight) << "\n";
    std::cout << "Poiseuille inlet at y = h    : " << poiseuilleProfile.value(0.0, halfHeight) << "\n";
    std::cout << std::endl;

    if (!mesh.cells.empty()) {
        const std::size_t first = 0;
        const std::size_t mid = mesh.cells.size() / 2;
        const std::size_t last = mesh.cells.size() - 1;

        std::cout << "=== Field samples ===\n";
        std::cout << "U[first] = (" << problem.U[first][0] << ", " << problem.U[first][1] << ")\n";
        std::cout << "U[mid]   = (" << problem.U[mid][0] << ", " << problem.U[mid][1] << ")\n";
        std::cout << "U[last]  = (" << problem.U[last][0] << ", " << problem.U[last][1] << ")\n";
        std::cout << "p[first] = " << problem.p[first] << "\n";
        std::cout << "pCorr[mid] = " << problem.pCorr[mid] << "\n";
        std::cout << std::endl;
    }
}

} // namespace

int main() {
    cfd3b::ChannelCaseConfig caseCfg;
    caseCfg.nx = 20;
    caseCfg.ny = 10;
    caseCfg.length = 6.0;
    caseCfg.halfHeight = 1.0;
    caseCfg.rho = 1.0;
    caseCfg.mu = 0.1;
    caseCfg.inletVelocity = 1.0;
    caseCfg.outletPressure = 0.0;
    caseCfg.inletType = cfd3b::InletProfileType::Constant;

    cfd3b::FlowRunConfig runCfg;
    runCfg.caseName = "channel_3b_class_test";

    cfd3b::SimplecSettings simplec;
    simplec.maxIterations = 100;
    simplec.momentumRelaxation = 0.7;
    simplec.pressureRelaxation = 0.3;

    geom::Mesh mesh = geom::Mesh::structuredRectangle(
        caseCfg.nx,
        caseCfg.ny,
        caseCfg.length,
        2.0 * caseCfg.halfHeight
    );

    cfd3b::NavierStokesProblem problem(mesh, caseCfg.rho, caseCfg.mu);

    cfd3b::ConstantInletProfile constantProfile(caseCfg.inletVelocity);
    cfd3b::PoiseuilleInletProfile poiseuilleProfile(caseCfg.halfHeight,
                                                    1.5 * caseCfg.inletVelocity);

    const cfd3b::InletProfile* activeProfile = nullptr;
    if (caseCfg.inletType == cfd3b::InletProfileType::Constant) {
        activeProfile = &constantProfile;
    } else {
        activeProfile = &poiseuilleProfile;
    }

    assignInitialVelocityFromProfile(problem, *activeProfile);

    printCaseInfo(caseCfg, runCfg, simplec, mesh);
    printSampleValues(mesh, problem, constantProfile, poiseuilleProfile, caseCfg.halfHeight);

    std::cout << "NavierStokesProblem cell count: " << problem.cellCount() << "\n";
    std::cout << "3B class test finished successfully.\n";

    return 0;
}