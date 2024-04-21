#pragma once

#include "../pins.h"
#include <USBComposite.h>
#include <strings.h>


namespace time {

String buf;
String cmp;
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

  Serial.println("iotGEThttp(time)");
  buf = Serial.readString();
  cmp = "";
  for (int i = 0; i < buf.length(); i++){
    if(buf[i] >= 48 && buf[i] <= 58) cmp.concat(buf[i]);
  }
  dbS.println(cmp);
}

}
