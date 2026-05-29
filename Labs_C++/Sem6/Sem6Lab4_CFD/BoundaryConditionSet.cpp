//
// Created by 6anna on 16.05.2026.
//

#include "BoundaryConditionSet.h"


namespace cfd {

    void BoundaryConditionSet::add(const std::shared_ptr<BoundaryCondition>& bc) {
        if (!bc) {
            throw std::runtime_error("Cannot add null boundary condition");
        }
        if (conditions.contains(bc->patchName)) {
            throw std::runtime_error("Boundary condition already exists for patch: " + bc->patchName);
        }
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