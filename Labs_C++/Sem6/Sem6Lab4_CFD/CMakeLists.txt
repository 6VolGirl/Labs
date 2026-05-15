cmake_minimum_required(VERSION 3.30)
project(Sem6Lab4_CFD)

set(CMAKE_CXX_STANDARD 20)

add_executable(Sem6Lab4_CFD
        Vec2.cpp
        Mesh.cpp
        Face.cpp
        Cell.cpp
        Vertex.cpp
        BoundaryPatch.cpp
        main.cpp)
