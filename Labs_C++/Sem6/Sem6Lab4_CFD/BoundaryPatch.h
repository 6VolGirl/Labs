//
// Created by 6anna on 15.05.2026.
//

#ifndef BOUNDARYPATCH_H
#define BOUNDARYPATCH_H


#include <string>
#include <vector>

namespace geom {
    // BoundaryType — тип граничного участка.
    // Используется для различения внутренних граней и физических границ
    enum class BoundaryType {
        Interior, // внутренняя грань
        Generic,  // граничная грань
        Inlet,    // входная граница
        Outlet,   // выходная граница
        Wall,     // стенка
        //Symmetry
    };

    // BoundaryPatch — именованный участок границы.
    // Объединяет набор граничных граней с одинаковым физическим смыслом
    class BoundaryPatch {
    public:
        std::string name;
        std::vector<int> faceIds;                  // Все грани, принадлежащие этому участку
        BoundaryType type{BoundaryType::Generic};

        BoundaryPatch() = default;
        BoundaryPatch(std::string name_, std::vector<int> faceIds_, BoundaryType type_);
    };

}


#endif //BOUNDARYPATCH_H
