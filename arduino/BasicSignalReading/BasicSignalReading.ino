// Script for basic signal reading and output to the graphical serial monitor
// Used for initial testing of the EXG pill to detect accurate signal detection

void setup() {
  Serial.begin(9600);
}

void loop() {
  bool read = false;
  int sensorValue0 = analogRead(A0);
  int sensorValue1 = 456;//analogRead(A1);
  int sensorValue2 = 789;//analogRead(A2);
  int sensorValue3 = 135;//analogRead(A3);
  int sensorValue4 = 791;//analogRead(A4);
  //String com = ",";

  ///float val;

  // Concatenate the sensor values 
  ///val = (sensorValue0*1000000) + (sensorValue1*1000) + (sensorValue2*1) + (sensorValue3/1000) + (sensorValue4/1000000);


  //String thing = String(sensorValue0) + String(sensorValue1) + String(sensorValue2) + String(sensorValue3) + String(sensorValue4);
  //String thing = String(sensorValue0) + "000000000000";
  
  //Serial.println(sensorValue0 + com + sensorValue1 + com + sensorValue2 + com + sensorValue3 + com + sensorValue4);
  //Serial.println(sensorValue0);
  
  //Serial.print(sensorValue0);

  //Serial.print(sensorValue1);

  //Serial.print(sensorValue2);
  
  //Serial.print(sensorValue3);
  
  //Serial.println(sensorValue4);


  

  
  Serial.println(sensorValue0);
  //Serial.println(sensorValue1);
  //Serial.println(sensorValue2);
  //Serial.println(sensorValue3);
  //Serial.println(sensorValue4)

}

