#include <WiFi.h> //built in library to connect to WiFi
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "enterprise.h"
#include <FastLED.h>
#define COLOR_ORDER GRB
#define CHIPSET     WS2811
#define BRIGHTNESS  200
#define FRAMES_PER_SECOND 60
#define COOLING  55
#define SPARKING 120
#define DATA_PIN 23 //data pin 23
#define NUM_LEDS 88// no. of LED is 1
#define CLOCK_PIN 13
char auth[] = "6vAD99x9C2NIZx8XVqFgozRGPs1vGCem";
char ssid[] = "NTUSECURE";
char iden[] = "STUDENT\\euge0026";
char pass[] = "Yugioh8307@";
// Define the array of leds
CRGB leds[NUM_LEDS];
bool boOnOffButton1;
bool boOnOffButton2;
bool gReverseDirection = false;

BLYNK_WRITE(V1)
{
  boOnOffButton1 = param.asInt();   // Read from virtual pin V1 as integer 
  Serial.println((bool)boOnOffButton1);
}

BLYNK_WRITE(V2)
{
  boOnOffButton2 = param.asInt();   // Read from virtual pin V1 as integer 
  Serial.println((bool)boOnOffButton2);
}

void setup() 
{ 
  Serial.begin(57600);
  Serial.println("resetting");
  LEDS.addLeds<WS2812,DATA_PIN,RGB>(leds,NUM_LEDS);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  FastLED.addLeds<CHIPSET, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  LEDS.setBrightness(84);
  FastLED.setBrightness( BRIGHTNESS );
  connectEnterprise(auth, ssid, iden, pass);
}

void fadeall() { for(int i = 0; i < NUM_LEDS; i++) { leds[i].nscale8(250); } }

void loop() 
{ 
  Blynk.run();
  if (boOnOffButton1)
  {
    static uint8_t hue = 0;
    Serial.print("x");
    for(int i = 0; i < NUM_LEDS; i++) 
    {
    leds[i] = CHSV(hue++, 255, 255);
    // Show the leds
    FastLED.show(); 
    // now that we've shown the leds, reset the i'th led to black
    // leds[i] = CRGB::Black;
    fadeall();
    // Wait a little bit before we loop around and do it again
    delay(0);
     }
    Serial.print("x");
    // Now go in the other direction.  
    for(int i = (NUM_LEDS)-1; i >= 0; i--)
    {
    // Set the i'th led to red 
    leds[i] = CHSV(hue++, 255, 255);
    // Show the leds
    FastLED.show();
    // now that we've shown the leds, reset the i'th led to black
    // leds[i] = CRGB::Black;
    fadeall();
    // Wait a little bit before we loop around and do it again
    delay(10);
    }
  }
  else if (boOnOffButton2)
  {
    Fire2012(); // run simulation frame
    FastLED.show(); // display this frame
    FastLED.delay(1000 / FRAMES_PER_SECOND);
  }
  else
    off();
}
void off()
{
  for(int i = (NUM_LEDS)-1; i >= 0; i--) {
      leds[i] = CRGB::Black;
      FastLED.show();
    }
}

void Fire2012()
{
// Array of temperature readings at each simulation cell
  static byte heat[NUM_LEDS];

  // Step 1.  Cool down every cell a little
    for( int i = 0; i < NUM_LEDS; i++) {
      heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / NUM_LEDS) + 2));
    }
  
    // Step 2.  Heat from each cell drifts 'up' and diffuses a little
    for( int k= NUM_LEDS - 1; k >= 2; k--) {
      heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
    }
    
    // Step 3.  Randomly ignite new 'sparks' of heat near the bottom
    if( random8() < SPARKING ) {
      int y = random8(7);
      heat[y] = qadd8( heat[y], random8(160,255) );
    }

    // Step 4.  Map from heat cells to LED colors
    for( int j = 0; j < NUM_LEDS; j++) {
      CRGB color = HeatColor( heat[j]);
      int pixelnumber;
      if( gReverseDirection ) {
        pixelnumber = (NUM_LEDS-1) - j;
      } else {
        pixelnumber = j;
      }
      leds[pixelnumber] = color;
    }
}
