#include <WiFi.h>        // built in library to connect to WiFi
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "enterprise.h"
#include <ESP32_Servo.h>

void closeWindow();
void openWindow();
int pos = 0, windowPos = 1, phoneState = 3; // 0 means closed, default position of window set to closed
Servo myservo;

BLYNK_WRITE(V2)
{
  phoneState = param.asInt();   // 1 Open, 2 Close, 3 Auto
}

BLYNK_READ(V8) // Raindrop sensor is writing to virtual pin V8
{
  Blynk.virtualWrite(V8, !digitalRead(23));
}

void setup() {
  Serial.begin(9600);
  connectEnterprise(auth, ssid, iden, pass);
  myservo.attach(22, 500, 3000);
  pinMode(23, INPUT_PULLUP); // Raindrop sensor
}

void closeWindow() {
  for (pos = myservo.read(); pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                      // waits 15ms for the servo to reach the position
    }
    windowPos = 0;
    Serial.println("Closing..");
}

void openWindow() {
  for (pos = myservo.read(); pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
    windowPos = 1;
    Serial.println("Opening...");
}

void loop() {
  Blynk.run();
  Serial.println(phoneState);
  int state = !digitalRead(23);
  Blynk.virtualWrite(V8, state);
  if (phoneState==3)
  {
    if (state && windowPos) // WET
      closeWindow();
    else if (!state && !windowPos) // DRY
      openWindow();
  }
  else if (phoneState==1) // window is manually set to open
    openWindow();
  else if (phoneState==2) // window is manually set to close
    closeWindow();
}
