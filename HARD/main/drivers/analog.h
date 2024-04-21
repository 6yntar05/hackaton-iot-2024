#pragma once

#include "../pins.h"
#include "networktime.h"

namespace analog {

#define CLK ENC_C
#define DT ENC_A
#define SW ENC_B
int value = 0;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;

bool isButtonPressed = false;
bool isButtonReleased = false;
unsigned long buttonPressTime = 0;
unsigned long debounceDelay = 50; // Задержка для подавления дребезга
//int buttonOld = LOW;
//int buttonBounceRatio = 100;

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
    pinMode(POT_BRIGHT, INPUT);
}

void getAnalog(analogData* ret) {
    ret->button = digitalRead(BUTTON);
    bool buttonState = digitalRead(BUTTON);
    if (buttonState == HIGH && !isButtonPressed) {
        isButtonPressed = true;
        //time::dbS.println("MEDIA: TOGGLE");
        buttonPressTime = millis();
    }
    if (isButtonPressed && millis() - buttonPressTime >= debounceDelay) {
        if (buttonState == LOW && !isButtonReleased) {
            isButtonReleased = true;
        } else if (buttonState == HIGH && isButtonReleased) {
            time::dbS.println("MEDIA: NEXT");
            isButtonReleased = false;
        }
    }

    // Сброс состояний кнопки после нажатия и отпускания
    if (buttonState == LOW && isButtonReleased) {
        isButtonPressed = false;
        isButtonReleased = false;
    }
    //if (buttonOld != ret->button) {
    //    if (buttonBounceRatio > 0) {
    //        buttonBounceRatio--;
    //    } else {
    //        time::dbS.println("MEDIA: TOGGLE");
    //        buttonOld = ret->button;
    //        buttonBounceRatio = 100;
    //    }
    //} else {
    //    buttonBounceRatio = 100;
    //}

    n = digitalRead(ENC_A);
    if ((encoder0PinALast == LOW) && (n == HIGH)) {
        if (digitalRead(ENC_C) == LOW) {
        encoder0Pos-=2;
        } else {
        encoder0Pos+=2;
        }
        time::dbS.println("VOLUME: "+String(encoder0Pos));
    }
    encoder0PinALast = n;
    ret->encoder = encoder0Pos;

    ret->bright = analogRead(POT_BRIGHT);
}

}