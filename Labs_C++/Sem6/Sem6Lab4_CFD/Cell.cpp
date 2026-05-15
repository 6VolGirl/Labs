//
// Created by 6anna on 15.05.2026.
//

#include "Cell.h"

#include <utility>

namespace geom {

    Cell::Cell(int id_, std::vector<int> vertexIds_)
        : id(id_), vertexIds(std::move(vertexIds_)) {}

}