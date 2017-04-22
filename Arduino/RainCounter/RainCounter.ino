const byte interruptPin = 3;
volatile unsigned long tiptime = millis();
volatile unsigned long tipcount = 0;

void setup() {
  Serial.begin(9600);

  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), count, FALLING);
}

void loop() {
}

void count() {
  tipcount = millis() - tiptime;
  tiptime = millis();
  delay(500);
  
  double rainrate = 914400.0 / tipcount;
  
  Serial.print("Cup tip: ");
  Serial.print(tipcount);
  Serial.println("ms");  
  
  Serial.print("Rain rate: ");
  Serial.print(rainrate);
  Serial.println("mm/hr");  
}
