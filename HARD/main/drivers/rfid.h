#pragma once

#include "../pins.h"

#include "SPI.h"
#include "MFRC522.h" 
#include <string.h>

namespace RFID {

#define RST_PIN  9 // RES pin
#define SS_PIN  10 // SDA (SS) pin

MFRC522 mfrc522(SS_PIN, RST_PIN); // создание объекта mfrc522

inline void initRFID() {
    mfrc522.PCD_Init();
    delay(4);
    mfrc522.PCD_DumpVersionToSerial();
    Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

inline String getPoint() {
    // сброс цикла, если на считывателе нет карты
    if ( ! mfrc522.PICC_IsNewCardPresent()) {
        return;
    }

    if ( ! mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    // вывод информации о карте на монитор порта
    mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
    return "FFFFFF";
}

}