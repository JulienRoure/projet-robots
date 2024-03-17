
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

control_t init_control( float kp, float ki){

    control_t control = { kp, ki, 0, 0, 0, 0, 0 } ;

    return control ;
}

void calculate_pid( control_t * control, float feedback ){

	float max_speed_omega = 2.5 ;
	
	if( control == &control_right_omega ){
		if( ( control->set_point ) > max_speed_omega ){
			control->set_point = max_speed_omega;
		}
		else if( ( control->set_point ) < - max_speed_omega ){
			control->set_point = -max_speed_omega ;
		}
	}

	float max_speed_left = 0.10 ;
	
	if( control == &control_left_omega ){
		if( ( control->set_point ) > max_speed_left ){
			control->set_point = max_speed_left ;
		}
		else if( ( control->set_point ) < -1 * max_speed_left ){
			control->set_point = -1 * max_speed_left ;
		}
	}

	control->error = control->set_point - feedback;

	if( control == &control_left_theta ){
		if( abs(control->error) < 0.000609781 ){
			control->error = 0 ;
			//control->integrator = 0 ; 
		}
	}
	else if( control == &control_right_theta ){
		if( abs(control->error) < 0.00029088 ){
			control->error = 0 ;
			//control->integrator = 0 ; 
		}
	}

    // anti wind-up
    if( abs( ( control->integrator + control->error ) * control->ki + control->error * control->kp ) < 12.0 ){
        control->integrator += control->error ;     // error * dt 
        // control->integrator *= 0.95 ;
    }

    control->pid = control->kp * control->error + control->ki * control->integrator ;
}
*/
