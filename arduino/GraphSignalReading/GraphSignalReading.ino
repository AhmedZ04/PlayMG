void setup() {
  Serial.begin(9600);

}

void loop() {
  int analogOutput0 = analogRead(A0);
  Serial.println(analogOutput0);

}
