//
// Created by 6anna on 15.05.2026.
//

#include "Face.h"
#include <utility>

namespace geom {

    Face::Face(int id_, std::array<int, 2> vertexIds_, int owner_, std::optional<int> neighbour_)
        : id(id_), vertexIds(vertexIds_), owner(owner_), neighbour(neighbour_) {}

    bool Face::isBoundary() const {
        return !neighbour.has_value();
    }

    bool Face::isInterior() const {
        return neighbour.has_value();
    }

}