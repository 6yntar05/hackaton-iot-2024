#pragma once

#include "../pins.h"
#include <USBComposite.h>
#include <strings.h>

#define MMOD 60
#define HMOD 60*60
#define DMOD 24*60*60
#define seconds() (millis()/1000)

namespace time {

String buf;
String cmp;
int hours;
int minutes;
int seconds;
int boottime;
long stime, otime;
USBCompositeSerial dbS;

void initTime() {
  delay(500);
  Serial.begin(115200);
  dbS.begin();
  
  while (!USBComposite);
  delay(1000);
  dbS.println("USB connected");
  tone(BEEP, 4000, 10);

  delay(10000);

  cmp = "OK\r\n";

  Serial.println("iotConnectWiFi(Hackaton,123456789)");
  dbS.println("Connecting");
  tone(BEEP, 4000, 10);
  delay(100);
  tone(BEEP, 4000, 10);

  while (!Serial.available());
  buf = Serial.readString();

  if (cmp == buf){ 
    dbS.println("Connect command executed successfully!");
    tone(BEEP, 2000, 10);
  } else{ 
    dbS.println("Connect command failed to execute :(");
    return;
  }

  Serial.println("iotServerParameters(172.16.12.46,5000)");
  buf = Serial.readString();
  if (cmp == buf){ 
    dbS.println("Set Server command executed successfully!");
    tone(BEEP, 2000, 10);
  } else {
    dbS.println("Set Server command failed to execute :(");
    return;
  }
  cmp = "";
  while(cmp.length() < 1){
    Serial.println("iotGEThttp(time)");
    while(!Serial.available());
    buf = Serial.readString();
    cmp = "";
    for (int i = 0; i < buf.length(); i++){
      if(buf[i] >= 48 && buf[i] <= 58) cmp.concat(buf[i]);
    }
  }
  cmp = cmp.substring(1,cmp.length());
  buf = cmp.substring(0,2);
  cmp = cmp.substring(3,5);
  hours = buf.toInt();
  minutes = cmp.toInt();
  boottime=seconds();
  otime = HMOD*hours+MMOD*minutes+seconds();
  dbS.println(hours);
  dbS.println(minutes);
  dbS.println(otime);
}
void refreshTime(){
  otime = HMOD*hours+MMOD*minutes+seconds();
  cmp=String(otime);
}
}
