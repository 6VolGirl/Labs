cmake_minimum_required(VERSION 3.30)
project(Sem6Lab4_CFD)

set(CMAKE_CXX_STANDARD 20)

add_executable(Sem6Lab4_CFD
        ScalarField.cpp
        VectorField.cpp
        TransportCoefficients.cpp
        ScalarTransportProblem.cpp
        BoundaryCondition.cpp
        BoundaryConditionSet.cpp
        FvMatrix.cpp
        UpwindScheme.cpp
        TvdScheme.cpp
        LinearSolver.cpp
        AdvectionDiffusionAssembler.cpp
        Vec2.cpp
        Mesh.cpp
        Face.cpp
        Cell.cpp
        Vertex.cpp
        BoundaryPatch.cpp
        QuickScheme.cpp
        main.cpp)
