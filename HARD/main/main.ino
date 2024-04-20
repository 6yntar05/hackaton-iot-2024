#include "pins.h"
#include "drivers/rfid.h"
#include "drivers/lamp.h"
#include "drivers/networktime.h"
#include "drivers/sdlog.h"
#include "drivers/analog.h"

#include "proto.h"

#include <string.h>
#include <stdlib.h>

/*
Aarch64: WorkSE App
Aarch64: WorkSE Module
Devices:
- SD card
- RGB address leds
- Photoresistor
- Wifi: BOARD API!!!!!!!!!!
- RFID
- Encoders & potentiometers & buttons:
*/

void setup() {
  // General
  Serial.begin(115200);
  SPI.begin();

  // Devices
  lamp::initLamp();
  analog::initAnalog();
  RFID::initRFID();
  SDLog::initSd();
  time::initTime();

  // Done!
  tone(BEEP, 2000, 80);
}

bool auth = false;
uint8_t R=150, G=150, B=30;

void loop() {
  analog::analogData analogs;

  /// Devices updates... 
  const String RFIDPoint = RFID::getPoint();
  time::initTime(); // -> auto
  if (auth)
    lamp::setLamp(R,G,B); // <- time
  else
    lamp::setLamp(0,0,0);

  /// Process
  if (RFIDPoint == "NO") {
    if (auth) { // Change state
      SDLog::logSd("[00:00:00] RFID: NO | Loging out! ");
      tone(BEEP, 360, 80);
    }
    auth = false;
    digitalWrite(GENERIC_LED, LOW);
  } else {
    if (!auth) { // Change state
      SDLog::logSd("[00:00:00] RFID: "+RFIDPoint+" | Authenticated! ");
      tone(BEEP, 2000, 80);
    }
    auth = true;
    digitalWrite(GENERIC_LED, HIGH);
  }

  /// Serial communication <-
  String buffer = {};
  while (Serial.available() > 0) {
    buffer += static_cast<char>(Serial.read());
  }
  proto::parseCommand(buffer);

  for (size_t i = 0; i < 1000; i++) {
    analog::getAnalog(&analogs);
    delay(1);
  }

  /// Serial communication ->
  Serial.println("RFID: "+RFIDPoint);
  Serial.println("MEDIA: NEXT");
  Serial.println("BRIGHT: "+String(analogs.bright));
  Serial.println("TIME: 00:00:00");
  Serial.println("LAMP: "+String(R)+" "+String(G)+" "+String(B));
}
