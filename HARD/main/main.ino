#include "pins.h"
#include "drivers/rfid.h"

#include <string.h>

/*
Devices:
- SD card:

- RGB address leds:

- Photoresistor:

- Wifi module (NRF24L01) (networktime):

- RFID:

- Encoders & potentiometers & buttons:
*/

void setup() {
  // General
  pinMode(GENERIC_LED, OUTPUT);
  Serial.begin(115200);
  SPI.begin();

  // Devices
  RFID::initRFID();
}

static char incomingByte = 0;
void loop() {
  /// Devices updates... 
  // <- RFID
  const String RFIDPoint = RFID::getPoint();
  // <- NetworkTime
  // -> Lamp
  // <- Analog values

  /// Serial communication <-
  String buffer = {};
  while (Serial.available() > 0) {
    incomingByte = Serial.read();
    buffer += incomingByte;
  }
  Serial.println(buffer);
  // Parse commands ...
  //  -> TODO
  //  -> Log to SDcard

  /// Serial communication ->
  Serial.print("PING: ");
  Serial.println(RFIDPoint);
  // +on analogs:
  // ->  ANALOG:<enum>:<diff value> OR <button status in case button>
  // TODO

  delay(1000);
}
