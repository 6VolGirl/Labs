#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "Mesh.h"
#include "Vec2.h"

#include "NavierStokesProblem.h"
#include "VelocityBoundaryCondition.h"
#include "VelocityBoundaryConditionSet.h"
#include "PressureBoundaryCondition.h"
#include "PressureBoundaryConditionSet.h"

#include "SimplecSettings.h"
#include "SimplecSolver.h"

#include "ConstantInletProfile.h"
#include "PoiseuilleInletProfile.h"

#include "FlowFieldWriter.h"
#include "ChannelProfileExtractor.h"
#include "ChannelComparisonWriter.h"

namespace {

    enum class InletMode {
        Constant,
        Poiseuille
    };

    std::string inletModeName(InletMode mode) {
        return mode == InletMode::Constant ? "constant" : "poiseuille";
    }

    double averagePressureAtSection(const cfd3b::NavierStokesProblem& problem, double xSection) {
        const auto profile = cfd3b::ChannelProfileExtractor::extractVerticalLine(problem, xSection);

        if (profile.empty()) {
            return 0.0;
        }

        double sum = 0.0;
        for (const auto& s : profile) {
            sum += s.p;
        }

        return sum / static_cast<double>(profile.size());
    }

    void runSingleCase(const std::string& caseName,
                       InletMode inletMode,
                       double length,
                       double height,
                       int nx,
                       int ny,
                       double rho,
                       double mu,
                       double meanInletU) {
        geom::Mesh mesh = geom::Mesh::structuredRectangle(nx, ny, length, height);

        cfd3b::NavierStokesProblem problem(mesh, rho, mu, caseName);
        problem.setUniformVelocity(geom::Vec2{meanInletU, 0.0});
        problem.setUniformPressure(0.0);
        problem.resetPressureCorrection();

        cfd3b::VelocityBoundaryConditionSet velocityBcs;
        cfd3b::PressureBoundaryConditionSet pressureBcs;

        cfd3b::ConstantInletProfile constantProfile(meanInletU);
        cfd3b::PoiseuilleInletProfile poiseuilleProfile(meanInletU, height);

        if (inletMode == InletMode::Constant) {
            velocityBcs.set(
                cfd3b::VelocityBoundaryCondition(
                    cfd3b::VelocityBoundaryConditionType::Dirichlet,
                    "left",
                    [&constantProfile](double x, double y) {
                        return geom::Vec2{constantProfile.value(x, y), 0.0};
                    }
                )
            );
        } else {
            velocityBcs.set(
                cfd3b::VelocityBoundaryCondition(
                    cfd3b::VelocityBoundaryConditionType::Dirichlet,
                    "left",
                    [&poiseuilleProfile](double x, double y) {
                        return geom::Vec2{poiseuilleProfile.value(x, y), 0.0};
                    }
                )
            );
        }

        velocityBcs.set(
            cfd3b::VelocityBoundaryCondition::constant(
                cfd3b::VelocityBoundaryConditionType::Dirichlet,
                "top",
                geom::Vec2{0.0, 0.0}
            )
        );

        velocityBcs.set(
            cfd3b::VelocityBoundaryCondition::constant(
                cfd3b::VelocityBoundaryConditionType::Dirichlet,
                "bottom",
                geom::Vec2{0.0, 0.0}
            )
        );

        velocityBcs.set(
            cfd3b::VelocityBoundaryCondition::constant(
                cfd3b::VelocityBoundaryConditionType::Neumann,
                "right",
                geom::Vec2{0.0, 0.0}
            )
        );

        pressureBcs.set(
            cfd3b::PressureBoundaryCondition::constant(
                cfd3b::PressureBoundaryConditionType::Dirichlet,
                "right",
                0.0
            )
        );

        pressureBcs.set(
            cfd3b::PressureBoundaryCondition::constant(
                cfd3b::PressureBoundaryConditionType::Neumann,
                "left",
                0.0
            )
        );

        pressureBcs.set(
            cfd3b::PressureBoundaryCondition::constant(
                cfd3b::PressureBoundaryConditionType::Neumann,
                "top",
                0.0
            )
        );

        pressureBcs.set(
            cfd3b::PressureBoundaryCondition::constant(
                cfd3b::PressureBoundaryConditionType::Neumann,
                "bottom",
                0.0
            )
        );

        cfd3b::SimplecSettings settings;
        settings.maxIterations = 200;
        settings.velocityTolerance = 1e-6;
        settings.pressureTolerance = 1e-6;
        settings.continuityTolerance = 1e-7;
        settings.momentumRelaxation = 0.3;
        settings.pressureRelaxation = 0.15;
        settings.logFrequency = 10;

        cfd3b::SimplecSolver solver(velocityBcs, pressureBcs, settings);
        solver.solve(problem);

        const auto& st = solver.state();

        const double xProfile = 0.9 * length;
        const auto profile = cfd3b::ChannelProfileExtractor::extractVerticalLine(problem, xProfile);

        const double pIn = averagePressureAtSection(problem, 0.1 * length);
        const double pOut = averagePressureAtSection(problem, 0.9 * length);
        const double dpdx = (length > 0.0) ? (pOut - pIn) / (0.8 * length) : 0.0;

        const std::string prefix = caseName + "_" + inletModeName(inletMode);

        cfd3b::FlowFieldWriter::writeCellFieldCsv(problem, prefix + "_field.csv");
        cfd3b::ChannelComparisonWriter::writeProfileComparisonCsv(
            profile,
            height,
            meanInletU,
            prefix + "_profile.csv"
        );

        std::cout << "\n=== " << prefix << " ===\n";
        std::cout << "iterations = " << st.iteration << '\n';
        std::cout << "uResidual = " << st.uResidual << '\n';
        std::cout << "vResidual = " << st.vResidual << '\n';
        std::cout << "pResidual = " << st.pResidual << '\n';
        std::cout << "continuityResidual = " << st.continuityResidual << '\n';
        std::cout << "converged = " << std::boolalpha << st.converged << '\n';
        std::cout << "pIn = " << pIn << ", pOut = " << pOut << '\n';
        std::cout << "saved: " << prefix << "_field.csv\n";
        std::cout << "saved: " << prefix << "_profile.csv\n";
    }

} // namespace

int main() {
    try {
        const double rho = 1.0;
        const double mu = 0.001;
        const double length = 8.0;
        const double height = 1.0;
        const double meanInletU = 1.0;
        const int nx = 40;
        const int ny = 20;


        runSingleCase("case_L4", InletMode::Constant,
                      length, height, nx, ny, rho, mu, meanInletU);

        // runSingleCase("case_L4", InletMode::Poiseuille,
        //               length, height, nx, ny, rho, mu, meanInletU);
    }
    catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << '\n';
        return 1;
    }

    return 0;
}