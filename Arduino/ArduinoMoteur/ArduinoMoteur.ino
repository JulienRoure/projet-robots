#include "ArduinoMoteur.h"
#include "encoders.hpp"
void setup() {
  Serial.begin(9600);
  setupEncoder();
  setupMotor();

}


unsigned long waitNextPeriod(){
  unsigned long temps=0;
  static unsigned long temps_prec=0;
  temps = millis();
  while( (temps-temps_prec)<DT)
  {
    temps = millis();
  }
  temps_prec = temps;
  return temps;
}

float stepSequence(float u0, float u1, float t_start,float t_stop){
  float u = 0;
  unsigned long temps= millis();
  if(temps < t_start) 
  {
      u=u0;
  }else
  if (temps <t_stop)
  {
    u= u1;
  }else
  if(temps>=t_stop){
  u =u0  ;
  }
  return u;
}

void loop() {
  unsigned long time =0;
  float u = 0;
  float speed_d = 0;
  float position_d= 0;
  float speed_g = 0;
  float position_g= 0;
  
  time = waitNextPeriod();
  // sensor update
  speed_d = getSpeed1();
  position_d = getPosition1();
  speed_g = getSpeed2();
  position_g = getPosition2();
  // control update
  u = stepSequence(0,5,1000,3000);
  // actuator update
  setMotorVoltage(u);
  
  printState(time, u, speed_d, position_d);
}

void printState(unsigned long time, float voltage, float speed_d, float position_d){
  Serial.print(time);
  Serial.print(" ,");
  Serial.print(voltage);
  Serial.print(" ,");
  Serial.print(speed_d);
  Serial.print(" ,");
  Serial.print(position_d);
  Serial.print(" ;");
  Serial.println(" ");
}
