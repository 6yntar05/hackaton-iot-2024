#pragma once

#include "../pins.h"

#include "SPI.h"
#include "MFRC522.h" 
#include <string.h>

namespace RFID {

MFRC522 mfrc522(RFID_SS, RFID_RST); // создание объекта mfrc522

inline void initRFID() {
    mfrc522.PCD_Init();
    delay(4);
    mfrc522.PCD_DumpVersionToSerial();
    Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

inline String getPoint() {
    if ( mfrc522.PICC_IsNewCardPresent() ) {
        mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid));
        mfrc522.PICC_HaltA();
        String buffer = "1A737580"; // Temporary
        for (size_t i = 0; i < mfrc522.uid.size; i++){
            buffer += static_cast<char>(mfrc522.uid.uidByte[i]);
        }
        return buffer;
    }
    if ( ! mfrc522.PICC_ReadCardSerial()) {
        digitalWrite(GENERIC_LED, LOW);
        return "NO";
    }
}

}