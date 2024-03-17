
typedef struct controle_t {

  float kp ;  
  float ki ;  
  float integrator ;

  float set_point ;
  //float old_set_point ;
  
  float feedback ;
  float error ;
  
  float pid ;
  
} control_t ;

control_t init_control( float kp, float ki) ;

void calculate_pid( control_t * control, float feedback ) ;
