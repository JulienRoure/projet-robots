
//#include "encoders.hpp"
#define PI 3.141592654

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
    if( encoder == &encoder_right){
        encoder->omega = ( (float)delta * 0.0542 );    //  ( ( 2 * PI ) / ( 46 * 1 * 8 * 2 ) ) );   
    }
    else if( encoder == &encoder_left){
      encoder->omega = ( (float)delta *  0.0542  );    //  ( ( 2 * PI ) / ( 75 * 1 * 8 * 4 ) ) );    0.0609781 
    }
    // supposes delta_t = 10ms
    // and gear ratio 46

    // calculates moving average
    encoder->omega_mean = encoder->omega_mean * 0.90 + encoder->omega * 0.10 ;    
    
    encoder->old_odom = encoder->odom;
}


void calculate_pos( encoder_t * encoder){
    
    // converts from delta encoder to omega [rad/s]
    if( encoder == &encoder_right){
      //encoder->theta = ( (float)encoder->odom * ( ( 2 * PI ) / ( 46 * 7 * 8 * 4 ) ) );     
        encoder->theta = ( (float)encoder->odom * 0.00008536684 );     
    }
    else if( encoder == &encoder_left){
      //encoder->theta = ( (float)encoder->odom * ( ( 2 * PI ) / ( 46 * 7 * 8 * 4 ) ) );          
      encoder->theta = ( (float)encoder->odom * 0.00008536684); 
    }
    
}

float velocity_linear() {

    float v = (encoder_right.omega + encoder_left.omega)*0.03/2;
    return v;
  }

float velocity_angular() {
    float baseRobot = 0.18;
    float w = (encoder_right.omega - encoder_left.omega)*0.03/baseRobot;
    return w;
  }

// treats encoder interrupt service routine
/*
void right_isr() {
    
    cli();    // stops interrupts
    
    if( digitalRead( encoder_right.B ) == digitalRead( encoder_right.A ) ){     // checks for polarity
        encoder_right.odom += 1.0000 ;
    }
    else{
        encoder_right.odom -= 1.0600 ;  
    }

    sei();    // starts interrupts
}

// treats encoder interrupt service routine
void left_isr() {
  
    cli();    // stops interrupts
    
    if( digitalRead( encoder_left.B ) == digitalRead( encoder_left.A ) ){     // checks for polarity
        encoder_left.odom += 1.0000 * 0.82 ;
    }
    else{
        encoder_left.odom -= (1.0000 + 0.0018) * 0.82 ;  
    }

    sei();    //stop interrupts
}
*/
