#include "Mesh.h"
#include "ScalarTransportProblem.h"
#include "TransportCoefficients.h"

#include "BoundaryCondition.h"
#include "BoundaryConditionSet.h"
#include "UpwindScheme.h"
#include "TvdScheme.h"
#include "Limiter.h"
#include "AdvectionDiffusionAssembler.h"
#include "LinearSolver.h"
#include "QuickScheme.h"

#include <algorithm>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
#include <iostream>
#include <memory>
#include <vector>
#include <cmath>


struct DiagPoint {
    double s;
    double x;
    double y;
    double phi;
};

enum class TaskType {
    Task1,
    Task2
};

struct SchemeEntry {
    std::string schemeName;     // Для вывода в консоль
    std::string fileTag;
    const cfd::FaceInterpolationScheme* scheme;
};

void saveSolution(const geom::Mesh& mesh,
                  const cfd::ScalarTransportProblem& problem,
                  const std::string& filename) {
    std::ofstream out(filename);
    out << "cell_id,x,y,phi\n";
    out << std::setprecision(16);

    for (const auto& cell : mesh.cells) {
        out << cell.id << ","
            << cell.center[0] << ","
            << cell.center[1] << ","
            << problem.phi[cell.id] << "\n";
    }
}

double exactPhi(TaskType task, double x, double y) {
    switch (task) {
        case TaskType::Task1:
            return (y > x) ? 1.0 : 0.0;

        case TaskType::Task2:
            if (y > x && (y - x) <= 0.5) {
                return 1.0;
            }
            return 0.0;
    }

    return 0.0;
}

std::vector<DiagPoint> extractDiagonal(const geom::Mesh& mesh,
                                       const cfd::ScalarTransportProblem& problem) {
    std::vector<DiagPoint> diag;
    const double eps = 1e-10;

    for (const auto& cell : mesh.cells) {
        const double x = cell.center[0];
        const double y = cell.center[1];

        if (std::abs((x + y) - 1.0) < eps) {
            diag.push_back({x, x, y, problem.phi[cell.id]});
        }
    }

    std::sort(diag.begin(), diag.end(),
              [](const DiagPoint& a, const DiagPoint& b) {
                  return a.s < b.s;
              });

    return diag;
}

void saveDiagonalCut(const geom::Mesh& mesh,
                     const cfd::ScalarTransportProblem& problem,
                     const std::string& filename,
                     TaskType task) {
    const std::vector<DiagPoint> diag = extractDiagonal(mesh, problem);

    std::ofstream out(filename);
    out << "s,x,y,phi,phi_exact\n";
    out << std::setprecision(16);

    for (const auto& p : diag) {
        const double phiExact = exactPhi(task, p.x, p.y);

        out << p.s << ","
            << p.x << ","
            << p.y << ","
            << p.phi << ","
            << phiExact << "\n";
    }
}

std::string gammaToString(double gamma) {
    std::ostringstream gstr;
    gstr << std::fixed << std::setprecision(2) << gamma;
    std::string gs = gstr.str();

    for (char& ch : gs) {
        if (ch == '.') {
            ch = '_';
        }
    }

    return gs;
}

std::string makeSolutionFile(TaskType task,
                             const std::string& fileTag,
                             const std::string& gammaSuffix = "") {
    const std::string prefix = (task == TaskType::Task2) ? "task2_" : "";
    return prefix + "solution_" + fileTag + gammaSuffix + ".csv";
}

std::string makeDiagFile(TaskType task,
                         const std::string& fileTag,
                         const std::string& gammaSuffix = "") {
    const std::string prefix = (task == TaskType::Task2) ? "task2_" : "";
    return prefix + "diag_" + fileTag + gammaSuffix + ".csv";
}

cfd::BoundaryConditionSet makeTask1BCs() {
    cfd::BoundaryConditionSet bcs;

    bcs.add(std::make_shared<cfd::DirichletBC>("left", 1.0));
    bcs.add(std::make_shared<cfd::DirichletBC>("bottom", 0.0));
    bcs.add(std::make_shared<cfd::NeumannBC>("top", 0.0));
    bcs.add(std::make_shared<cfd::NeumannBC>("right", 0.0));

    return bcs;
}

cfd::BoundaryConditionSet makeTask2BCs() {
    cfd::BoundaryConditionSet bcs;

    bcs.add(std::make_shared<cfd::FunctionalDirichletBC>(
        "left",
        [](double, double y) {
            return (y <= 0.5) ? 1.0 : 0.0;
        }
    ));

    bcs.add(std::make_shared<cfd::DirichletBC>("bottom", 0.0));
    bcs.add(std::make_shared<cfd::NeumannBC>("top", 0.0));
    bcs.add(std::make_shared<cfd::NeumannBC>("right", 0.0));

    return bcs;
}

void copySolutionToField(cfd::ScalarTransportProblem& problem,
                         const std::vector<double>& solution) {
    for (std::size_t i = 0; i < solution.size(); ++i) {
        problem.phi[i] = solution[i];
    }
}

void solveOnePass(cfd::ScalarTransportProblem& problem,
                  const cfd::BoundaryConditionSet& bcs,
                  const cfd::FaceInterpolationScheme& scheme) {
    cfd::AdvectionDiffusionAssembler assembler(scheme, bcs);
    cfd::DenseGaussSolver solver;

    cfd::FvMatrix M = assembler.assemble(problem);
    std::vector<double> solution = solver.solve(M);
    copySolutionToField(problem, solution);
}

void solveAndSave(const geom::Mesh& mesh,
                  const cfd::TransportCoefficients& coeffs,
                  const cfd::BoundaryConditionSet& bcs,
                  const cfd::FaceInterpolationScheme& scheme,
                  const std::string& schemeName,
                  const std::string& solutionFile,
                  const std::string& diagFile,
                  TaskType task) {
    cfd::ScalarTransportProblem problem(const_cast<geom::Mesh&>(mesh), coeffs, "phi");

    problem.phi.fill(0.0);

    if (dynamic_cast<const cfd::UpwindScheme*>(&scheme) != nullptr) {
        solveOnePass(problem, bcs, scheme);
    } else {
        cfd::UpwindScheme upwindStarter;
        solveOnePass(problem, bcs, upwindStarter);

        cfd::AdvectionDiffusionAssembler assembler(scheme, bcs);
        cfd::DenseGaussSolver solver;

        const int maxIter = 8;
        const double tol = 1e-6;
        const double alpha = 0.7;

        for (int iter = 0; iter < maxIter; ++iter) {
            cfd::FvMatrix M = assembler.assemble(problem);
            std::vector<double> solution = solver.solve(M);

            double maxDiff = 0.0;

            for (std::size_t i = 0; i < solution.size(); ++i) {
                const double relaxed =
                    (1.0 - alpha) * problem.phi[i] + alpha * solution[i];

                maxDiff = std::max(maxDiff, std::abs(relaxed - problem.phi[i]));
                problem.phi[i] = relaxed;
            }

            if (maxDiff < tol) {
                std::cout << schemeName
                          << " converged in " << (iter + 1)
                          << " nonlinear iterations\n";
                break;
            }
        }
    }

    saveSolution(mesh, problem, solutionFile);
    saveDiagonalCut(mesh, problem, diagFile, task);

    std::cout << schemeName << " solved\n";
    std::cout << "  full field: " << solutionFile << "\n";
    std::cout << "  diagonal  : " << diagFile << "\n";
}

void runSchemesForCase(const geom::Mesh& mesh,
                       const cfd::TransportCoefficients& coeffs,
                       const cfd::BoundaryConditionSet& bcs,
                       const std::vector<SchemeEntry>& schemes,
                       TaskType task) {
    for (const auto& entry : schemes) {
        const std::string solutionFile = makeSolutionFile(task, entry.fileTag);
        const std::string diagFile = makeDiagFile(task, entry.fileTag);

        std::cout << "Start " << entry.schemeName << "\n";
        solveAndSave(mesh, coeffs, bcs, *entry.scheme,
                     entry.schemeName, solutionFile, diagFile, task);
        std::cout << "Finish " << entry.schemeName << "\n";
    }
}

void runGammaSweepForCase(const geom::Mesh& mesh,
                          cfd::TransportCoefficients coeffs,
                          const cfd::BoundaryConditionSet& bcs,
                          const std::vector<SchemeEntry>& schemes,
                          TaskType task,
                          const std::vector<double>& gammas) {
    for (double gamma : gammas) {
        coeffs.setGamma(gamma);
        const std::string gs = gammaToString(gamma);
        const std::string gammaSuffix = "_gamma_" + gs;

        std::cout << "\n===== gamma = " << gamma << " =====\n";

        for (const auto& entry : schemes) {
            const std::string solutionFile =
                makeSolutionFile(task, entry.fileTag, gammaSuffix);
            const std::string diagFile =
                makeDiagFile(task, entry.fileTag, gammaSuffix);

            const std::string runName =
                entry.schemeName + " gamma=" + std::to_string(gamma);

            std::cout << "Start " << runName << "\n";
            solveAndSave(mesh, coeffs, bcs, *entry.scheme,
                         runName, solutionFile, diagFile, task);
            std::cout << "Finish " << runName << "\n";
        }
    }
}

void runTask(const geom::Mesh& mesh,
             const cfd::TransportCoefficients& coeffs,
             const cfd::BoundaryConditionSet& bcs,
             const std::vector<SchemeEntry>& schemes,
             TaskType task,
             const std::vector<double>& gammas) {
    runSchemesForCase(mesh, coeffs, bcs, schemes, task);
    runGammaSweepForCase(mesh, coeffs, bcs, schemes, task, gammas);
}

int main() {
    try {
        const int nx = 40;
        const int ny = 40;
        geom::Mesh mesh = geom::Mesh::structuredRectangle(nx, ny, 1.0, 1.0);

        cfd::TransportCoefficients coeffs;
        coeffs.setRho(1.0);
        coeffs.setGamma(0.0);
        coeffs.setSource(0.0);
        coeffs.setVelocity(geom::Vec2{2.0, 2.0});

        // Новые реализации схем
        cfd::UpwindScheme upwind;
        cfd::TvdScheme tvdMinmod(cfd::LimiterType::Minmod);
        cfd::TvdScheme tvdVanLeer(cfd::LimiterType::VanLeer);
        cfd::TvdScheme tvdSuperbee(cfd::LimiterType::Superbee);
        cfd::QuickScheme quick;

        const std::vector<SchemeEntry> schemes = {
            {"Upwind",       "upwind",       &upwind},
            {"TVD Minmod",   "tvd_minmod",   &tvdMinmod},
            {"TVD VanLeer",  "tvd_vanleer",  &tvdVanLeer},
            {"TVD Superbee", "tvd_superbee", &tvdSuperbee},
            {"QUICK",        "quick",        &quick}
        };

        const std::vector<double> gammas = {0.0, 0.01, 0.05, 0.10, 0.50};

        std::cout << "\n===== TASK 1 =====\n";
        runTask(mesh, coeffs, makeTask1BCs(), schemes, TaskType::Task1, gammas);

        std::cout << "\n===== TASK 2 =====\n";
        runTask(mesh, coeffs, makeTask2BCs(), schemes, TaskType::Task2, gammas);

        std::cout << "\nAll calculations finished.\n";
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
































//
// struct DiagPoint {
//     double s;
//     double x;
//     double y;
//     double phi;
// };
//
// enum class TaskType {
//     Task1,
//     Task2
// };
//
// void saveSolution(const geom::Mesh& mesh,
//                   const cfd::ScalarTransportProblem& problem,
//                   const std::string& filename) {
//     std::ofstream out(filename);
//     out << "cell_id,x,y,phi\n";
//     out << std::setprecision(16);
//
//     for (const auto& cell : mesh.cells) {
//         out << cell.id << ","
//             << cell.center[0] << ","
//             << cell.center[1] << ","
//             << problem.phi[cell.id] << "\n";
//     }
//
//     out.close();
// }
//
// std::vector<DiagPoint> exactSolution1(const geom::Mesh& mesh, const cfd::ScalarTransportProblem& problem) {
//     std::vector<DiagPoint> diag;
//     // так как сетка структурированная и центры ячеек лежат в серединах,
//     // для побочной диагонали берем точки с x + y = 1
//     for (const auto& cell : mesh.cells) {
//         double x = cell.center[0];
//         double y = cell.center[1];
//
//         if (std::abs((x + y) - 1.0) < 1e-12) {
//             diag.push_back({x, x, y, problem.phi[cell.id]});
//         }
//     }
//     return diag;
// }
//
// std::vector<DiagPoint> exactSolution2(const geom::Mesh& mesh,
//                                       const cfd::ScalarTransportProblem& /*problem*/) {
//     std::vector<DiagPoint> diag;
//     const double eps = 1e-10;
//
//     for (const auto& cell : mesh.cells) {
//         const double x = cell.center[0];
//         const double y = cell.center[1];
//
//         // Побочная диагональ: x + y = 1
//         if (std::abs((x + y) - 1.0) < eps) {
//             double phiExact = 0.0;
//
//             if (y > x) {
//                 phiExact = ((y - x) <= 0.5) ? 1.0 : 0.0;
//             }
//
//             diag.push_back({x, x, y, phiExact});
//         }
//     }
//
//     std::sort(diag.begin(), diag.end(),
//               [](const DiagPoint& a, const DiagPoint& b) {
//                   return a.s < b.s;
//               });
//
//     return diag;
// }
//
// double exactPhi(TaskType task, double x, double y) {
//     switch (task) {
//         case TaskType::Task1:
//             return (y > x) ? 1.0 : 0.0;
//
//         case TaskType::Task2:
//             if (y > x && (y - x) <= 0.5) {
//                 return 1.0;
//             }
//         return 0.0;
//     }
//
//     return 0.0;
// }
//
// std::vector<DiagPoint> extractDiagonal(const geom::Mesh& mesh,
//                                        const cfd::ScalarTransportProblem& problem) {
//     std::vector<DiagPoint> diag;
//     const double eps = 1e-10;
//
//     for (const auto& cell : mesh.cells) {
//         const double x = cell.center[0];
//         const double y = cell.center[1];
//
//         if (std::abs((x + y) - 1.0) < eps) {
//             diag.push_back({x, x, y, problem.phi[cell.id]});
//         }
//     }
//
//     std::sort(diag.begin(), diag.end(),
//               [](const DiagPoint& a, const DiagPoint& b) {
//                   return a.s < b.s;
//               });
//
//     return diag;
// }
//
// void saveDiagonalCut(const geom::Mesh& mesh,
//                      const cfd::ScalarTransportProblem& problem,
//                      const std::string& filename,
//                      TaskType task) {
//     std::vector<DiagPoint> diag = extractDiagonal(mesh, problem);
//
//     std::ofstream out(filename);
//     out << "s,x,y,phi,phi_exact\n";
//     out << std::setprecision(16);
//
//     for (const auto& p : diag) {
//         const double phi_exact = exactPhi(task, p.x, p.y);
//
//         out << p.s << ","
//             << p.x << ","
//             << p.y << ","
//             << p.phi << ","
//             << phi_exact << "\n";
//     }
// }
//
// // void saveDiagonalCut(const geom::Mesh& mesh,
// //                      const cfd::ScalarTransportProblem& problem,
// //                      const std::string& filename) {
// //     std::vector<DiagPoint> diag;
// //     diag.reserve(mesh.cells.size());
// //
// //     diag = exactSolution2(mesh, problem);
// //
// //     std::sort(diag.begin(), diag.end(),
// //               [](const DiagPoint& a, const DiagPoint& b) {
// //                   return a.s < b.s;
// //               });
// //
// //     std::ofstream out(filename);
// //     out << "s,x,y,phi,phi_exact\n";
// //     out << std::setprecision(16);
// //
// //     for (const auto& p : diag) {
// //         double phi_exact = (p.x < 0.5) ? 1.0 : 0.0;
// //         out << p.s << ","
// //             << p.x << ","
// //             << p.y << ","
// //             << p.phi << ","
// //             << phi_exact << "\n";
// //     }
// // }
//
// void solveAndSave(const geom::Mesh& mesh,
//                   const cfd::TransportCoefficients& coeffs,
//                   const cfd::BoundaryConditionSet& bcs,
//                   const cfd::FaceInterpolationScheme& scheme,
//                   const std::string& schemeName,
//                  const std::string& solutionFile,
//                  const std::string& diagFile,
//                  TaskType task) {
//     cfd::ScalarTransportProblem problem(const_cast<geom::Mesh&>(mesh), coeffs, "phi");
//
//     problem.phi.fill(0.0);
//
//     cfd::AdvectionDiffusionAssembler assembler(scheme, bcs);
//     cfd::FvMatrix M = assembler.assemble(problem);
//
//     cfd::DenseGaussSolver solver;
//
//     const int maxIter = 200;
//     const double tol = 1e-5;
//     for (int iter = 0; iter < maxIter; ++iter) {
//         cfd::FvMatrix M = assembler.assemble(problem);
//         std::vector<double> solution = solver.solve(M);
//
//         double maxDiff = 0.0;
//         for (std::size_t i = 0; i < solution.size(); ++i) {
//             maxDiff = std::max(maxDiff, std::abs(solution[i] - problem.phi[i]));
//             problem.phi[i] = solution[i];
//         }
//
//         if (maxDiff < tol) {
//             break;
//         }
//     }
//
//     saveSolution(mesh, problem, solutionFile);
//     saveDiagonalCut(mesh, problem, diagFile, task);
//
//     std::cout << schemeName << " solved\n";
//     std::cout << "  full field: " << solutionFile << "\n";
//     std::cout << "  diagonal  : " << diagFile << "\n";
//
//
//     std::cout << schemeName << " solved, file saved: " << solutionFile << "\n";
// }
//
//
//
// int main() {
//     try {
//         // 1. Строим прямоугольную сетку [0,1] x [0,1]
//         const int nx = 40;
//         const int ny = 40;
//         geom::Mesh mesh = geom::Mesh::structuredRectangle(nx, ny, 1.0, 1.0);
//
//         // 2. Задаём коэффициенты задачи:
//         // rho = 1, Gamma = 0, S = 0, v = (2,2)
//         cfd::TransportCoefficients coeffs;
//         coeffs.setRho(1.0);
//         coeffs.setGamma(0.0);
//         coeffs.setSource(0.0);
//         coeffs.setVelocity(geom::Vec2{2.0, 2.0});
//
//         // 3. Схемы
//         cfd::UpwindScheme upwind;
//         // cfd::TvdScheme tvdMinmod(cfd::LimiterType::Minmod);
//         // cfd::TvdScheme tvdVanLeer(cfd::LimiterType::VanLeer);
//         // cfd::TvdScheme tvdSuperbee(cfd::LimiterType::Superbee);
//
//
//         {
//             // 4. Граничные условия
//             cfd::BoundaryConditionSet bcs;
//             bcs.add(std::make_shared<cfd::DirichletBC>("left", 1.0));
//             bcs.add(std::make_shared<cfd::DirichletBC>("bottom", 0.0));
//             bcs.add(std::make_shared<cfd::NeumannBC>("top", 0.0));
//             bcs.add(std::make_shared<cfd::NeumannBC>("right", 0.0));
//
//             TaskType task1 = TaskType::Task1;
//
//             // 5. Решение и сохранение
//             std::cout << "Start Upwind\n";
//             solveAndSave(mesh, coeffs, bcs, upwind,
//                          "Upwind", "solution_upwind.csv",  "diag_upwind.csv", task1);
//             std::cout << "Finish Upwind\n";
//
//             // std::cout << "Start TVD Minmod\n";
//             // solveAndSave(mesh, coeffs, bcs, tvdMinmod,
//             //              "TVD Minmod", "solution_tvd_minmod.csv",  "diag_tvd_minmod.csv", task1);
//             // std::cout << "Finish TVD Minmod\n";
//             //
//             // std::cout << "Start TVD VanLeer\n";
//             // solveAndSave(mesh, coeffs, bcs, tvdVanLeer,
//             //              "TVD VanLeer", "solution_tvd_vanleer.csv", "diag_tvd_valeer.csv", task1);
//             // std::cout << "Finish TVD VanLeer\n";
//             //
//             // std::cout << "Start TVD Superbee\n";
//             // solveAndSave(mesh, coeffs, bcs, tvdSuperbee,
//             //              "TVD Superbee", "solution_tvd_superbee.csv", "diag_tvd_superbee.csv", task1);
//             // std::cout << "Finish TVD Superbee\n";
//
//             std::cout << "\nAll files task1 created:\n";
//
//             // std::vector<double> gammas = {0.0, 0.01, 0.05, 0.1, 0.5};
//             //
//             // for (double gamma : gammas) {
//             //     coeffs.setGamma(gamma);
//             //
//             //     std::ostringstream gstr;
//             //     gstr << std::fixed << std::setprecision(2) << gamma;
//             //     std::string gs = gstr.str();
//             //
//             //     for (char& ch : gs) {
//             //         if (ch == '.') ch = '_';
//             //     }
//             //
//             //     solveAndSave(
//             //         mesh, coeffs, bcs, upwind,
//             //         "Upwind_gamma_" + gs,
//             //         "solution_upwind_gamma_" + gs + ".csv",
//             //         "diag_upwind_gamma_" + gs + ".csv"
//             //     );
//             // }
//
//             std::cout << "\nDiagonal files for different Gamma created.\n";
//         }
//
//        //  // Задание 2
//        //  {
//        //      cfd::BoundaryConditionSet bcs2;
//        //
//        //      // Левая граница:
//        //      // нижняя часть -> phi = 1
//        //      // верхняя часть -> phi = 0
//        //      bcs2.add(std::make_shared<cfd::FunctionalDirichletBC>(
//        //          "left",
//        //          [](double, double y) {
//        //              if (y <= 0.5) {
//        //                  return 1.0;
//        //              }
//        //              return 0.0;
//        //          }
//        //      ));
//        //
//        //      // Нижняя граница
//        //      bcs2.add(std::make_shared<cfd::DirichletBC>("bottom", 0.0));
//        //
//        //      // Верхняя и правая границы: outlet
//        //      bcs2.add(std::make_shared<cfd::NeumannBC>("top", 0.0));
//        //      bcs2.add(std::make_shared<cfd::NeumannBC>("right", 0.0));
//        //
//        //      TaskType task2 = TaskType::Task2;
//        //
//        //      solveAndSave(mesh, coeffs, bcs2, upwind,
//        //                   "Task2 Upwind", "task2_solution_upwind.csv", "task2_diag_upwind.csv", task2);
//        //
//        //      solveAndSave(mesh, coeffs, bcs2, tvdMinmod,
//        //                   "Task2 TVD Minmod", "task2_solution_tvd_minmod.csv", "task2_diag_tvd_minmod.csv", task2);
//        //
//        //      solveAndSave(mesh, coeffs, bcs2, tvdVanLeer,
//        //                   "Task2 TVD VanLeer", "task2_solution_tvd_vanleer.csv", "task2_diag_tvd_valeer.csv", task2);
//        //
//        //      solveAndSave(mesh, coeffs, bcs2, tvdSuperbee,
//        //                   "Task2 TVD Superbee", "task2_solution_tvd_superbee.csv", "task2_diag_tvd_superbee.csv", task2);
//        //
//        //      // std::vector<double> gammas = {0.0, 0.01, 0.05, 0.1, 0.5};
//        //      // for (double gamma : gammas) {
//        //      //     coeffs.setGamma(gamma);
//        //      //
//        //      //     std::ostringstream gstr;
//        //      //     gstr << std::fixed << std::setprecision(2) << gamma;
//        //      //     std::string gs = gstr.str();
//        //      //
//        //      //     for (char& ch : gs) {
//        //      //         if (ch == '.') ch = '_';
//        //      //     }
//        //      //
//        //      //     solveAndSave(
//        //      //         mesh, coeffs, bcs2, upwind,
//        //      //         "Upwind_gamma_" + gs,
//        //      //         "solution_upwind_gamma_" + gs + ".csv",
//        //      //         "diag_upwind_gamma_" + gs + ".csv"
//        //      //     );
//        //      // }
//        //
//        //      std::cout << "\nDiagonal files for different Gamma created.\n";
//        //      std::cout << "\nAll files task2 created:\n";
//        // }
//
//     }
//     catch (const std::exception& e) {
//         std::cerr << "Error: " << e.what() << "\n";
//         return 1;
//     }
//
//     return 0;
// }
