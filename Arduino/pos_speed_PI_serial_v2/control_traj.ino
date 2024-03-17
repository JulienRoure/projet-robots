#include "control_traj.hpp"
//#include <cmath>

WheelVelocities controlTrajectory(const TrajectoryParameters &params) {
    WheelVelocities wheel_velocities;

    // Parâmetros do controlador
    double kp_dist = 1; // Ganho proporcional para o erro de distância
    double kp_theta = 10; // Ganho proporcional para o erro de orientação
    
    // Calculando o erro de trajetória
    double e_x = params.xd - params.x_pos;
    double e_y = params.yd - params.y_pos;
    double e_theta = atan2(params.yd - params.y_pos, params.xd - params.x_pos) - params.theta_pos;
    double tol_pos = 0.02; //ver sensibilidade do sensor
    double tol_theta = 0.01; //ver sensibilidade do sensor
    double e_dist = sqrt(e_x * e_x + e_y * e_y);

    double v, w;
    
    if (e_dist > tol_pos) {
        // Calculando as velocidades das rodas
        if (abs(e_theta) > tol_theta) {
            v = 0; // + kp_zeta*zeta;
            w = 1.5 * kp_theta * e_theta;
        } else {
            v = kp_dist * e_dist; // + kp_zeta*zeta;
            w = kp_theta * e_theta;
        }
    } else {
        v = 0;
        w = 5 * (params.thetad - params.theta_pos);
    }

    // Calculando as velocidades das rodas
    double vl = v - params.L / 2 * w;
    double vr = v + params.L / 2 * w;

    wheel_velocities.vl = vl;
    wheel_velocities.vr = vr;

    wheel_velocities.ul = vl * 9 / 0.3;
    wheel_velocities.ur = vr * 9 / 0.3;

    if (wheel_velocities.ur > 6) {
       wheel_velocities.ur = 6.0 ;
    }
    else if (wheel_velocities.ur < -6) {
      wheel_velocities.ur = -6.0 ;
    }

    if (wheel_velocities.ul > 6) {
       wheel_velocities.ul = 6.0 ;
    }
    else if (wheel_velocities.ul < -6) {
      wheel_velocities.ul = -6.0 ;
    }

    if (wheel_velocities.ur < 3 && wheel_velocities.ur > 0.5 ) {
       wheel_velocities.ur = 3.0 ;
    }
    else if (wheel_velocities.ur > -3 && wheel_velocities.ur < -0.5) {
      wheel_velocities.ur = -3.0 ;
    }

    if (wheel_velocities.ul < 3 && wheel_velocities.ul > 0.5 ) {
       wheel_velocities.ul = 3.0 ;
    }
    else if (wheel_velocities.ul > -3 && wheel_velocities.ul < -0.5) {
      wheel_velocities.ul = -3.0 ;
    }

    return wheel_velocities;
}
