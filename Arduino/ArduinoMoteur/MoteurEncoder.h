#ifndef _MOT_ENC_H_
#define _MOT_ENC_H_
// 1 est le moteur à droite et 2, le moteur à gauche
// encoder1 PINs
#define VA1 18
#define VB1 31

// motor1 PINs
#define I11 34
#define I21 35
#define PWM1 12

// encoder2 PINs
#define VA2 19
#define VB2 38

// motor2 PINs
#define I12 37
#define I22 36
#define PWM2 8

void setupEncoder();
void setupMotor();


float getSpeed1();
float getSpeed2();
long getPosition1();
long getPosition2();

void setMotorVoltage(float voltage);


#endif
