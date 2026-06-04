//
// Created by 6anna on 29.05.2026.
//

#include "PressureBoundaryConditionSet.h"


namespace cfd3b {

    void PressureBoundaryConditionSet::set(const PressureBoundaryCondition& bc) {
        conditions_[bc.patchName] = bc;
    }

    bool PressureBoundaryConditionSet::has(const std::string& patchName) const {
        return conditions_.find(patchName) != conditions_.end();
    }

    const PressureBoundaryCondition& PressureBoundaryConditionSet::get(const std::string& patchName) const {
        auto it = conditions_.find(patchName);
        if (it == conditions_.end()) {
            throw std::runtime_error("Missing pressure BC for patch: " + patchName);
        }
        return it->second;
    }

    void PressureBoundaryConditionSet::clear() {
        conditions_.clear();
    }

} // namespace cfd3b