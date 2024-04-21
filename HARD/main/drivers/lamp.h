#pragma once

#include "../pins.h"
#include "networktime.h"

#include <bluepill_ws2812.h>
bluepill_neopixel PIX;       // a string of pixels
#define NUM_PIXELS 4     //   number of pixels in the string
pixel string[NUM_PIXELS]; //   rgb data buffer
#define string_port GPIOA //   pin string is connected to
#define string_pin  0

namespace lamp {

static uint8_t Ro=0, Go=0, Bo=0;

void initLamp() {
    PIX.begin(string_port, string_pin);
}

void setLamp(uint8_t R, uint8_t G, uint8_t B) {
    for (uint8_t i=0; i < NUM_PIXELS; i++) {
        string[i].rgb.r = G;
        string[i].rgb.g = R;
        string[i].rgb.b = B;
    } 
    
    PIX.paint( string[0].bytes, NUM_PIXELS, string_port, string_pin );
}

}