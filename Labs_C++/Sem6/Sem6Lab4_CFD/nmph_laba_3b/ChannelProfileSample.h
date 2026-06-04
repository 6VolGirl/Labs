//
// Created by 6anna on 30.05.2026.
//

#ifndef CHANNELPROFILESAMPLE_H
#define CHANNELPROFILESAMPLE_H


#pragma once

namespace cfd3b {
    struct ChannelProfileSample {
        double x{};
        double y{};
        double u{};
        double v{};
        double speed{};
        double p{};
        double pTheory{};
        double uTheory{};
    };
}

#endif //CHANNELPROFILESAMPLE_H
