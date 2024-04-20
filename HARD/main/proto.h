#pragma once

#include "drivers/sdlog.h"

#include <string.h>

namespace proto {

void parseCommand(const String& command) {
    // BEEP: 1000
    
    // LOG: text
    auto logMsg = command;
    SDLog::logSd("[00:00:00] "+logMsg);
}

}