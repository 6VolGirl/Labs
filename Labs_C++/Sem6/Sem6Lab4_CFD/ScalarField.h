//
// Created by 6anna on 16.05.2026.
//

#ifndef SCALARFIELD_H
#define SCALARFIELD_H

#include "FieldLocation.h"
#include "Functions.h"
#include "Mesh.h"

#include <cstddef>
#include <string>
#include <vector>

namespace cfd {
    // ScalarField — скалярное поле на сетке.
    // Хранит ссылку на сетку, имя поля, место хранения значений
    // (в ячейках или на гранях) и массив числовых значений.
    // Позволяет создать нулевое поле, заполнить его константой,
    // либо вычислить значения по заданной функции от координат.
    class ScalarField {
    public:
        geom::Mesh* mesh{};
        std::string name;
        FieldLocation location{FieldLocation::Cell};
        std::vector<double> values;     // Массив значений поля

        ScalarField() = default;
        ScalarField(geom::Mesh& mesh_, const std::string& name_, FieldLocation location_ = FieldLocation::Cell);

        static ScalarField zeros(geom::Mesh& mesh, const std::string& name, FieldLocation location = FieldLocation::Cell);

        // Возвращает число значений поля:
        // количество ячеек или количество граней.
        std::size_t size() const;

        // Заполняет всё поле одним и тем же значением.
        void fill(double value);

        // Заполняет поле значениями функции от координат.
        void assign(ScalarFunction function);

        // Доступ к значению поля по индексу
        double& operator[](std::size_t index);
        const double& operator[](std::size_t index) const;
    };

}

#endif //SCALARFIELD_H
