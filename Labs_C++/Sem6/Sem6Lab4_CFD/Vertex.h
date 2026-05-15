//
// Created by 6anna on 15.05.2026.
//

#ifndef VERTEX_H
#define VERTEX_H

#include "Vec2.h"

namespace geom {

    // Вершина сетки
    class Vertex {
    public:
        int id{};    // номер вершины
        double x{};  // коорда x
        double y{};  // коорда y

        Vertex() = default;
        Vertex(int id_, double x_, double y_);

        Vec2 xy() const;
    };

}


#endif //VERTEX_H
