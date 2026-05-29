//
// Created by 6anna on 29.05.2026.
//

#ifndef INLETPROFILE_H
#define INLETPROFILE_H


#pragma once

namespace cfd3b {

    // Абстрактный интерфейс профиля скорости на входной границе
    // Возврат значения продольной скорости в точке входа по координатам x и y
    class InletProfile {
    public:
        virtual ~InletProfile() = default;

        virtual double value(double x, double y) const = 0;
    };

} // namespace cfd3b


#endif //INLETPROFILE_H
