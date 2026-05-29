//
// Created by 6anna on 16.05.2026.
//

#ifndef BOUNDARYCONDITIONSET_H
#define BOUNDARYCONDITIONSET_H



#include "BoundaryCondition.h"

#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>

namespace cfd {
    // BoundaryConditionSet — набор граничных условий для разных boundary patch-ей.
    // Хранит отображение "имя patch-а -> граничное условие".
    // Используется сборщиком уравнения для поиска нужного условия
    // по имени patchName у граничной грани.
    class BoundaryConditionSet {
    public:
        std::unordered_map<std::string, std::shared_ptr<BoundaryCondition>> conditions;

        void add(const std::shared_ptr<BoundaryCondition>& bc);
        bool has(const std::string& patchName) const;
        const BoundaryCondition& get(const std::string& patchName) const;
    };

} // namespace cfd


#endif //BOUNDARYCONDITIONSET_H
