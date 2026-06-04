cmake_minimum_required(VERSION 3.30)

project(Sem6Lab4_CFD LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --------------------------------
# Общие файлы, которые лежат в корне
# --------------------------------
add_library(cfd_core STATIC
        ScalarField.cpp
        VectorField.cpp
        BoundaryCondition.cpp
        BoundaryConditionSet.cpp
        FvMatrix.cpp
        LinearSolver.cpp
        Vec2.cpp
        Mesh.cpp
        Face.cpp
        Cell.cpp
        Vertex.cpp
        BoundaryPatch.cpp
)

target_include_directories(cfd_core
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# --------------------------------
# Лаба 3a
# --------------------------------
add_executable(nmph_laba_3a
        nmph_laba_3a/TransportCoefficients.cpp
        nmph_laba_3a/ScalarTransportProblem.cpp
        nmph_laba_3a/UpwindScheme.cpp
        nmph_laba_3a/TvdScheme.cpp
        nmph_laba_3a/QuickScheme.cpp
        nmph_laba_3a/AdvectionDiffusionAssembler.cpp
        nmph_laba_3a/main_3a.cpp
)

target_include_directories(nmph_laba_3a
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/nmph_laba_3a
)

target_link_libraries(nmph_laba_3a
        PRIVATE
        cfd_core
)

# --------------------------------
# Лаба 3b
# --------------------------------
add_executable(nmph_laba_3b
        nmph_laba_3b/main_3b.cpp
        nmph_laba_3b/ConstantInletProfile.cpp
        nmph_laba_3b/PoiseuilleInletProfile.cpp
        nmph_laba_3b/NavierStokesProblem.cpp
        nmph_laba_3b/VelocityBoundaryCondition.cpp
        nmph_laba_3b/VelocityBoundaryConditionSet.cpp
        nmph_laba_3b/PressureBoundaryCondition.cpp
        nmph_laba_3b/PressureBoundaryConditionSet.cpp
        nmph_laba_3b/FaceMassFluxCalculator.cpp
        nmph_laba_3b/MomentumEquationAssembler.cpp
        nmph_laba_3b/PressureCorrectionAssembler.cpp
        nmph_laba_3b/SimplecSolver.cpp
        nmph_laba_3b/FlowFieldWriter.cpp
        nmph_laba_3b/ChannelProfileExtractor.cpp
        nmph_laba_3b/ChannelComparisonWriter.cpp
        nmph_laba_3b/FlowFieldWriter.cpp
        nmph_laba_3b/StudySummaryWriter.cpp
)


target_include_directories(nmph_laba_3b
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/nmph_laba_3b
)

target_link_libraries(nmph_laba_3b
        PRIVATE
        cfd_core
)