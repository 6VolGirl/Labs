//
// Created by 6anna on 15.05.2026.
//

#ifndef MESH_H
#define MESH_H

#include "BoundaryPatch.h"
#include "Cell.h"
#include "Face.h"
#include "Vertex.h"

#include <string>
#include <unordered_map>
#include <vector>

namespace geom {
    // Сетка
    class Mesh {
    public:
        std::vector<Vertex> vertices;     // Все вершины сетки
        std::vector<Face> faces;          // Все грани сетки
        std::vector<Cell> cells;          // Все ячейки сетки
        // Карта граничных участков: имя -> BoundaryPatch
        std::unordered_map<std::string, BoundaryPatch> boundaryPatches;

        Mesh() = default;
        Mesh(std::vector<Vertex> vertices_, std::vector<Face> faces_, std::vector<Cell> cells_);

        Vertex& vertex(int id);
        const Vertex& vertex(int id) const;
        Face& face(int id);
        const Face& face(int id) const;
        Cell& cell(int id);
        const Cell& cell(int id) const;

        // Связность сетки: какие грани принадлежат каждой ячейке,
        //                 какие ячейки соседствуют друг с другом
        void buildConnectivity();

        // Геометрия ячеек: площадь, центр ячейки
        // по списку вершин для каждой ячейки.
        void computeCellGeometry();

        // Вычисляет геометрию граней:центр, длину, касательную
        // нормаль, расстояния и векторы между центрами ячеек и гранью.
        void computeFaceGeometry();

        // Проверяет корректность сетки
        void validate() const;

        // Вызывает все методы для создания сетки
        void finalize();

        // Добавляет границы
        void addBoundaryPatch(const std::string& name, const std::vector<int>& faceIds, BoundaryType type);
        const BoundaryPatch& patch(const std::string& name) const;

        std::vector<int> boundaryFaceIds() const;
        std::vector<int> interiorFaceIds() const;

        // Генерирует прямоугольную структурированную сетку nx × ny на прямоугольнике [0, lx] × [0, ly].
        // Автоматически создаёт вершины, ячейки, грани и patch-и: left, right, bottom, top.
        static Mesh structuredRectangle(int nx, int ny, double lx = 1.0, double ly = 1.0);
    };

}



#endif //MESH_H
