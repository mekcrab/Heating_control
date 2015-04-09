//testing file for Mudbus TCP/IP modbus interface

#include <SPI.h>
#include <Ethernet.h>
#include <Mudbus.h>

#define DEBUG

//Instansiate Mudbus class
Mudbus Mb;

void setup(void){
	//setup ethernet and start
	uint8_t mac[]   = { 0x90, 0xA2, 0xDA, 0x00, 0x51, 0x06 };
	uint8_t ip[]	= { 192, 168, 0, 51};
	uint8_t gateway[] = { 192,168,0,1};	
	uint8_t subnet[]  = { 255, 255, 255, 0};
	Ethernet.begin(mac, ip, gateway, subnet);

	//Avoid pins 4,10,11,12,13 when using ethernet shield
	delay(5000); //Time to open the terminal

	#ifdef DEBUG
		Serial.begin(9600);
	#endif	

	pinMode(7, OUTPUT);
	pinMode(8, OUTPUT);

	//Set some static registers and coils
	Mb.R[1] = 4294967295;
	Mb.R[2] = 1500;		//millivolts i.e. AIN
	Mb.R[3] = 0;
}

void loop(void){
        //Run MODBUS service
	Mb.Run();
  
	//pin 7 to coil 7
	Mb.C[7] = digitalRead(7);	
	//coil 8 write to pin 8
	digitalWrite(8, Mb.C[8]);

	#ifdef DEBUG
	  if (Serial.available() > 0) {
        	Serial.print("C8 = ");
	        Serial.println(Mb.C[8]);
	        Serial.print("C7 = ");
	        Serial.println(Mb.C[7]);
                while(Serial.available()>0){Serial.read();}
          }
	#endif
}

