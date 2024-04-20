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
    // сброс цикла, если на считывателе нет карты
    if ( ! mfrc522.PICC_IsNewCardPresent()) {
        return "ERR";
    }

    if ( ! mfrc522.PICC_ReadCardSerial()) {
        return "ERR";
    }

    // вывод информации о карте на монитор порта
    mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
    digitalWrite(GENERIC_LED, HIGH);
    return "FFFFFF";
}

}