//
// Created by 6anna on 30.05.2026.
//

#ifndef FLOWFIELDWRITER_H
#define FLOWFIELDWRITER_H


#pragma once

#include <string>

#include "NavierStokesProblem.h"

namespace cfd3b {

    // Записывает распределение скорости и давления
    class FlowFieldWriter {
    public:
        static void writeCellFieldCsv(const NavierStokesProblem& problem,
                                      const std::string& fileName);
    };

} // namespace cfd3b


#endif //FLOWFIELDWRITER_H
