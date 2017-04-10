#include <SDI12.h>
#include <DHT.h>
#include <SHT1x.h>

#define RAINPIN 3         // Interrupt pin for Rain Gauge
#define DHTPIN  4         // Data pin for the DHT
#define SHTDATA 6         // Soil sensor data pin (blue)
#define SHTCLK  5         // Soil sensor clock pin (yellow)
#define SDIPIN  8         // Data pin for the Solinst

#define DHTTYPE DHT22     // DHT 22  (AM2302), AM2321

DHT dht(DHTPIN, DHTTYPE);
SHT1x sht1x(SHTDATA, SHTCLK);
SDI12 mySDI12(SDIPIN); 

volatile unsigned long tiptime = millis();
volatile unsigned long rainrate = 0;
           
void setup(){
    Serial.begin(9600); 

    pinMode(RAINPIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(RAINPIN), raincount, FALLING);

    dht.begin();
    mySDI12.begin(); 
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    String output = getData();
    Serial.println(output);
  }
}

String getSDI(String sdiCommand) {
    String sdiReturn = "";

    mySDI12.sendCommand(sdiCommand); 
    delay(30);

    while(mySDI12.available()){    // build a string of the response
      char c = mySDI12.read();
      if((c!='\n') && (c!='\r')) {
//        Serial.print(c);
        sdiReturn += c;
        delay(5); 
      }
    }
//    Serial.println(".");
 
//    Serial.println(sdiReturn);
    mySDI12.flush(); //clear the line

    return(sdiReturn);
}

String getSolinst() {
    String sdiResponse;
    getSDI("0M!");
    delay(5000);
    sdiResponse = getSDI("0D0!");

    return(sdiResponse);
}

String getData() {
    String solResp   = getSolinst();
    int tempPos = solResp.indexOf('+');
    int depthPos = solResp.indexOf('+', tempPos + 1);
    String solTemp = String(solResp.substring(tempPos + 1,depthPos).toFloat());
    String solDepth = String(solResp.substring(depthPos + 1).toFloat());

    String dhtHumid  = String(dht.readHumidity());
    String dhtTemp   = String(dht.readTemperature());

    String soilTemp  = String(sht1x.readTemperatureC());
    String soilHumid = String(sht1x.readHumidity());

    String rainAmt = String(rainrate);

    String output = dhtTemp + "," + dhtHumid + "," + soilTemp + "," + soilHumid + "," + solTemp + "," + solDepth + "," + rainAmt;
    return(output);
}

void raincount() {
  unsigned long tipcount = millis() - tiptime;
  tiptime = millis();
  rainrate = 914400 / tipcount;


  delay(500);
}
