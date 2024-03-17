typedef struct controle_t {

  float kp_dist ;  
  float kp_theta ;  
  float integrator ;

  float x_setpoint ;
  float y_setpoint ;
  float theta_setpoint ;
  //float old_set_point ;
  
  float feedback[3] ;

  float error_x ;
  float error_y ;
  float error_theta;
  float error_dist;
  
  float vel_linear ;
  float vel_angular ;
  
} control_t ;

control_t init_control_traj( float kp_dist, float kp_theta) ;

//void calculate_traj( control_t * control, float setpoint[3], float feedback[3] ) 
