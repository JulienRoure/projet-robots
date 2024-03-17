#ATTENTION :

# 1) Pour bien compiler, vérifiez le PATH_CC pour votre ordinateur
# 2) Il faut assurer que le RPI_Root soit bien implementé sur votre ordinateur.

##### COMPILATION CROISEE #######
PATH_CC=/home/jose/Downloads/RPI/tools-master/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin
GCC_PI=$(PATH_CC)/arm-linux-gnueabihf-gcc

#Fake image de notre raspberry sur l'ordi
PATH_RPI_ROOT=/home/jose/Documents/PSE/travail_rpi/RPI_Root

#Mode verbeux, tapper make V=1
ifneq ($V,1)
Q = @
endif

#Paramètres compilateur
DESTDIR =$(PATH_RPI_ROOT)
INCLUDE = -I. -I$(DESTDIR)/include -I$(PATH_RPI_ROOT)/include

CPFLAGS	= -Wall
LDFLAGS = -L. -L$(DESTDIR)/lib
LIBS    = -lwiringPi

### Pour envoyer les programmes sur la Raspberry
USER_PI = pi
IP_PI   = 172.20.10.4
PASSWORD = robot_sec

########################################################################

all : lib exe

lib : libSendToArduino.so

exe : send_to_arduino

libSendToArduino.so : send_to_arduino.c
	@ echo "Compilation de $< pour produire $@"
	$(GCC_PI) $(CPFLAGS) $(INCLUDE) -c -fPIC $< -o send_to_arduino-fpic.o
	$(GCC_PI) -shared send_to_arduino-fpic.o -o $@
	rm -f send_to_arduino-fpic.o

send_to_arduino : libSendToArduino.so send_to_arduino.c
	@ echo "Compilation de send_to_arduino.c pour produire $@"
	$(GCC_PI) $(CPFLAGS) $(INCLUDE) -c send_to_arduino.c -o send_to_arduino.o
	@ echo "Edition des liens pour produire $@"
	$(GCC_PI) $(CPFLAGS) $(LDFLAGS) send_to_arduino.o -o $@ $(LIBS) -lSendToArduino
	rm -f send_to_arduino.o
	@ echo "RAPPEL : Ajouter l'emplacement de libSendToArduino.so dans la variable d'environnement LD_LIBRARY_PATH avant l'exécution !"

sendAll : send_to_arduino libSendToArduino.so
	sshpass -p $(PASSWORD) scp send_to_arduino libSendToArduino.so $(USER_PI)@$(IP_PI):/home/pi/Desktop/Teste

clean : 
	rm -f libSendToArduino.so send_to_arduino

