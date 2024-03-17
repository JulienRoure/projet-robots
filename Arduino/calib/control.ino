
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

control_t init_control( float kp, float ki){

    control_t control = { kp, ki, 0, 0, 0, 0, 0 } ;

    return control ;
}

void calculate_pid( control_t * control, float feedback ){

	if( control == &control_power_omega ){
		if( ( control->set_point ) > 2.5 ){
			control->set_point = 2.5;
		}
		else if( ( control->set_point ) < - 2.5 ){
			control->set_point = -2.5;
		}
	}

	if( control == &control_direc_omega ){
		if( ( control->set_point ) > 0.5 ){
			control->set_point = 0.5;
		}
		else if( ( control->set_point ) < -0.5 ){
			control->set_point = -0.5;
		}
	}

	control->error = control->set_point - feedback;

	//if( control == &control_direc_theta || control == &control_power_theta ){
		if( abs(control->error) < 0.001 ){
			control->error = 0 ;
			//control->integrator = 0 ; 
		}
	//}

    // anti wind-up
    if( abs( ( control->integrator + control->error ) * control->ki + control->error * control->kp ) < 12.0 ){
        control->integrator += control->error ;     // error * dt 
        // control->integrator *= 0.95 ;
    }

    control->pid = control->kp * control->error + control->ki * control->integrator ;
    
}
