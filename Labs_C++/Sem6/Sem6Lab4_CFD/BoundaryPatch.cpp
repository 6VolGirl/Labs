//
// Created by 6anna on 15.05.2026.
//

#include "BoundaryPatch.h"
#include <utility>

namespace geom {

    BoundaryPatch::BoundaryPatch(std::string name_, std::vector<int> faceIds_, BoundaryType type_)
        : name(std::move(name_)), faceIds(std::move(faceIds_)), type(type_) {}

}
