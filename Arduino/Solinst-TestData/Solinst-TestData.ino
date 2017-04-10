void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();

    Serial.println("22.1,62.8,21.6,48.3,18.5,10.563,2.354");
  }
  delay(500);
}
