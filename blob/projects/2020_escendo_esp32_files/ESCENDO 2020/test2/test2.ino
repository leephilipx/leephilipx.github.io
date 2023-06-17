/*********
 Rui Santos
 Complete project details at http://randomnerdtutorials.com 
*********/

#include <WiFi.h>        // built in library to connect to WiFi
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "enterprise.h"
#include <ESP32_Servo.h>

// Motor A
int motor1Pin1 = 18; 
int motor1Pin2 = 19; 
int enable1Pin = 4; 
// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

int rainState = 0, phoneState = 2; // 0 means closed

BLYNK_WRITE(V3) // Writing to virtual pin 3
{
  phoneState = param.asInt();   // 1 Open, 2 Close, 3 Auto
}

void setup() {
  connectEnterprise(auth, ssid, iden, pass);
  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(22, INPUT_PULLUP); // Open switch
  pinMode(23, INPUT_PULLUP); // Close switch
  pinMode(21, INPUT_PULLUP); // Raindrop sensor
  pinMode(2, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(pwmChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);
  Serial.begin(115200);
  // testing
  Serial.print("Testing DC Motor...");
  
}

void loop() {
  Blynk.run();
  while (dutyCycle <= 255){
    Blynk.run();
  ledcWrite(pwmChannel, dutyCycle);  
  // Serial.print("Forward with duty cycle: ");
  // Serial.println(dutyCycle);
  dutyCycle = dutyCycle + 5;
  }
  dutyCycle = 200;
  
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  
  rainState = !digitalRead(21);
  Serial.println(rainState);
  digitalWrite(2, rainState);
  
//  if (phoneState==3)
//  {
//    if (rainState) // WET
//    {
//      while(digitalRead(23))
//      {
//        Blynk.run();
//        digitalWrite(motor1Pin1, HIGH);
//        digitalWrite(motor1Pin2, LOW);
//        Serial.println('a');
//      }
//    }
//    else if (!rainState) // DRY
//    {
//      while(digitalRead(22))
//      {
//        Blynk.run();
//        digitalWrite(motor1Pin1, LOW);
//        digitalWrite(motor1Pin2, HIGH);
//        Serial.println('b');
//      }
//    }
//  }
  if (phoneState==1) // window is manually set to open
    {
      while(digitalRead(22))
      {
        Blynk.run();
        digitalWrite(motor1Pin1, HIGH);
        digitalWrite(motor1Pin2, LOW);
        Serial.println('c');
      }
    }
  else if (phoneState==2) // window is manually set to close
    {
      while(digitalRead(23))
      {
        Blynk.run();
        digitalWrite(motor1Pin1, LOW);
        digitalWrite(motor1Pin2, HIGH);
        Serial.println('d');
      }
    }
}
