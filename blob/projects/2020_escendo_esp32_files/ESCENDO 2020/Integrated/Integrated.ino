#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <BlynkSimpleEsp32.h>  
#include "enterprise.h"
#include <ArduinoJson.h>
#include <ESP32_Servo.h>

float humidity;
// Set password to "" for open networks.
        char auth[] = "7FpYmGcnOoDwaleRDg73iUT78FlCe_8p";
        char ssid[] = "NTUSECURE";
        char iden[] = "STUDENT\\";
        char pass[] = "";
 
const String endpoint = "https://api.data.gov.sg/v1/environment/relative-humidity";

int buttonState; 

void closeWindow();
void openWindow();
int pos = 0, windowPos = 1, phoneState = 2; // 0 means closed, default position of window set to closed
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
//  myservo.attach(servoPin,500,3000);
//  myservo.write(5);
  pinMode(23, INPUT_PULLUP); // Raindrop sensor
  myservo.attach(22, 500, 3000);
  connectEnterprise(auth,ssid,iden, pass);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 }

void closeWindow() {
  for (pos = myservo.read(); pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                      // waits 15ms for the servo to reach the position
    }
    windowPos = 0;
}

void openWindow() {
  for (pos = myservo.read(); pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
    windowPos = 1;
}
 
BLYNK_WRITE(V10){
  buttonState = param.asInt();
}

void loop() {
  delay(5);
 
if(buttonState == HIGH){ 
  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
 
    HTTPClient http;
 
    http.begin(endpoint ); //Specify the URL
    int httpCode = http.GET();  //Make the request
 
    if (httpCode > 0) { //Check for the returning code
        //DynamicJsonDocument doc(1024);
          String payload = http.getString(); http.end();
        //Serial.println(httpCode);
        //Serial.println(payload); 
          const size_t capacity = JSON_ARRAY_SIZE(1) + 2*JSON_ARRAY_SIZE(17) + JSON_OBJECT_SIZE(1) + 35*JSON_OBJECT_SIZE(2) + 2*JSON_OBJECT_SIZE(3) + 17*JSON_OBJECT_SIZE(4) + 1920;
          DynamicJsonDocument doc(capacity);
//Serial.println(sizeof(payload)*payload.length());
//char json[sizeof(payload) * payload.length()];
//payload.toCharArray(json, sizeof(payload)* payload.length()); 

//deserializeJson(doc, json);
          deserializeJson(doc, payload);  
          JsonObject items = doc["items"][0];

          JsonArray readings = items["readings"];

          const char* NTU_station_id = "S44";
          float threshold = 90;
              for (JsonObject r: readings){
                  const char* station_id = r["station_id"];
                  if (strcmp(station_id, NTU_station_id) == 0){
                      humidity = r["value"];
                      Serial.println(humidity);
           
                  if (humidity > threshold){
                      String c = "Weather is humid,might rain soon";
                      Serial.println(c);
                      Blynk.notify(c);
                      Blynk.run();
                   
                      }
                  else{
                    String c = "Today's humidity is optimal";
                    Blynk.notify(c);
                    Blynk.run();
                    }
                  }
              }  
    }     
  }    
      else {
            Serial.println("Error on HTTP request");
            }

}
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
  Blynk.run();
  delay(300);
}
