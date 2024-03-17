//#include "moteur.hpp"

motor_t init_motor(uint8_t pwm, uint8_t forward, uint8_t backward) {
  motor_t motor = {pwm, forward, backward};
  pinMode(motor.pwm, OUTPUT);
  pinMode(motor.forward, OUTPUT);
  pinMode(motor.backward, OUTPUT);
  drive_voltage(motor, 0);
  return motor;
}

int drive_voltage(motor_t motor, float voltage) {
  if (voltage > 9.0) 
    voltage = 9.0;
  else if (voltage < -9.0) 
    voltage = -9.0;

  int pwm_value = abs(voltage) * VOLT_TO_PWM;

  if (voltage < 0) {
    digitalWrite(motor.forward, 0);
    digitalWrite(motor.backward, 1);
  } else {
    digitalWrite(motor.forward, 1);
    digitalWrite(motor.backward, 0);
  }

  analogWrite(motor.pwm, pwm_value);

  return 0;
}

void moveTo(float voltage) {
  drive_voltage(right, voltage);
  drive_voltage(left, voltage);
  delay(DELAY_UP_DOWN);
}

void stopMove(void) {
  drive_voltage(right, 0.0);
  drive_voltage(left, 0.0);
}

void back(float voltage) {
  drive_voltage(right, -voltage);
  drive_voltage(left, -voltage);
  delay(DELAY_UP_DOWN);
}

void toRight(float voltage) {
  drive_voltage(right, -voltage);
  drive_voltage(left, voltage);
  delay(DELAY_UP_DOWN);
}

void toLeft(float voltage) {
  drive_voltage(right, voltage);
  drive_voltage(left, -voltage);
  delay(DELAY_UP_DOWN);
}
