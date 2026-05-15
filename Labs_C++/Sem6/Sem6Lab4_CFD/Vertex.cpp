//
// Created by 6anna on 15.05.2026.
//

#include "Vertex.h"

namespace geom {

    Vertex::Vertex(int id_, double x_, double y_) : id(id_), x(x_), y(y_) {}

    Vec2 Vertex::xy() const {
        return {x, y};
    }

}