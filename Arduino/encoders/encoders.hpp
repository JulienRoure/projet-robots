// pins used for encoder 1 (powertrain motor encoder)
#define PORT1_NE1 31    // determines orientation B
#define PORT1_NE2 18    // accepts interrupts A

// pins used for encoder 2 (direction motor encoder)
#define PORT2_NE1 38    // determines orientation B
#define PORT2_NE2 19    // accepts interrupts A

// defines quadrature encoder pins
//uint8_t A_Pin = PORT1_NE2;
//uint8_t B_Pin = PORT1_NE1;

typedef struct encoder_t {

  uint32_t A ;             // holds the pin number for the A quadrature signal
  uint32_t B ;             // holds the pin number for the B quadrature signal
  
  float odom ;            // holds total distance ever travelled in encoder ticks
  float old_odom ;        // holds odom since lasts measurement

  float theta ;           // holds instant position
  
  float omega ;           // holds the instant angular velocity of the wheels
  float omega_mean ;      // holds the instant angular velocity of the wheels
  
} encoder_t ;

// function to initialize the encoders
encoder_t init_encoder( uint32_t A, uint32_t B );
