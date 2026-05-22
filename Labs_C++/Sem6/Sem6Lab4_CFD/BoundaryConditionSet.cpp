//
// Created by 6anna on 16.05.2026.
//

#include "BoundaryConditionSet.h"


namespace cfd {

    void BoundaryConditionSet::add(const std::shared_ptr<BoundaryCondition>& bc) {
        conditions[bc->patchName] = bc;
    }

    bool BoundaryConditionSet::has(const std::string& patchName) const {
        return conditions.find(patchName) != conditions.end();
    }

    const BoundaryCondition& BoundaryConditionSet::get(const std::string& patchName) const {
        auto it = conditions.find(patchName);
        if (it == conditions.end()) {
            throw std::runtime_error("Boundary condition not found for patch: " + patchName);
        }
        return *(it->second);
    }

} // namespace cfd