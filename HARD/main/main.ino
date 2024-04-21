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

using namespace time;

void setup() {
  // General
  time::initTime();
  SPI.begin();

  // Devices
  lamp::initLamp();
  analog::initAnalog();
  RFID::initRFID();
  SDLog::initSd();

  pinMode(BUTTON, INPUT_PULLDOWN);
  // Done!
  tone(BEEP, 2000, 80);

}

bool auth = false;
uint8_t R=150, G=150, B=30;
analog::analogData analogs;

// timers
constexpr int notifyTimerReference = 100;
static int notifyTimer = notifyTimerReference;
static uint32_t utimeYes = 0;

constexpr int sleepTimerReference = 100;
static int sleepTimer = sleepTimerReference;
static uint32_t utimeNo = 0;

void loop() {
  /// Timers updates...

  if (auth) {
    utimeYes++;
    dbS.println("LOGTIME: "+String(utimeYes));
  } else {
    utimeNo++;
    dbS.println("UNLOGTIME: "+String(utimeNo));
  }

  /// Devices updates... 
  const String RFIDPoint = RFID::getPoint();
  if (auth && (analogs.bright > 100)) {
    float mul = (float)analogs.bright / 4096.0;
    lamp::setLamp(R*mul,G*mul,B*mul); // <- time
  } else {
    lamp::setLamp(0,0,0);
  }

  /// Process
  if (RFIDPoint == "NO") {
    if (auth) { // Change state
      tone(BEEP, 360, 80);
      SDLog::logSd("["+time::cmp+"] RFID: NO | Loging out! | Session utime: "+String(utimeYes));
      notifyTimer = notifyTimerReference;
      utimeYes = 0;
    }
    auth = false;
    digitalWrite(GENERIC_LED, LOW);
  } else {
    if (!auth) { // Change state
      SDLog::logSd("["+time::cmp+"] RFID: "+RFIDPoint+" | Authenticated! | Session utime: "+String(utimeNo));
      tone(BEEP, 2000, 80);
      sleepTimer = sleepTimerReference;
      utimeNo = 0;
    }
    auth = true;
    digitalWrite(GENERIC_LED, HIGH);
  }

  /// Serial communication <-
  String buffer = {};
  while (dbS.available() > 0) {
    buffer += static_cast<char>(dbS.read());
  }
  proto::parseCommand(buffer);

  for (size_t i = 0; i < 1000; i++) {
    analog::getAnalog(&analogs);

    int btn_time = 0;
    int btn_penalty = 0;
    if(digitalRead(BUTTON)){
      btn_penalty = 50;
    }
    while(--btn_penalty > 0){
      if(digitalRead(BUTTON)) btn_penalty = 50;
      delay(1);
      btn_time++;
      if(btn_time > 5000) break;
    }
    if(btn_time > 1000) {
      dbS.println("MEDIA: NEXT");
    }else if(btn_time > 0){
      dbS.println("MEDIA: PAUSE");
    }
    
    delay(1);
  }

  /// Serial communication ->
  dbS.println("RFID: "+RFIDPoint);
  dbS.println("TIME: "+time::cmp);
  dbS.println("LAMP: "+String(R)+" "+String(G)+" "+String(B));
  dbS.println("BRIGHT: "+String(analogs.bright/4096.0*100));

  if (auth) {
    if (notifyTimer < 1) {
      dbS.println("NOTIFY");
      notifyTimer = notifyTimerReference;
    }
    notifyTimer--;
  }
  if (!auth) {
    if (sleepTimer < 1) {
      dbS.println("SLEEP");
      sleepTimer = sleepTimerReference;
    }
    sleepTimer--;
  }
}
