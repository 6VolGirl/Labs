//
// Created by 6anna on 29.05.2026.
//

#ifndef PRESSUREBOUNDARYCONDITIONSET_H
#define PRESSUREBOUNDARYCONDITIONSET_H


#pragma once

#include <stdexcept>
#include <string>
#include <unordered_map>

#include "PressureBoundaryCondition.h"

namespace cfd3b {

    // Набор граничных условий для давления.
    class PressureBoundaryConditionSet {
    private:
        std::unordered_map<std::string, PressureBoundaryCondition> conditions_;

    public:
        // Добавить или заменить условие для patch
        void set(const PressureBoundaryCondition& bc);

        // Проверить наличие BC
        bool has(const std::string& patchName) const;

        // Получить BC по имени patch
        const PressureBoundaryCondition& get(const std::string& patchName) const;

        // Очистить все BC
        void clear();

    };

} // namespace cfd3b

#endif //PRESSUREBOUNDARYCONDITIONSET_H
