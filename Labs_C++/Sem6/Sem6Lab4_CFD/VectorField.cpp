//
// Created by 6anna on 16.05.2026.
//

#include "VectorField.h"

#include <algorithm>
#include <stdexcept>

namespace cfd {

    namespace {
        std::size_t fieldSize(const geom::Mesh& mesh, FieldLocation location) {
            return (location == FieldLocation::Cell)
                ? mesh.cells.size()
                : mesh.faces.size();
        }
    }

    VectorField::VectorField(geom::Mesh& mesh_,
                             const std::string& name_,
                             FieldLocation location_)
        : mesh(&mesh_),
          name(name_),
          location(location_),
          values(fieldSize(mesh_, location_), geom::Vec2{0.0, 0.0}) {}

    VectorField VectorField::zeros(geom::Mesh& mesh,
                                   const std::string& name,
                                   FieldLocation location) {
        return VectorField(mesh, name, location);
    }

    std::size_t VectorField::size() const {
        return values.size();
    }

    void VectorField::fill(const geom::Vec2& value) {
        std::fill(values.begin(), values.end(), value);
    }

    void VectorField::assign(VectorFunction function) {
        if (!mesh) {
            throw std::runtime_error("VectorField has no mesh");
        }

        if (location == FieldLocation::Cell) {
            for (std::size_t i = 0; i < mesh->cells.size(); ++i) {
                const auto& c = mesh->cells[i];
                values[i] = function(c.center[0], c.center[1]);
            }
        } else {
            for (std::size_t i = 0; i < mesh->faces.size(); ++i) {
                const auto& f = mesh->faces[i];
                values[i] = function(f.center[0], f.center[1]);
            }
        }
    }

    geom::Vec2& VectorField::operator[](std::size_t index) {
        return values.at(index);
    }

    const geom::Vec2& VectorField::operator[](std::size_t index) const {
        return values.at(index);
    }

} // namespace cfd