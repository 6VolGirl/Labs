//
// Created by 6anna on 29.05.2026.
//

#ifndef VELOCITYBOUNDARYCONDITIONSET_H
#define VELOCITYBOUNDARYCONDITIONSET_H


#pragma once

#include <stdexcept>
#include <string>
#include <unordered_map>

#include "VelocityBoundaryCondition.h"

namespace cfd3b {

    // Набор граничных условий для скорости
    // Хранит BC по имени patch, например:
    // left, right, top, bottom.
    class VelocityBoundaryConditionSet {
    private:
        std::unordered_map<std::string, VelocityBoundaryCondition> conditions_;

    public:

        void set(const VelocityBoundaryCondition& bc);
        // Проверить, задано ли условие для patch
        bool has(const std::string& patchName) const;
        const VelocityBoundaryCondition& get(const std::string& patchName) const;

        void clear();

   };

} // namespace cfd3b



#endif //VELOCITYBOUNDARYCONDITIONSET_H
