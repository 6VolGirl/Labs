//
// Created by 6anna on 30.05.2026.
//

#ifndef CHANNELCOMPARISONWRITER_H
#define CHANNELCOMPARISONWRITER_H



#pragma once

#include <string>
#include <vector>

#include "ChannelProfileSample.h"

namespace cfd3b {

    // Записывает численное решение(профиль), точное и ошибку
    class ChannelComparisonWriter {
    public:
        static double  poiseuilleUFromMean(double y, double H, double meanVelocity);

        static void writeProfileComparisonCsv(const std::vector<ChannelProfileSample>& profile,
                                              double H,
                                              double meanVelocity,
                                              const std::string& fileName);
    };

} // namespace cfd3b



#endif //CHANNELCOMPARISONWRITER_H
