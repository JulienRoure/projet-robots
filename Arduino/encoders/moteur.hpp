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

typedef struct motor_t {

  uint32_t pwm ;          // holds the pin number for the pwm
  uint32_t forward ;     // holds the pin number for moving forwards
  uint32_t backward ;    // holds the pin number for moving backwards
  
} motor_t ;

// functions declaration

void back(float voltage);
void moveTo(float voltage);
void stopMove(float voltage);
void toRight(float voltage);
void toLeft(float voltage);
// function to initialize the motor
motor_t init_motor( uint32_t pwm, uint32_t forward, uint32_t backward );

// function to apply voltage to the motors
int drive_voltage( motor_t motor, float voltage );  
