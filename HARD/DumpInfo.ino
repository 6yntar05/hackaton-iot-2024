#define diod PC13
#define R PB9
#define G PB8
#define B PB1

void setup() {
  pinMode(PC13, OUTPUT);
  pinMode(R, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(R, HIGH); //Подача высоко напряжения на пин
  delay(100); // Задержка на ... мс
  digitalWrite(R, LOW); // Подача низкого напряжения на пин
  delay(100); // задержка на ... мс
}
