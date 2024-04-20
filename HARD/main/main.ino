#include "pins.h"
#include "drivers/rfid.h"
#include "drivers/lamp.h"
#include "drivers/networktime.h"
//#include "drivers/sd.h"
#include "drivers/analog.h"

#include "parser.h"

#include <string.h>

/*
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
  //lamp::initLamp();
  analog::initAnalog();
  RFID::initRFID();
  //SD::initSd();
  //time::initTime();

  // Done!
  tone(BEEP, 2000, 80);
}

void loop() {
  /// Devices updates... 
  // <- RFID
  const String RFIDPoint = RFID::getPoint();
  // <- NetworkTime
  time::initTime(); // -> auto
  // -> Lamp
  //lamp::setLamp(0,120,0); // <- time
  // <- Analog values
  analog::getAnalog(); // -> auto

  /// Serial communication <-
  String buffer = {};
  while (Serial.available() > 0) {
    buffer += static_cast<char>(Serial.read());
  }
  parseCommand(buffer); // TODO
  //SD::logSd("TESTLOG");

  /// Serial communication ->
  Serial.print("PING: ");
  Serial.println(RFIDPoint);
  // +on analogs:
  // ->  ANALOG:<enum>:<diff value> OR <button status in case button>
  // TODO

  delay(1000);
}
