#include <FastLED.h>  // Include the library. Must do this every time we use a library.

#define NUM_LEDS 3    // Number of LEDs in the LED strip
#define DATA_PIN 3    // The digital pin the LED signal line is connected to.


// Define the array of LEDs. Later, leds[0] refers to the 1st LED, leds[1] refers to the 2nd LED, and so on.
CRGB leds[NUM_LEDS];

void setup() {
  // Initialize the LED strip.
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  pinMode(10, INPUT_PULLUP);
}

void loop() {
    int state = digitalRead(10), i;
    if(!state) {
      delay(400);
      leds[0] = CRGB(0, 0, 0);
      leds[2] = CRGB(0, 100, 0);   // Full green.
      FastLED.show();
      delay(4000);
      for(i=0;i<3;i++)
      {
        leds[2] = CRGB(0, 0, 0);
        FastLED.show();
        delay(500);
        leds[2] = CRGB(0, 100, 0);   // Full green.
        FastLED.show();
        delay(1000);
      }
      leds[2] = CRGB(0, 0, 0);
      leds[1] = CRGB(100, 100, 0);   // Full yellow.
      FastLED.show();
      delay(2000);
      leds[1] = CRGB(0, 0, 0);
      leds[0] = CRGB(100, 0, 0);   // Full red.
      FastLED.show();
   }
}
