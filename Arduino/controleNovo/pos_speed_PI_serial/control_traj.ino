#include "control_traj.hpp"
//#include <cmath>

WheelVelocities controlTrajectory(const TrajectoryParameters &params) {
    WheelVelocities wheel_velocities;

    // Parâmetros do controlador
    double kp_dist = 5; // Ganho proporcional para o erro de distância
    double kp_theta = 10; // Ganho proporcional para o erro de orientação
    
    // Calculando o erro de trajetória
    double e_x = params.xd - params.x_pos;
    double e_y = params.yd - params.y_pos;
    double e_theta = atan2(params.yd - params.y_pos, params.xd - params.x_pos) - params.theta_pos;
    double tol_pos = 10^-2; //ver sensibilidade do sensor
    double tol_theta = 3.1415 / 18; //ver sensibilidade do sensor
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
        w = kp_theta * (params.thetad - params.theta_pos);
    }

    // Calculando as velocidades das rodas
    double vl = v - params.L / 2 * w;
    double vr = v + params.L / 2 * w;

    wheel_velocities.ul = vl * 0.3 / 9;
    wheel_velocities.ur = vr * 0.3 / 9;

    return wheel_velocities;
}
