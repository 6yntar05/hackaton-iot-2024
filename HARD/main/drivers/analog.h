#pragma once

#include "../pins.h"

namespace analog {

#define CLK ENC_C
#define DT ENC_A
#define SW ENC_B
int value = 0;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;

int buttonOld = LOW;
int buttonBounceRatio = 100;

struct analogData {
    bool button = false;
    float bright = 50.0;
    int encoder = 0;
};

void initAnalog() {
    pinMode(GENERIC_LED, OUTPUT);
    pinMode(ENC_A, INPUT);
    pinMode(ENC_B, INPUT);
    pinMode(ENC_C, INPUT);
    pinMode(BUTTON, INPUT);
}

void getAnalog(analogData* ret) {
    ret->button = digitalRead(BUTTON);
    if (buttonOld != ret->button) {
        if (buttonBounceRatio > 0) {
            buttonBounceRatio--;
            //Serial.println("MEDIA: BOUNCE");
        } else {
            Serial.println("MEDIA: TOGGLE");
            buttonOld = ret->button;
            buttonBounceRatio = 100;
        }
    } else {
        buttonBounceRatio = 100;
    }

    n = digitalRead(ENC_A);
    if ((encoder0PinALast == LOW) && (n == HIGH)) {
        if (digitalRead(ENC_C) == LOW) {
        encoder0Pos--;
        } else {
        encoder0Pos++;
        }
        Serial.println("VOLUME: "+String(encoder0Pos));
    }
    encoder0PinALast = n;
    ret->encoder = encoder0Pos;

    ret->bright = analogRead(POT_BRIGHT);

}

}