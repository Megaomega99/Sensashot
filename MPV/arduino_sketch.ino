/*
  Arduino Pulse Controller
  Receives commands from Python script and sends 200ms pulses on pins 3,5,6,9
*/

const int OUTPUT_PINS[] = {3, 5, 6, 9};
const int PULSE_DURATION = 200; // 200 milliseconds

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set pins as outputs
  for (int i = 0; i < 4; i++) {
    pinMode(OUTPUT_PINS[i], OUTPUT);
    digitalWrite(OUTPUT_PINS[i], LOW);
  }

  Serial.println("Arduino Pulse Controller Ready");
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse command
    if (command.startsWith("PULSE_")) {
      int pin = command.substring(6).toInt();

      // Validate pin and send pulse
      if (isValidPin(pin)) {
        sendPulse(pin);
        Serial.println("Pulse sent on pin " + String(pin));
      } else {
        Serial.println("Invalid pin: " + String(pin));
      }
    } else {
      Serial.println("Unknown command: " + command);
    }
  }
}

bool isValidPin(int pin) {
  for (int i = 0; i < 4; i++) {
    if (OUTPUT_PINS[i] == pin) {
      return true;
    }
  }
  return false;
}

void sendPulse(int pin) {
  digitalWrite(pin, HIGH);
  delay(PULSE_DURATION);
  digitalWrite(pin, LOW);
}