#define diod PC13
#define R PB9
#define G PB8
#define B PB1

void setup() {
  pinMode(PC13, OUTPUT);
  pinMode(R, OUTPUT);
}

void loop() {
  digitalWrite(R, HIGH);
  delay(100);
  digitalWrite(R, LOW);
  delay(100);
}
