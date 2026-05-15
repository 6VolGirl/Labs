//
// Created by 6anna on 15.05.2026.
//

#ifndef CELL_H
#define CELL_H

#include "Vec2.h"

#include <string>
#include <vector>

namespace geom {

    // Ячейка сетки
    class Cell {
    public:
        int id{};                         // Уникальный номер ячейки
        std::vector<int> vertexIds;       // Вершины ячейки в порядке обхода
        std::vector<int> faceIds;         // Грани, принадлежащие ячейки
        std::vector<int> neighbourIds;    // Соседние ячейки
        Vec2 center{0.0, 0.0};            // Геометрический центр
        double area{0.0};                 // Площадь ячейки
        //std::string tag;

        Cell() = default;
        Cell(int id_, std::vector<int> vertexIds_);
    };

}



#endif //CELL_H
