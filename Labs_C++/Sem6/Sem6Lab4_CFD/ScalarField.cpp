//
// Created by 6anna on 16.05.2026.
//

#include "ScalarField.h"
#include "FieldLocation.h"

#include <algorithm>
#include <stdexcept>

namespace cfd {

namespace {

// определяет, сколько элементов должно быть в поле,
std::size_t fieldSize(const geom::Mesh& mesh, FieldLocation location) {
    return (location == FieldLocation::Cell)
        ? mesh.cells.size()
        : mesh.faces.size();
}

} // anonymous namespace


ScalarField::ScalarField(geom::Mesh& mesh_,
                         const std::string& name_,
                         FieldLocation location_)
    : mesh(&mesh_),
      name(name_),
      location(location_),
      values(fieldSize(mesh_, location_), 0.0) {
}


ScalarField ScalarField::zeros(geom::Mesh& mesh,
                               const std::string& name,
                               FieldLocation location) {
    return ScalarField(mesh, name, location);
}


std::size_t ScalarField::size() const {
    return values.size();
}


void ScalarField::fill(double value) {
    // Заполняем весь массив одним значением.
    std::fill(values.begin(), values.end(), value);
}


void ScalarField::assign(ScalarFunction function) {
    if (!mesh) {
        throw std::runtime_error("ScalarField has no mesh");
    }

    if (location == FieldLocation::Cell) {
        // Если поле определено в ячейках, вычисляем функцию в центрах ячеек.
        for (std::size_t i = 0; i < mesh->cells.size(); ++i) {
            const auto& c = mesh->cells[i];
            values[i] = function(c.center[0], c.center[1]);
        }
    } else {
        // Если поле определено на гранях, вычисляем функцию в центрах граней.
        for (std::size_t i = 0; i < mesh->faces.size(); ++i) {
            const auto& f = mesh->faces[i];
            values[i] = function(f.center[0], f.center[1]);
        }
    }
}


double& ScalarField::operator[](std::size_t index) {
    return values.at(index);
}


const double& ScalarField::operator[](std::size_t index) const {
    return values.at(index);
}

}