//
// Created by 6anna on 30.05.2026.
//

#ifndef CHANNELPROFILEEXTRACTO_H
#define CHANNELPROFILEEXTRACTO_H


#pragma once

#include <vector>

#include "NavierStokesProblem.h"
#include "ChannelProfileSample.h"

namespace cfd3b {
    // Берёт одно сечение канала и проверяет форму профиля
    class ChannelProfileExtractor {
    public:
        static std::vector<ChannelProfileSample>
        extractVerticalLine(const NavierStokesProblem& problem, double xSection);
    };

} // namespace cfd3b



#endif //CHANNELPROFILEEXTRACTO_H
