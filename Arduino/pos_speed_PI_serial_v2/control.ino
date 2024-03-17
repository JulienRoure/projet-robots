/*typedef struct control_t {

  float kp ;  
  float ki ;  
  float kd ;  // Adicionando o termo derivativo

  float integrator ;
  float derivative ;  // Novo termo para a parte derivativa

  float set_point ;
  float feedback ;
  float error ;
  
  float pid ;
  
} control_t ; 

control_t init_control( float kp, float ki, float kd){

    control_t control = { kp, ki, kd, 0, 0, 0, 0, 0, 0 } ;

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

	control->error = control->set_point - feedback;
  
  // Calculando o termo derivativo
  float dt = 0.01; // Por exemplo, use um valor de tempo fixo para a diferença de tempo
  control->derivative = (control->error - control->last_error) / dt;
  control->last_error = control->error;


    // anti wind-up
    if( abs( ( control->integrator + control->error ) * control->ki + control->error * control->kp ) < 7.0 ){
        control->integrator += control->error ;     // error * dt 
        // control->integrator *= 0.95 ;
    }

    control->pid = control->kp * control->error + control->ki * control->integrator + control->kd * control->derivative;
}
*/