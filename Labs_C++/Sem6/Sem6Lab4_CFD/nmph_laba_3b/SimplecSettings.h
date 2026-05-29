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

        double velocityTolerance{1e-8};
        double continuityTolerance{1e-8};
    };

} // namespace cfd3b


#endif //SIMPLECSETTINGS_H
