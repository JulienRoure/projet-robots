/**
 * \par Copyright (C), 2012-2016, MakeBlock
 * @file    MeMegaPiDCMotorTest.ino
 * @author  MakeBlock
 * @version V1.0.0
 * @date    2016/05/17
 * @brief   Description: this file is sample code for MegaPi DC motor device.
 *
 * Function List:
 *    1. void MeMegaPiDCMotorTest::run(int16_t speed)
 *    2. void MeMegaPiDCMotorTest::stop(void)
 *
 * \par History:
 * <pre>
 * <Author>     <Time>        <Version>      <Descr>
 * Mark Yan     2016/05/17    1.0.0          build the new
 * </pre>
 */

#define DELAY_UP_DOWN 500
#define DELAY_LEFT_RIGHT 550


#include "MeMegaPi.h"

MeMegaPiDCMotor motor1(PORT1A);

MeMegaPiDCMotor motor2(PORT1B);

MeMegaPiDCMotor motor3(PORT2A);

MeMegaPiDCMotor motor4(PORT2B);


uint8_t motorSpeed = 100;

void recuer(int motorSpeed){
  motor1.run(motorSpeed); /* value: between -255 and 255. */
  motor2.run(motorSpeed); /* value: between -255 and 255. */
  motor3.run(-motorSpeed);
  motor4.run(-motorSpeed);
  }

void avancer(int motorSpeed){
  motor1.run(-motorSpeed); /* value: between -255 and 255. */
  motor2.run(-motorSpeed); /* value: between -255 and 255. */
  motor3.run(motorSpeed);
  motor4.run(motorSpeed);
  }

 void droit(int motorSpeed){
  motor1.run(motorSpeed); /* value: between -255 and 255. */
  motor2.run(motorSpeed); /* value: between -255 and 255. */
  motor3.run(motorSpeed);
  motor4.run(motorSpeed);
  }

void gauche(int motorSpeed){
  motor1.run(-motorSpeed); /* value: between -255 and 255. */
  motor2.run(-motorSpeed); /* value: between -255 and 255. */
  motor3.run(-motorSpeed);
  motor4.run(-motorSpeed);
  }

void arreter(){
  motor1.stop(); /* value: between -255 and 255. */
  motor2.stop(); /* value: between -255 and 255. */
  motor3.stop();
  motor4.stop();
  }
  
void setup()
{
  Serial2.begin(9600);    // /dev/ttyS0     on rpi
}

void loop()
{

  
  Serial2.flush();
  

  while ( Serial2.available() == 0 ) {
    // do nothing
    digitalWrite(LED_BUILTIN, LOW);   
    arreter();
  }
  digitalWrite(LED_BUILTIN, HIGH);   
  
  char c = Serial2.read();
  if( c == 'U' || c == 'w' ){
    avancer(100);
    delay(DELAY_UP_DOWN);   // define delay period
    //break;
  }
  else if( c == 'D' || c == 's' ){
    recuer(100);  
    delay(DELAY_UP_DOWN);   
  }
  else if( c == 'L' || c == 'a' ){
    gauche(150);   

    delay(DELAY_LEFT_RIGHT);   
  }
  else if( c == 'R' || c == 'd' ){
    droit(150);
    delay(DELAY_LEFT_RIGHT);   
  }

  else {
    avancer(0);
    }
  
}
