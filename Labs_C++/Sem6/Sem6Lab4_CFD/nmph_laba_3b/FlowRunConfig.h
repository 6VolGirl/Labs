//
// Created by 6anna on 29.05.2026.
//

#ifndef FLOWRUNCONFIG_H
#define FLOWRUNCONFIG_H


#pragma once

#include <string>

namespace cfd3b {

    // Параметры запуска расчёта и сохранения результатов
    // имя кейса, папку вывода и то, какие файлы постобработки нужно сохранять
    class FlowRunConfig {
    public:
        std::string caseName{"channel_flow"};
        std::string outputDirectory{"output"};

        bool saveVelocityField{true};
        bool savePressureField{true};
        bool saveCenterlineProfile{true};
        bool saveCrossSectionProfile{true};
    };

} // namespace cfd3b


#endif //FLOWRUNCONFIG_H
