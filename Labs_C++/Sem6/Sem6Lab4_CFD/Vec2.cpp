//
// Created by 6anna on 15.05.2026.
//

#include "Vec2.h"
#include <cmath>

namespace geom {

    Vec2 vadd(const Vec2& a, const Vec2& b) { return {a[0] + b[0], a[1] + b[1]}; }
    Vec2 vsub(const Vec2& a, const Vec2& b) { return {a[0] - b[0], a[1] - b[1]}; }
    Vec2 vmul(const Vec2& a, double s) { return {a[0] * s, a[1] * s}; }
    double dot(const Vec2& a, const Vec2& b) { return a[0] * b[0] + a[1] * b[1]; }
    double cross(const Vec2& a, const Vec2& b) { return a[0] * b[1] - a[1] * b[0]; }
    double norm(const Vec2& a) { return std::hypot(a[0], a[1]); }
    Vec2 midpoint(const Vec2& a, const Vec2& b) { return {(a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5}; }

}