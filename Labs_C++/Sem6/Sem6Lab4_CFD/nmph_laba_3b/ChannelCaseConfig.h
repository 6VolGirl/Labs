//
// Created by 6anna on 29.05.2026.
//

#ifndef CHANNELCASECONFIG_H
#define CHANNELCASECONFIG_H


#pragma once

namespace cfd3b {

    // Тип задания профиля скорости на входной границе канала
    // постоянный inlet и аналитический профиль Пуазейля
    enum class InletProfileType {
        Constant,
        Poiseuille
    };

    // Конфигурация одной расчётной задачи для ламинарного течения в канале
    // Хранит параметры сетки, геометрию канала, физические свойства жидкости
    // и тип граничных условий на входе/выходе
    class ChannelCaseConfig {
    public:
        int nx{80};
        int ny{40};

        double length{6.0};
        double halfHeight{1.0};

        double rho{1.0};
        double mu{0.1};

        double inletVelocity{1.0};
        double outletPressure{0.0};

        InletProfileType inletType{InletProfileType::Constant};
    };

} // namespace cfd3b


#endif //CHANNELCASECONFIG_H
