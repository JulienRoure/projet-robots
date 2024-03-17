/**
 * \par Copyright (C), 2012-2016, MakeBlock
 * @file    UltrasonicSensorTest.ino
 * @author  MakeBlock
 * @version V1.0.0
 * @date    2015/09/01
 * @brief   Description: this file is sample code for Me ultrasonic sensor module.
 *
 * Function List:
 * 1. double MeUltrasonicSensor::distanceCm(uint16_t MAXcm)
 *
 * \par History:
 * <pre>
 * <Author>     <Time>        <Version>      <Descr>
 * Mark Yan     2015/09/01    1.0.0          rebuild the old lib
 * </pre>
 */



// pins used by the motor drivers
#define PWMB_1 12
#define BI1_1 34
#define BI2_1 35

#define PWMB_2 8
#define BI1_2 37
#define BI2_2 36

#define MAX_PWM 190     // maximum duty cycle for the PWM is 255/MAXPWM
#define VOLT_TO_PWM 255.0/12.0

#define DELAY_UP_DOWN 500
#define DELAY_LEFT_RIGHT 550

#include "MeOrion.h"

typedef struct motor_t {

  uint8_t pwm ;          // holds the pin number for the pwm
  uint8_t forward ;     // holds the pin number for moving forwards
  uint8_t backward ;    // holds the pin number for moving backwards
  
} motor_t ;

MeUltrasonicSensor ultraSensor(PORT_8); /* Ultrasonic module can ONLY be connected to port 3, 4, 6, 7, 8 of base shield. */

// functions declaration
int drive_voltage( motor_t motor, float voltage );
motor_t init_motor( uint8_t pwm, uint8_t forward, uint8_t backward );


// function to initialize the motor
motor_t init_motor( uint8_t pwm, uint8_t forward, uint8_t backward ){

  motor_t motor = { pwm, forward, backward } ;
  
  // motor pins mode 
  pinMode(motor.pwm, OUTPUT);
  pinMode(motor.forward, OUTPUT);
  pinMode(motor.backward, OUTPUT);
  
  drive_voltage(motor, 0);

  return motor;
}


// function to apply voltage to the motors
int drive_voltage( motor_t motor, float voltage ){

  if( voltage > 9.0 ) voltage = 9.0 ;
  else if(voltage < -9.0) voltage = -9.0 ;
    
  int pwm_value = abs(voltage) * VOLT_TO_PWM ;

  if(voltage < 0){
    digitalWrite( motor.forward, 0 );
    digitalWrite( motor.backward, 1 );
  }
  else{
    
    digitalWrite( motor.forward, 1 );
    digitalWrite( motor.backward, 0);
  }

  analogWrite( motor.pwm, pwm_value );
  
  return 0;
}

static motor_t right = init_motor( 12, 34, 35 );
static motor_t left = init_motor( 8, 36, 37 );


void moveTo(float voltage){
  drive_voltage(right, voltage);
  drive_voltage(left,voltage);
  delay(DELAY_UP_DOWN);   // define delay period
  
  }

void stopMove(void){
  drive_voltage(right, 0.0);
  drive_voltage(left, 0.0);
  }

void back(float voltage){
  drive_voltage(right, -voltage);
  drive_voltage(left,-voltage);
  delay(DELAY_UP_DOWN);   // define delay period
  //break;
  }

void toRight(float voltage){
  drive_voltage(right, -voltage);
  drive_voltage(left,voltage);
  delay(DELAY_UP_DOWN);   // define delay period
  //break;
  
  }

void toLeft(float voltage){
  drive_voltage(right, voltage);
  drive_voltage(left,-voltage);
  delay(DELAY_UP_DOWN);   // define delay period
  //break;
  }
void setup()
{
  drive_voltage( left, 0.0);
  drive_voltage( right, 0.0);
  Serial.begin(9600);
}

void loop()
{
  if (ultraSensor.distanceCm() < 20){
    back(5.0);
    delay(DELAY_UP_DOWN);
    }
}
