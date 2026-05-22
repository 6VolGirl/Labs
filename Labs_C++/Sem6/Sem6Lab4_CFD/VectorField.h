//
// Created by 6anna on 16.05.2026.
//

#ifndef VECTORFIELD_H
#define VECTORFIELD_H

#include "FieldLocation.h"
#include "Functions.h"
#include "Mesh.h"

#include <cstddef>
#include <string>
#include <vector>

namespace cfd {

    class VectorField {
    public:
        geom::Mesh* mesh{};
        std::string name;
        FieldLocation location{FieldLocation::Cell};
        std::vector<geom::Vec2> values;

        VectorField() = default;
        VectorField(geom::Mesh& mesh_, const std::string& name_, FieldLocation location_ = FieldLocation::Cell);

        static VectorField zeros(geom::Mesh& mesh, const std::string& name, FieldLocation location = FieldLocation::Cell);

        std::size_t size() const;
        void fill(const geom::Vec2& value);
        void assign(VectorFunction function);

        geom::Vec2& operator[](std::size_t index);
        const geom::Vec2& operator[](std::size_t index) const;
    };

} // namespace cfd




#endif //VECTORFIELD_H
