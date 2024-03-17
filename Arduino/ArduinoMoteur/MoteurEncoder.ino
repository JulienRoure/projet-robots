
#include "MoteurEncoder.h"


volatile long compteur1 = 0;
volatile long  t_ISR_last1 = 0;
volatile long  t_ISR1 = 0;
volatile long compteur2 = 0;
volatile long  t_ISR_last2 = 0;
volatile long  t_ISR2 = 0;

void setupMotor()
{
  pinMode(I11, OUTPUT);
  pinMode(I21, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(I12, OUTPUT);
  pinMode(I22, OUTPUT);
  pinMode(PWM2, OUTPUT);
}

void setMotorVoltage(float voltage){
  voltage = constrain(voltage,-9.0, 9.0);
  if(voltage>0)
  {
    digitalWrite(I21,LOW);
    digitalWrite(I11,HIGH);
    digitalWrite(I22,LOW);
    digitalWrite(I12,HIGH);
  }else{
    digitalWrite(I11,LOW);
    digitalWrite(I21,HIGH);
    digitalWrite(I12,LOW);
    digitalWrite(I22,HIGH);
  }
  
  analogWrite(PWM1, abs(voltage)*255.0/12.0   );
  analogWrite(PWM2, abs(voltage)*255.0/12.0   );
}

void setupEncoder(){
  pinMode(VA1, INPUT_PULLUP);
  pinMode(VB1, INPUT_PULLUP);
  pinMode(VA2, INPUT_PULLUP);
  pinMode(VB2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(VA1), _ISR_VA1, RISING);
  attachInterrupt(digitalPinToInterrupt(VA2), _ISR_VA2, RISING);
}
  
void _ISR_VA1(){
  if(digitalRead(VB1)){
    compteur1++;  
  }else{
    compteur1--;
  }
  t_ISR_last1 = t_ISR1;
  t_ISR1= micros();
}

void _ISR_VA2(){
  if(digitalRead(VB2)){
    compteur2++;  
  }else{
    compteur2--;
  }
  t_ISR_last2 = t_ISR2;
  t_ISR2 = micros();
}

float getSpeed1(){
  float  t_ISR_last_copy1;
  float  t_ISR_copy1;
  noInterrupts();
  t_ISR_last_copy1 =t_ISR_last1;
  t_ISR_copy1 = t_ISR1;
  interrupts();
  if( t_ISR1==t_ISR_last1)
    return 0;
  else
    return (1.0/(t_ISR_copy1-t_ISR_last_copy1) )*1e6;
}

float getSpeed2(){
  float  t_ISR_last_copy2;
  float  t_ISR_copy2;
  noInterrupts();
  t_ISR_last_copy2 =t_ISR_last2;
  t_ISR_copy2 = t_ISR2;
  interrupts();
  if( t_ISR2==t_ISR_last2)
    return 0;
  else
    return (1.0/(t_ISR_copy2-t_ISR_last_copy2) )*1e6;
}

long getPosition1(){
  noInterrupts();
  long compteur_copy = compteur1;
  interrupts();
  return compteur_copy;
}

long getPosition2(){
  noInterrupts();
  long compteur_copy = compteur1;
  interrupts();
  return compteur_copy;
}
