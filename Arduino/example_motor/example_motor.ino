#include "moteur.hpp"
#include "encoders.hpp"
#include "interrupts.hpp"
#include "control.hpp"
#include <stdio.h>

typedef struct robot_t{

  encoder_t encoder_right ;
  encoder_t encoder_left ;
  
} robot_t ;

static robot_t mobile_robot ;

static motor_t right = init_motor( 12, 34, 35 );
static motor_t left = init_motor( 8, 37, 36 );

static encoder_t encoder_left = init_encoder( 18, 31 );
static encoder_t encoder_right = init_encoder( 19, 38 );

static control_t control_left_omega = init_control(10, 1) ;      // direction internal speed control
static control_t control_left_theta = init_control( 2, 0) ;      // direction external position control 

static control_t control_right_omega = init_control( 4, 0.4) ;    // power internal speed control
static control_t control_right_theta = init_control( 2, 0) ;      // power external position control 

static float calib = 0;
static float time_counter = 0;
static uint32_t cnt = 0;

void setup() {
  drive_voltage(left, 0.0);
  drive_voltage(right, 0.0);
  Serial2.begin(115200);
}


    
void loop() {
  while (Serial2.available() == 0) {
    stopMove();
  }

  digitalWrite(LED_BUILTIN, HIGH);
 
  
  char c = Serial2.read();
  if (c == 'U' || c == 'w') {
    moveTo(3.0);
  } else if (c == 'D' || c == 's') {
    back(3.0);
  } else if (c == 'L' || c == 'a') {
    toLeft(3.0);
  } else if (c == 'R' || c == 'd') {
    toRight(3.0);
  } 
}
