//
// Created by 6anna on 29.05.2026.
//

#ifndef SIMPLECSETTINGS_H
#define SIMPLECSETTINGS_H

#pragma once

namespace cfd3b {

    // Настройки итерационного SIMPLEC-решателя
    // Содержит число внешних итераций, коэффициенты релаксации
    // и критерии остановки по скорости и невязке неразрывности
    class SimplecSettings {
    public:
        int maxIterations{500};

        double momentumRelaxation{0.7};
        double pressureRelaxation{0.3};

        // Критерии остановки
        double velocityTolerance{1e-8};
        double pressureTolerance{1e-8};
        double continuityTolerance{1e-8};

        // Защита от деления на очень маленькие числа
        double small{1e-14};

        // Как часто печатать лог
        int logFrequency{10};
    };

} // namespace cfd3b


#endif //SIMPLECSETTINGS_H
