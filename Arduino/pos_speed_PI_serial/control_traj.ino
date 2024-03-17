/*
  typedef struct control_t {

  float kp ;  
  float ki ;  
  float integrator ;

  float set_point ;
  //float old_set_point ;
  
  float feedback ;
  float error ;
  
  float pid ;
  
} control_t ;

*/

control_t init_control_traj( float kp_dist, float kp_theta){

    control_t control = { kp_dist, kp_theta, 0, 0, 0, 0, 0 } ;

    return control ;
}

void calculate_traj( control_t * control, float setpoint[3], float feedback[3] ){

  float max_speed_omega = 2.5 ;
  
  if( ( control->x_setpoint ) > max_speed_omega ){
      control->x_setpoint = max_speed_omega;
    }
    else if( ( control->x_setpoint ) < - max_speed_omega ){
      control->x_setpoint = -max_speed_omega ;
    }
  

  if( ( control->y_setpoint ) > max_speed_omega ){
      control->y_setpoint = max_speed_omega;
    }
    else if( ( control->y_setpoint ) < - max_speed_omega ){
      control->y_setpoint = -max_speed_omega ;
    }

  float max_speed_left = 0.10 ;
  
  if( ( control->theta_setpoint ) > max_speed_left ){
      control->theta_setpoint = max_speed_left ;
    }
    else if( ( control->theta_setpoint ) < -1 * max_speed_left ){
      control->theta_setpoint = -1 * max_speed_left ;
    }

  control->x_setpoint = setpoint[0];
  control->y_setpoint = setpoint[1];
  control->theta_setpoint = setpoint[2];


  control->error_x = control->x_setpoint - feedback[0];
  control->error_y = control->y_setpoint - feedback[1];
  control->error_theta = atan2(control->error_y,control->error_x) - feedback[2];
  control->error_dist = sqrt(pow(control->error_x, 2) + pow(control->error_y, 2));

  if( abs(control->error_x) < 0.002 ){
      control->error_x = 0 ;
      //control->integrator = 0 ; 
    }
    if( abs(control->error_y) < 0.002 ){
      control->error_y = 0 ;
      //control->integrator = 0 ; 
    }

    // anti wind-up
   /* if( abs( ( control->integrator + control->error ) * control->ki + control->error * control->kp ) < 12.0 ){
        control->integrator += control->error ;     // error * dt 
        // control->integrator *= 0.95 ;
    }*/

    float tolerance_pos = 0.02;
    float tolerance_theta = 3.14/18;
  

    if (control->error_dist > tolerance_pos) {
        if (abs(control->error_theta) > tolerance_pos) {
            control->vel_linear = 0.0 ;
            control->vel_angular = 1.5 * control->kp_theta * control->error_theta ;

    } else {
      control->vel_linear = control->kp_dist * control->error_dist ;
      control->vel_angular = control->kp_theta * control->error_theta ;

    }
    } else{
      control->vel_linear = 0.0 ;
      control->vel_angular = control->kp_theta * control->error_theta ;

    }
}
