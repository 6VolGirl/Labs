//
// Created by 6anna on 16.05.2026.
//

#ifndef FIELDLOCATION_H
#define FIELDLOCATION_H


namespace cfd {

    // Показывает, где на сетке хранится поле:
    // Cell - в центрах ячеек,
    // Face - в центрах граней.
    enum class FieldLocation {
        Cell,
        Face
    };

} // namespace cfd



#endif //FIELDLOCATION_H
