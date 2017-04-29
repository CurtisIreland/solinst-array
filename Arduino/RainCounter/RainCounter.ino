const byte interruptPin = 3;
const int interval = 500;
volatile unsigned long tiptime = millis();

void setup() {
  Serial.begin(9600);

  // Set up our digital pin as an interrupt
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), count, FALLING);
}

void loop() {
}

void count() {
  // Make sure we don't record bounces
  if ((millis() - tiptime) < interval) {
    return;
  }

  // How long since the last tip?
  unsigned long tipcount = millis() - tiptime;
  tiptime = millis();
  
  // Calculate mm/hr from period between cup tips
  double rainrate = 914400.0 / tipcount;
  
  Serial.print("Cup tip: ");
  Serial.print(tipcount);
  Serial.println("ms");  
  
  Serial.print("Rain rate: ");
  Serial.print(rainrate);
  Serial.println("mm/hr");  
}
