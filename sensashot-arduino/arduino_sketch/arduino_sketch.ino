// Arduino Pulse Controller
// Sends 200ms digital pulses on pins 3, 5, 6, and 9
// Controlled via serial commands from Python

const int LED_PINS[] = {3, 5, 6, 9};
const int NUM_PINS = 4;
const int PULSE_DURATION = 200; // 200ms pulse duration

void setup() {
  Serial.begin(9600);

  // Initialize output pins
  for (int i = 0; i < NUM_PINS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }

  Serial.println("Arduino Pulse Controller Ready");
  Serial.println("Pins configured: 3, 5, 6, 9");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("PULSE_")) {
      int pin = command.substring(6).toInt();
      sendPulse(pin);
    }
  }
}

void sendPulse(int pin) {
  bool validPin = false;

  // Check if pin is valid
  for (int i = 0; i < NUM_PINS; i++) {
    if (LED_PINS[i] == pin) {
      validPin = true;
      break;
    }
  }

  if (validPin) {
    digitalWrite(pin, HIGH);
    delay(PULSE_DURATION);
    digitalWrite(pin, LOW);

    Serial.print("Pulse sent on pin ");
    Serial.println(pin);
  } else {
    Serial.print("Invalid pin: ");
    Serial.println(pin);
  }
}