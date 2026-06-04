//
// Created by 6anna on 29.05.2026.
//

#include "VelocityBoundaryConditionSet.h"

#include "VelocityBoundaryConditionSet.h"

namespace cfd3b {

    void VelocityBoundaryConditionSet::set(const VelocityBoundaryCondition& bc) {
        conditions_[bc.patchName] = bc;
    }

    bool VelocityBoundaryConditionSet::has(const std::string& patchName) const {
        return conditions_.find(patchName) != conditions_.end();
    }

    const VelocityBoundaryCondition& VelocityBoundaryConditionSet::get(const std::string& patchName) const {
        auto it = conditions_.find(patchName);
        if (it == conditions_.end()) {
            throw std::runtime_error("Missing velocity BC for patch: " + patchName);
        }
        return it->second;
    }

    void VelocityBoundaryConditionSet::clear() {
        conditions_.clear();
    }

} // namespace cfd3b