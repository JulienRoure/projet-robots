

#include "MeOrion.h"

#define MAX_PWM 190
#define VOLT_TO_PWM 255.0 / 12.0
#define DELAY_UP_DOWN 500
#define DELAY_LEFT_RIGHT 550

typedef struct motor_t {
  uint8_t pwm;      // holds the pin number for the pwm
  uint8_t forward;  // holds the pin number for moving forwards
  uint8_t backward; // holds the pin number for moving backward
} motor_t;

motor_t init_motor(uint8_t pwm, uint8_t forward, uint8_t backward);
int drive_voltage(motor_t motor, float voltage);


void moveTo(float voltage);
void stopMove(void);
void back(float voltage);
void toRight(float voltage);
void toLeft(float voltage);
