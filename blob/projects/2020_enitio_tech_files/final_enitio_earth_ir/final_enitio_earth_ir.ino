#include <IRremote.h>

const int RECV_PIN = 4;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
    Serial.begin(9600);
    irrecv.enableIRIn();
    irrecv.blink13(true);
}

void loop() {
    pinMode(2, OUTPUT);
    digitalWrite(2, LOW);
    if (irrecv.decode(&results)) {
        Serial.println(results.value, HEX);
        irrecv.resume();
        if (results.value == 3960362407 || results.value == 235820455 || results.value == 4294967295) // HEX: EC0E55A7, E0E55A7, FFFFFFFF
            digitalWrite(2, HIGH);
    }
    
    //else
      //  Serial.println("null");
}

