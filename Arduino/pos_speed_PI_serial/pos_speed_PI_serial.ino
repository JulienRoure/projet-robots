// ATTENTION
// to get scanf and printf to work with floats on Arduino, edit the file "platform.txt" in directory
// pi@raspberrypi:/usr/share/arduino/hardware/arduino/avr
// goto lines with "compiler.c.extra_flags=" and "compiler.c.elf.extra_flags=" and add the following
// =-Wl,-u,vfprintf -lprintf_flt -lm -Wl,-u,vfscanf -lscanf_flt -lm
// then the printing will work fine


#include "encoders.hpp"


#include <Encoder.h>
//#include "Encoder.h"

#include "interrupts.hpp"
#include "motors.hpp"
//#include "control.hpp"
#include "control_traj.hpp"
#include <stdio.h>
#include <math.h>

#define ENCODER_OPTIMIZE_INTERRUPTS
#define BUFFER_SIZE 10

char buffer[128] = {0};
char buffer2[128] = {0};

const float delta_t = 0.01;
typedef struct robot_t{

	char msg[40];
	encoder_t encoder_right ;
	encoder_t encoder_left ;
	
} robot_t ;


//static robot_t ;

float gyro = 0;

float x = 0;
float y = 0;

robot_t mobile_robot ;

static motor_t motor_right = init_motor( 12, 34, 35 );
static motor_t motor_left = init_motor( 8, 37, 36 );

static encoder_t encoder_right = init_encoder(  18, 31 ); // 18 31
static encoder_t encoder_left = init_encoder(  19, 38 ); // 19 38

Encoder encoder_lib_right( (int8_t)encoder_right.A, (int8_t)encoder_right.B );
Encoder encoder_lib_left( (int8_t)encoder_left.A, (int8_t)encoder_left.B );

int position = 0;

//static control_t control_left_omega = init_control_traj( 15, 0.15) ;   	// direction internal speed control
//static control_t control_left_theta = init_control_traj( 2, 0) ;      	// direction external position control 

static control_t control_right_omega = init_control_traj( 10, 20) ;   // power internal speed control
static control_t control_right_theta = init_control_traj( 1, 0) ;       // power external position control 

static float time_counter = 0;
static uint32_t cnt = 0;

char buffer_serial[100] = {0};

// put your setup code here, to run once:
void setup() {
    //gyro.begin();
  	Serial.begin(115200);        	// /dev/ttyUSB0   usb cable serial
  	Serial2.begin(115200);          // /dev/ttyS0     gpios on rpi
	
	pinMode(13, OUTPUT);            // blue LED
    drive_voltage( motor_left, 0.0 );
    drive_voltage( motor_right, 0.0 );
    //start_encoders_interrupt();
    start_timer_interrupt();        // starts 10ms timer interrupt
    
	// print header
	//sprintf(buffer, "Hello World! \n");
    //Serial2.print(buffer2);  
		
}


/*
// put your main code here, to run repeatedly:
void loop() {
	int i;
	char buffer_serial[100] = {0};
	
	if( Serial.available() > 0 ){
		for(i = 0 ; i < 100 ; i++){
			char input = Serial.read() ;

			buffer_serial[i] = input;
			
			if( input == '\n' || input == '\0' || Serial.available() == 0 ){
				break;
			}
			
		}

		Serial.println(buffer_serial);

		if( buffer_serial[0] == 's' ){			// it is a command to set a parameter
			if( buffer_serial[2] == 'd' ){		// set the direction 
				
				float target ;
				sscanf( &buffer_serial[3], "%f", &target ) ;

				sprintf( buffer, "%1.5f \n", target) ;
				if( abs(target) <= 1.001){
				//if( 1 ){
					Serial.print( target ) ;
					control_left_theta.set_point = target ;	
				}
				else{
					Serial.print( "target out of range (-1~1) [rad] \n" ) ;
				}
				
				
			}
			else if( buffer_serial[2] == 'p' ){		// set the direction	 
				
				float target ;
				sscanf( &buffer_serial[3], "%f", &target ) ;

				sprintf( buffer, "%1.5f \n", target) ;
				//if( abs(target) <= 1.001){
				if( 1 ){
					Serial.println( target ) ;
					control_right_theta.set_point += target ;	
				}
				else{
					Serial.print( "target out of range (-1~1) [rad] \n" ) ;
				}
				
				
			}
		}
	}

	// read the debounced value of the encoder button
  bool pb = encoder.button();

  // get the encoder variation since our last check, it can be positive or negative, or zero if the encoder didn't move
  // only call this once per loop cicle, or at any time you want to know any incremental change
  int delta = encoder.delta();

  // add the delta value to the variable you are controlling
  //myEncoderControlledVariable += delta;
  position += delta;
	
	sprintf(buffer, "$ [%5d] [%7.3d] ; \n", cnt, position ) ;
	//drive_voltage( motor_left, 1.0 );
	
	//sprintf(buffer, "$ [%010d] [%s] ; \n\0", cnt, buffer_odom) ;
	
	cnt++;
	

	char msg_local[40] = {0} ;
	sprintf(msg_local, "$ [%10d] Hello ; \0", cnt);
	
	mobile_robot.encoder_right = encoder_right ;
	mobile_robot.encoder_left = encoder_direc ;
	strcpy( mobile_robot.msg, msg_local);
	
	/*
	sprintf(buffer, "$ [%010d] [%s] ; \n\0", cnt, (( uint8_t * ) &mobile_robot) ) ;
	
	memcpy(& buffer[16] , &mobile_robot, sizeof(mobile_robot)) ;
	buffer[16 + sizeof(mobile_robot) + 1] = ']';
	buffer[16 + sizeof(mobile_robot) + 2] = ';';
	buffer[16 + sizeof(mobile_robot) + 3] = '\n';
	buffer[16 + sizeof(mobile_robot) + 4] = '\0';
	
	
	// sends bin data
	Serial2.write( (byte *) &mobile_robot, sizeof(robot_t) );	
	//Serial2.write( mobile_robot, sizeof(mobile_robot) );	
	Serial.println( buffer );
	//Serial.println( sizeof(robot_t));
	
  	digitalWrite(13, HIGH);
  	delay(80);
  	
	
}
*/
// loop code

void moveTo(float voltage) {
  drive_voltage(motor_right, voltage);
  drive_voltage(motor_left, -voltage);
  delay(DELAY_UP_DOWN);
}

void stopMove(void) {
  drive_voltage(motor_right, 0.0);
  drive_voltage(motor_left, 0.0);
}

void back(float voltage) {
  drive_voltage(motor_right, -voltage);
  drive_voltage(motor_left, voltage);
  delay(DELAY_UP_DOWN);
}

void toRight(float voltage) {
  drive_voltage(motor_right, -voltage);
  drive_voltage(motor_left, -voltage);
  delay(DELAY_UP_DOWN);
}

void toLeft(float voltage) {
  drive_voltage(motor_right, voltage);
  drive_voltage(motor_left, voltage);
  delay(DELAY_UP_DOWN);
}
void loop()
{
  /*
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
  } */
  	int i;

	// update odom_counters
  	//encoder_right.odom += (int32_t) encoder1.delta();
 	//encoder_left.odom += (int32_t) encoder2.delta();
  	//gyro.update();
  	// do stuff with the updated value
    //Serial.print(" Z:");
    //Serial.println(gyro.getAngleZ() );

    float dois = velocity_angular();
    calculate_speed(&encoder_right);
    calculate_speed(&encoder_left);
  	//sprintf(buffer2, "%ld %ld \t %f %f\n", encoder_right.odom, encoder_left.odom, encoder_right.omega, encoder_left.omega, dois) ;
    //sprintf(buffer2, "%0.3f %0.3f %0.3f \n", x, y, gyro) ;
    //drive_voltage(motor_left,-0.0);
    //drive_voltage(motor_right,0.0);
  	//sprintf(buffer2, "%f %f \n", encoder_right.odom, encoder_left.theta ) ;
  	//Serial.print(buffer2);
  	//Serial.println(  );

	char msg_local[40] = {0} ;
	//sprintf(msg_local, "$ [%10d] Hello ; \0", cnt);
	
	mobile_robot.encoder_right = encoder_right ;
	mobile_robot.encoder_left = encoder_left ;
	strcpy( mobile_robot.msg, msg_local);
	
	//sprintf(buffer, "$ [%010d] [%s] ; \n\0", cnt, (( uint8_t * ) &mobile_robot) ) ;
	/*
	memcpy(& buffer[16] , &mobile_robot, sizeof(mobile_robot)) ;
	buffer[16 + sizeof(mobile_robot) + 1] = ']';
	buffer[16 + sizeof(mobile_robot) + 2] = ';';
	buffer[16 + sizeof(mobile_robot) + 3] = '\n';
	buffer[16 + sizeof(mobile_robot) + 4] = '\0';
	*/
	
	
	// sends bin data
	//Serial2.write( (byte *) &mobile_robot, sizeof(robot_t) );	

  	delay(100);
  	
}
 
//timer5 interrupt 10ms 
ISR(TIMER5_COMPA_vect){
	 
	// update odom_counters
  	encoder_right.odom = encoder_lib_right.read() ;
 	  encoder_left.odom = -1*encoder_lib_left.read() ;
	float baseRobot = 0.18;
	time_counter += 0.010 ; 		// time_counter is in seconds
    
      // calculates instant speed [rad/s]
        calculate_speed( &encoder_right);
        float feedback[3];
        feedback[0] = x;
        feedback[1] = y;
        feedback[2] = gyro;

        float setpoint[3];
        setpoint[0] = 1;
        setpoint[1] = 1;
        setpoint[2] = 2.1;
        // calculates PID
        calculate_traj( &control_right_omega, setpoint ,feedback) ;
        
        
        float vlin = control_right_omega.vel_linear;
        float wlin = control_right_omega.vel_angular;
        
        float vl = (vlin - (baseRobot/2)*wlin)/0.03;
        float vr = (vlin + (baseRobot/2)*wlin)/0.03;

        float ul = vl*0.1/9;
        float ur = vr*0.1/9;
        
        // updates motor voltage
    drive_voltage( motor_right, 0);
    drive_voltage( motor_left, -0);

    float dot_x, dot_y, dot_theta;

    float v = velocity_linear(); 
    
    dot_x = v * cos(gyro);
    dot_y = v * sin(gyro);
    dot_theta = velocity_angular();

    x += dot_x*delta_t;
    y += dot_y*delta_t;
    gyro += dot_theta*delta_t;

    //Serial.println(x);
    //Serial.println("\t");
    //Serial.println(y);
    //Serial.println("\t");
    //Serial.println(gyro);
    //Serial.println("\t");
    //Serial.print(encoder_left.omega*0.029);
    //Serial.print("\n"); */
    
    char c = Serial2.read();
    if (c == 'U' || c == 'w') {
      drive_voltage(motor_right,2.0);
      drive_voltage(motor_left,0.0);
      delay(1000);
    } else if (c == 'D' || c == 's') {
      drive_voltage(motor_right,-2.0);
      drive_voltage(motor_left,2.0);
    } else if (c == 'L' || c == 'a') {
      drive_voltage(motor_right,2.0);
      drive_voltage(motor_left,2.0);
    } else if (c == 'R' || c == 'd') {
      drive_voltage(motor_right,-2.0);
      drive_voltage(motor_left,2.0);
    }
    sprintf(buffer,c);
}
