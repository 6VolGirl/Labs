//
// Created by 6anna on 29.05.2026.
//

#ifndef NAVIERSTOKESPROBLEM_H
#define NAVIERSTOKESPROBLEM_H


#pragma once

#include "Mesh.h"
#include "ScalarField.h"
#include "VectorField.h"

namespace cfd3b {

    // Постановка задачи стационарного течения вязкой несжимаемой жидкости.
    // Объединяет сетку, поле скорости, давление, поле коррекции давления
    // и основные физические параметры среды.
    class NavierStokesProblem {
    public:
        geom::Mesh* mesh{};
        std::string name{"navier_stokes_problem"};
        cfd::VectorField U;
        cfd::VectorField Ustar;
        cfd::ScalarField p;
        // Поле коррекции давления в SIMPLE/SIMPLEC.
        cfd::ScalarField pCorr;
        double rho{1.0};
        // Динамическая вязкость жидкости.
        double mu{1.0};

        NavierStokesProblem() = default;
        NavierStokesProblem(geom::Mesh& mesh_, double rho_, double mu_, const std::string& name_ = "navier_stokes_problem");

        //  число ячеек в сетке
        std::size_t cellCount() const;

        // Инициализация нулями
        void initializeFields();

        // Постоянное начальное поле скорости
       void setUniformVelocity(const geom::Vec2& value);

       // Постоянное начальное давление
       void setUniformPressure(double value);

       // Полностью обнуляет поправку давления
       void resetPressureCorrection();
    };

} // namespace cfd3b



#endif //NAVIERSTOKESPROBLEM_H
