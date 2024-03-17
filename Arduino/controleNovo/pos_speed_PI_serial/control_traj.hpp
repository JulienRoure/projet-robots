#ifndef CONTROL_TRAJ_HPP
#define CONTROL_TRAJ_HPP

struct TrajectoryParameters {
    double L; // Comprimento do eixo
    double x_pos; // Posição x atual
    double y_pos; // Posição y atual
    double theta_pos; // Orientação atual
    double xd; // Destino x
    double yd; // Destino y
    double thetad; // Orientação desejada
};

struct WheelVelocities {
    double ul; // Velocidade da roda esquerda
    double ur; // Velocidade da roda direita
};

WheelVelocities controlTrajectory(const TrajectoryParameters &params);

#endif
