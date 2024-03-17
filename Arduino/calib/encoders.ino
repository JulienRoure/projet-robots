//#include "encoders.hpp"

// function to initialize the encoders
encoder_t init_encoder( uint32_t A, uint32_t B ){

    encoder_t encoder = { A, B, 0, 0, 0, 0, 0} ;
    
    pinMode(encoder.A, INPUT_PULLUP);
    pinMode(encoder.B, INPUT_PULLUP);

    return encoder;
}

// calculates encoder speed
void calculate_speed( encoder_t * encoder ){
	
    int32_t delta = encoder->odom - encoder->old_odom ;
	
    // converts from delta encoder to omega [rad/s]
    if( encoder == &encoder_power){
        encoder->omega = ( (float)delta * 0.243912473 );     
    }
    else if( encoder == &encoder_direc){
      encoder->omega = ( (float)delta * 0.14959965 );     
    }
    // supposes delta_t = 10ms
    // and gear ratio 2576

    // calculates moving average
    encoder->omega_mean = encoder->omega_mean * 0.80 + encoder->omega * 0.20 ;    
    
    encoder->old_odom = encoder->odom;
}

void calculate_pos( encoder_t * encoder){

    // converts from delta encoder to omega [rad/s]
    if( encoder == &encoder_power){
        encoder->theta = ( encoder->odom * 0.00243912473 );     
    }
    else if( encoder == &encoder_direc){
        encoder->theta = ( encoder->odom * 0.0014959965 );     
    }
    
}

// treats encoder interrupt service routine
void power_isr() {
    
    cli();    // stops interrupts
    
    if( digitalRead( encoder_power.B ) ){     // checks for polarity
        encoder_power.odom += 1.0000 ;
    }
    else{
        encoder_power.odom -= 1.0500 ;  
    }

    sei();    // starts interrupts
}

// treats encoder interrupt service routine
void direc_isr() {
  
    cli();    // stops interrupts
    
    if( digitalRead( encoder_direc.B ) ){     // checks for polarity
        encoder_direc.odom += 1.0000 * 0.82 ;
    }
    else{
        encoder_direc.odom -= (1.0000 + 0.00620) * 0.82 ;  
    }

    sei();    //stop interrupts
}
