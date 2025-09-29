#include <Arduino.h>

const int PINS[] = {3, 5, 6, 9};
const int PULSE_DURATION = 200;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(PINS[i], OUTPUT);
    digitalWrite(PINS[i], LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command >= '1' && command <= '4') {
      int pinIndex = command - '1';

      digitalWrite(PINS[pinIndex], HIGH);
      delay(PULSE_DURATION);
      digitalWrite(PINS[pinIndex], LOW);

      Serial.print("Pulso enviado en pin ");
      Serial.println(PINS[pinIndex]);
    }
  }
}