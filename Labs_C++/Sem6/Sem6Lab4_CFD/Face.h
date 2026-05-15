//
// Created by 6anna on 15.05.2026.
//

#ifndef FACE_H
#define FACE_H

#include "BoundaryPatch.h"
#include "Vec2.h"

#include <array>
#include <optional>
#include <string>

namespace geom {

    // Грань сетки
    class Face {
    public:
        int id{};                         // номер грани
        std::array<int, 2> vertexIds{};   // две вешни данной грани
        int owner{-1};                    // Ячейка владельца
        std::optional<int> neighbour{};   // соседняя ячейка
        std::string patchName;            // имя граничного объекта
        BoundaryType boundaryType{BoundaryType::Interior};

        Vec2 center{0.0, 0.0};           // Центр грани
        Vec2 tangent{0.0, 0.0};          // Касательная к грани
        Vec2 normal{0.0, 0.0};           // Нормаль к грани(наружу owner)
        Vec2 ownerToFace{0.0, 0.0};      // Вектор от центра owner к центру грани
        Vec2 centerToCenter{0.0, 0.0};   // Вектор от центра owner к центру neighbour
        double length{0.0};              // Длина грани
        double dOwnerToFace{0.0};        // Расстояние от центра owner до центра грани
        double dOwnerToNeighbour{0.0};   // Расстояние между центрами owner и neighbour

        Face() = default;
        // Если neighbour не задан, грань считается граничной
        Face(int id_, std::array<int, 2> vertexIds_, int owner_, std::optional<int> neighbour_ = std::nullopt);

        bool isBoundary() const;
        bool isInterior() const;
    };

}


#endif //FACE_H
