//
// Created by 6anna on 15.05.2026.
//

#ifndef VEC2_H
#define VEC2_H

#include <array>

namespace geom {

    using Vec2 = std::array<double, 2>;

    Vec2 vadd(const Vec2& a, const Vec2& b);
    Vec2 vsub(const Vec2& a, const Vec2& b);
    Vec2 vmul(const Vec2& a, double s);

    // Скалярное произведение
    double dot(const Vec2& a, const Vec2& b);

    // a.x * b.y - a.y * b.x
    double cross(const Vec2& a, const Vec2& b);
    double norm(const Vec2& a);
    Vec2 midpoint(const Vec2& a, const Vec2& b);

}


#endif //VEC2_H
