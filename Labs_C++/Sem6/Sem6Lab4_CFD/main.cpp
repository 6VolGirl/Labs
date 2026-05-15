#include <iostream>

#include "Mesh.h"


int main() {
    geom::Mesh mesh = geom::Mesh::structuredRectangle(4, 3, 1.0, 1.0);

    std::cout << "vertices = " << mesh.vertices.size() << '\n';
    std::cout << "faces = " << mesh.faces.size() << '\n';
    std::cout << "cells = " << mesh.cells.size() << '\n';

    const auto& c0 = mesh.cell(0);
    std::cout << "cell0 center = (" << c0.center[0] << ", " << c0.center[1] << ")\n";
    std::cout << "cell0 area = " << c0.area << '\n';

    const auto& f0 = mesh.face(0);
    std::cout << "face0 center = (" << f0.center[0] << ", " << f0.center[1] << ")\n";
    std::cout << "face0 normal = (" << f0.normal[0] << ", " << f0.normal[1] << ")\n";
    std::cout << "face0 boundary = " << std::boolalpha << f0.isBoundary() << '\n';

    std::cout << "left patch faces = " << mesh.patch("left").faceIds.size() << '\n';
    return 0;
}