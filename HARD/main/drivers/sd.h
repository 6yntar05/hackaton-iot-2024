#pragma once

#include "../pins.h"

#include <STM32SD.h>

#include <SPI.h>

namespace SD {

void initSd() {
    pinMode(SD_CS, OUTPUT);
    Serial.print("Initializing SD card...");
    while (!SD.begin(SD_CS))
    {
        delay(10);
    }
    Serial.println("initialization done.");
}

void logSd() {
    myFile = SD.open("test.txt", FILE_WRITE);

    if (myFile) {
        Serial.print("Writing to test.txt...");
        myFile.println("testing 1, 2, 3.");
        // close the file:
        myFile.close();
        Serial.println("done.");
    } else {
        // if the file didn't open, print an error:
        Serial.println("error opening test.txt");
    }
}

}