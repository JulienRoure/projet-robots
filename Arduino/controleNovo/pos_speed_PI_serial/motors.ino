//#include "motors.hpp"

// function to initialize the motor
motor_t init_motor( uint32_t pwm, uint32_t forward, uint32_t backward ){

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

  if( voltage > 12.0 ) voltage = 12.0 ;
  else if(voltage < -12.0) voltage = -12.0 ;

  //if( abs(voltage) < 0.1) voltage = 0 ;		// friction correction
  
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
