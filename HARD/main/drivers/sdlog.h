#pragma once

#include "../pins.h"
#include "networktime.h"

#include <string.h>
#include <SPI.h>
#include <SD.h>

namespace SDLog {

void initSd() {
    pinMode(SD_CS, OUTPUT);
    time::dbS.print("Initializing SD card...");
    while (!SD.begin(SD_CS))
    {
        delay(10);
    }
    time::dbS.println("initialization done.");
}

void logSd(const String& text) {
    auto myFile = SD.open("WorkSE.txt", FILE_WRITE);

    if (myFile) {
        myFile.println(text);
        myFile.close();
    } else {
        // if the file didn't open, print an error:
        time::dbS.println("error opening test.txt");
    }
}

}