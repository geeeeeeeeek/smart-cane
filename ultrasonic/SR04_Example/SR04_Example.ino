//www.elegoo.com
//2016.12.08
#include "SR04.h"
#define TRIG_PIN 12
#define ECHO_PIN 11

#define TRIG_PIN_2 10
#define ECHO_PIN_2 9
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
SR04 sr04_2 = SR04(ECHO_PIN_2,TRIG_PIN_2);
long a;
long b;

void setup() {
   Serial.begin(9600);
   delay(1000);
}

void loop() {
   a=sr04.Distance();
   b=sr04_2.Distance();

   Serial.print(a);
   Serial.print(";");
   Serial.print(b);
   Serial.println("\n");
   delay(500);
}
