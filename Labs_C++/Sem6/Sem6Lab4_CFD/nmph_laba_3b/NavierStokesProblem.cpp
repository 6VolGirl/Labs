//
// Created by 6anna on 29.05.2026.
//

#include "NavierStokesProblem.h"

namespace cfd3b {

    NavierStokesProblem::NavierStokesProblem(geom::Mesh& mesh_,
                                             double rho_,
                                             double mu_)
        : mesh(&mesh_),
          U(mesh_, "U"),
          Ustar(mesh_, "Ustar"),
          p(mesh_, "p"),
          pCorr(mesh_, "pCorr"),
          rho(rho_),
          mu(mu_) {
        initializeFields();
    }

    std::size_t NavierStokesProblem::cellCount() const {
        if (!mesh) {
            return 0;
        }

        return mesh->cells.size();
    }

    void NavierStokesProblem::initializeFields() {
        U.fill(geom::Vec2{0.0, 0.0});
        Ustar.fill(geom::Vec2{0.0, 0.0});
        p.fill(0.0);
        pCorr.fill(0.0);
    }

} // namespace cfd3b