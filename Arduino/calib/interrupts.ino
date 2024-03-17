//#include "interrupts.hpp"

// start timer4 interrupt for each 10ms
void start_timer_interrupt(){
    cli();//stop interrupts

    //set timer4 interrupt at 1Hz
    TCCR5A = 0;         // set entire TCCR1A register to 0
    TCCR5B = 0;         // same for TCCR1B
    TCNT5  = 0;         //initialize counter value to 0
    
    // set compare match register for 10 ms increments
    OCR5A = 624;        // = (16*10^6) / (256) - 1 (must be <65536)
    
    // set compare match register for 50 ms increments
    //OCR4A = 3124;       // = (16*10^6) / (256) - 1 (must be <65536)
        
    // set compare match register for 1hz increments
    //OCR4A = 62499;        // = (16*10^6) / (256) - 1 (must be <65536)
    
    TCCR5B |= (1 << WGM12);   // turn on CTC mode
    
    TCCR5B |= (1 << CS12);    // Set CS12 for 256 prescaler
    //TCCR4B |= (1 << CS12) | (1 << CS10);    // Set CS12 and CS10 bits for 1024 prescaler
    
    TIMSK5 |= (1 << OCIE5A);  // enable timer compare interrupt
    
    sei();//allow interrupts
}

void start_encoders_interrupt( ){
         
    attachInterrupt(digitalPinToInterrupt(encoder_power.A), power_isr, RISING);    
    attachInterrupt(digitalPinToInterrupt(encoder_direc.A), direc_isr, RISING);       
    
}
