import serial

def read_serial(serial_port='/dev/ttyS0', serial_speed=115200):
    try:
        # Initialize the serial connection
        ser = serial.Serial(serial_port, serial_speed, timeout=1)
        
		with open('arrivee.txt', 'w') as fichier:
		    while True:
		        # Read a line from the serial port
		        line = ser.readline().decode('utf-8').strip()

		        # Check if the line is not empty before printing
		        if line:
		            print(f'Received data: {line}')
		            
		        if line == '1':
		                fichier.write('1\n')
		                #print("Ecriture de '1' dans le fichier arrivee.txt")
		            else:
		                print("Données non valides, aucun écriture dans le fichier")
		
    except KeyboardInterrupt:
        # Capture keyboard interruption (Ctrl+C) to terminate the program
        print("Program terminated by the user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the serial connection when the program terminates
        ser.close()

# Call the function to read from the serial port
read_serial()

