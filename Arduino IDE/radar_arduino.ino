 
// This code should be paste on Arduino IDE siftwere 


#include <Servo.h>

Servo radarServo;

// Pin connections
const int trigPin = 10;
const int echoPin = 11;
const int servoPin = 12;

const int greenLED = 7;
const int redLED = 6;

long duration;
int distance;

int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return 0;
  }

  return duration * 0.0343 / 2;
}

void checkObject(int d) {
  if (d > 0 && d <= 30) {
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
  } else {
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, HIGH);
  }
}

void scan(int angle) {
  radarServo.write(angle);
  delay(25);

  distance = getDistance();
  checkObject(distance);

 
  Serial.print(angle);
  Serial.print(",");
  Serial.println(distance);
}

void setup() {
  radarServo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, HIGH);

  Serial.begin(9600);
}

void loop() {
  for (int angle = 0; angle <= 180; angle++) {
    scan(angle);
  }

  for (int angle = 180; angle >= 0; angle--) {
    scan(angle);
  }
}
