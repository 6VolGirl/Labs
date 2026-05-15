//
// Created by 6anna on 15.05.2026.
//

#include "Mesh.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <utility>

namespace geom {

    Mesh::Mesh(std::vector<Vertex> vertices_, std::vector<Face> faces_, std::vector<Cell> cells_)
        : vertices(std::move(vertices_)), faces(std::move(faces_)), cells(std::move(cells_)) {}

    Vertex& Mesh::vertex(int id) { return vertices.at(id); }
    const Vertex& Mesh::vertex(int id) const { return vertices.at(id); }
    Face& Mesh::face(int id) { return faces.at(id); }
    const Face& Mesh::face(int id) const { return faces.at(id); }
    Cell& Mesh::cell(int id) { return cells.at(id); }
    const Cell& Mesh::cell(int id) const { return cells.at(id); }

    void Mesh::buildConnectivity() {
        for (auto& c : cells) {
            c.faceIds.clear();
            c.neighbourIds.clear();
        }

        for (const auto& f : faces) {
            if (f.owner < 0 || f.owner >= static_cast<int>(cells.size())) {
                throw std::runtime_error("Face owner index is out of range");
            }
            // Для каждой грани добавляем id  в список граней ячейки
            cells[f.owner].faceIds.push_back(f.id);
            // Проверка внут или нет грань
            if (f.neighbour.has_value()) {
                if (*f.neighbour < 0 || *f.neighbour >= static_cast<int>(cells.size())) {
                    throw std::runtime_error("Face neighbour index is out of range");
                }
                cells[*f.neighbour].faceIds.push_back(f.id);
                cells[f.owner].neighbourIds.push_back(*f.neighbour);
                cells[*f.neighbour].neighbourIds.push_back(f.owner);
            }
        }

        for (auto& c : cells) {
            std::sort(c.faceIds.begin(), c.faceIds.end());
            c.faceIds.erase(std::unique(c.faceIds.begin(), c.faceIds.end()), c.faceIds.end());
            std::sort(c.neighbourIds.begin(), c.neighbourIds.end());
            c.neighbourIds.erase(std::unique(c.neighbourIds.begin(), c.neighbourIds.end()), c.neighbourIds.end());
        }
    }

    void Mesh::computeCellGeometry() {
        for (auto& c : cells) {
            if (c.vertexIds.size() < 3) {
                throw std::runtime_error("Cell must contain at least three vertices");
            }

            double area2 = 0.0;
            double cx = 0.0;
            double cy = 0.0;
            const int n = static_cast<int>(c.vertexIds.size());

            for (int i = 0; i < n; ++i) {
                const Vec2 p = vertices.at(c.vertexIds[i]).xy();
                const Vec2 q = vertices.at(c.vertexIds[(i + 1) % n]).xy();

                const double cr = cross(p, q);
                area2 += cr;

                cx += (p[0] + q[0]) * cr;
                cy += (p[1] + q[1]) * cr;
            }

            if (std::abs(area2) < 1e-14) {
                throw std::runtime_error("Cell area is near zero");
            }

            c.area = std::abs(0.5 * area2);
            c.center = {cx / (3.0 * area2), cy / (3.0 * area2)};
        }
    }
    void Mesh::computeFaceGeometry() {
    for (auto& f : faces) {
        const Vec2 a = vertices.at(f.vertexIds[0]).xy();
        const Vec2 b = vertices.at(f.vertexIds[1]).xy();

        const Vec2 t = vsub(b, a);
        const double len = norm(t);

        if (len < 1e-14) {
            throw std::runtime_error("Face length is near zero");
        }

        f.center = midpoint(a, b);
        f.length = len;
        f.tangent = vmul(t, 1.0 / len);

        Vec2 n{f.tangent[1], -f.tangent[0]};

        // проверяем в ту ли сторону нормаль
        const Vec2 ownerCenter = cells.at(f.owner).center;
        const Vec2 ownerToFace = vsub(f.center, ownerCenter);

        if (dot(n, ownerToFace) < 0.0) {
            n = {-n[0], -n[1]};
        }

        f.normal = n;
        f.ownerToFace = ownerToFace;
        f.dOwnerToFace = norm(ownerToFace);

        //проверяем наличие neighbour
        if (f.neighbour.has_value()) {
            const Vec2 neighbourCenter = cells.at(*f.neighbour).center;
            f.centerToCenter = vsub(neighbourCenter, ownerCenter);
            f.dOwnerToNeighbour = norm(f.centerToCenter);
        } else {
            f.centerToCenter = ownerToFace;
            f.dOwnerToNeighbour = f.dOwnerToFace;
        }
    }
}

void Mesh::validate() const {
    // id элемента должен совпадать с его положением в массиве
    for (std::size_t i = 0; i < vertices.size(); ++i) {
        if (vertices[i].id != static_cast<int>(i)) {
            throw std::runtime_error("Vertex ids must match positions in the vertices array");
        }
    }

    for (std::size_t i = 0; i < cells.size(); ++i) {
        if (cells[i].id != static_cast<int>(i)) {
            throw std::runtime_error("Cell ids must match positions in the cells array");
        }

        for (int vid : cells[i].vertexIds) {
            if (vid < 0 || vid >= static_cast<int>(vertices.size())) {
                throw std::runtime_error("Cell contains an invalid vertex index");
            }
        }
    }

    for (std::size_t i = 0; i < faces.size(); ++i) {
        if (faces[i].id != static_cast<int>(i)) {
            throw std::runtime_error("Face ids must match positions in the faces array");
        }

        for (int vid : faces[i].vertexIds) {
            if (vid < 0 || vid >= static_cast<int>(vertices.size())) {
                throw std::runtime_error("Face contains an invalid vertex index");
            }
        }

        //Ввыходы за массив и id_neighbour != id_owner
        if (faces[i].owner < 0 || faces[i].owner >= static_cast<int>(cells.size())) {
            throw std::runtime_error("Face contains an invalid owner index");
        }

        if (faces[i].neighbour.has_value()) {
            if (*faces[i].neighbour < 0 || *faces[i].neighbour >= static_cast<int>(cells.size())) {
                throw std::runtime_error("Face contains an invalid neighbour index");
            }

            if (*faces[i].neighbour == faces[i].owner) {
                throw std::runtime_error("Face owner and neighbour must be different");
            }
        }
    }

    for (const auto& [name, patch] : boundaryPatches) {
        if (name != patch.name) {
            throw std::runtime_error("Boundary patch key does not match patch.name");
        }

        // Все faceIds должны принадлежать граничной грани
        for (int fid : patch.faceIds) {
            if (fid < 0 || fid >= static_cast<int>(faces.size())) {
                throw std::runtime_error("Boundary patch contains an invalid face index");
            }

            if (!faces[fid].isBoundary()) {
                throw std::runtime_error("Interior face cannot belong to a boundary patch");
            }
        }
    }
}

void Mesh::finalize() {
    validate();
    computeCellGeometry();
    buildConnectivity();
    computeFaceGeometry();
}

void Mesh::addBoundaryPatch(const std::string& name,
                            const std::vector<int>& faceIds,
                            BoundaryType type) {
    boundaryPatches[name] = BoundaryPatch{name, faceIds, type};

    for (int fid : faceIds) {
        auto& f = faces.at(fid);

        if (!f.isBoundary()) {
            throw std::runtime_error("Only boundary faces can be added to boundary patches");
        }

        f.patchName = name;
        f.boundaryType = type;
    }
}

const BoundaryPatch& Mesh::patch(const std::string& name) const {
    auto it = boundaryPatches.find(name);

    if (it == boundaryPatches.end()) {
        throw std::runtime_error("Boundary patch not found: " + name);
    }
    return it->second;
}

std::vector<int> Mesh::boundaryFaceIds() const {
    std::vector<int> ids;
    ids.reserve(faces.size());

    for (const auto& f : faces) {
        if (f.isBoundary()) {
            ids.push_back(f.id);
        }
    }

    return ids;
}

std::vector<int> Mesh::interiorFaceIds() const {
    std::vector<int> ids;
    ids.reserve(faces.size());

    for (const auto& f : faces) {
        if (f.isInterior()) {
            ids.push_back(f.id);
        }
    }

    return ids;
}

Mesh Mesh::structuredRectangle(int nx, int ny, double lx, double ly) {
    if (nx < 1 || ny < 1) {
        throw std::invalid_argument("nx and ny must be positive");
    }

    if (lx <= 0.0 || ly <= 0.0) {
        throw std::invalid_argument("lx and ly must be positive");
    }

    auto vid = [nx](int i, int j) {
        return j * (nx + 1) + i;
    };

    auto cid = [nx](int i, int j) {
        return j * nx + i;
    };

    // Строим все вершины
    std::vector<Vertex> vertices_;
    vertices_.reserve((nx + 1) * (ny + 1));

    for (int j = 0; j <= ny; ++j) {
        const double y = ly * static_cast<double>(j) / ny;

        for (int i = 0; i <= nx; ++i) {
            const double x = lx * static_cast<double>(i) / nx;
            vertices_.emplace_back(vid(i, j), x, y);
        }
    }

    // Строим все ячейки
    std::vector<Cell> cells_;
    cells_.reserve(nx * ny);

    for (int j = 0; j < ny; ++j) {
        for (int i = 0; i < nx; ++i) {
            cells_.emplace_back(
                cid(i, j),
                std::vector<int>{vid(i, j), vid(i + 1, j), vid(i + 1, j + 1), vid(i, j + 1)}
            );
        }
    }

     // Строим все грани
    std::vector<Face> faces_;
    faces_.reserve((nx + 1) * ny + (ny + 1) * nx);

    std::vector<int> leftPatch;
    std::vector<int> rightPatch;
    std::vector<int> bottomPatch;
    std::vector<int> topPatch;

    int faceId = 0;

    // Все вертикальные грани
    for (int j = 0; j < ny; ++j) {
        for (int i = 0; i <= nx; ++i) {
            std::array<int, 2> verts{vid(i, j), vid(i, j + 1)};

            if (i == 0) {
                faces_.emplace_back(faceId, verts, cid(i, j), std::nullopt);
                leftPatch.push_back(faceId);
            } else if (i == nx) {
                faces_.emplace_back(faceId, verts, cid(i - 1, j), std::nullopt);
                rightPatch.push_back(faceId);
            } else {
                faces_.emplace_back(faceId, verts, cid(i - 1, j), cid(i, j));
            }

            ++faceId;
        }
    }

    // Все горизонтальные грани
    for (int j = 0; j <= ny; ++j) {
        for (int i = 0; i < nx; ++i) {
            std::array<int, 2> verts{vid(i, j), vid(i + 1, j)};

            if (j == 0) {
                faces_.emplace_back(faceId, verts, cid(i, j), std::nullopt);
                bottomPatch.push_back(faceId);
            } else if (j == ny) {
                faces_.emplace_back(faceId, verts, cid(i, j - 1), std::nullopt);
                topPatch.push_back(faceId);
            } else {
                faces_.emplace_back(faceId, verts, cid(i, j - 1), cid(i, j));
            }

            ++faceId;
        }
    }

    Mesh mesh{std::move(vertices_), std::move(faces_), std::move(cells_)};

    mesh.addBoundaryPatch("left", leftPatch, BoundaryType::Generic);
    mesh.addBoundaryPatch("right", rightPatch, BoundaryType::Generic);
    mesh.addBoundaryPatch("bottom", bottomPatch, BoundaryType::Generic);
    mesh.addBoundaryPatch("top", topPatch, BoundaryType::Generic);

    mesh.finalize();
    return mesh;
}

}