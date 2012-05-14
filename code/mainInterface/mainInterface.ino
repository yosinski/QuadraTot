#include "myAx12.h"
#include <Motors2.h>

#define NUM_SERVOS 8

#define BIOLOID_FRAME_LENGTH 33
#define BIOLOID_SHIFT 3

#define COMMAND_OVER_TIME 20

/** Used for timing events. Should be removed later. */
unsigned int ticToc = 0;
void tic(String x) { Serial.print(x + ": ");ticToc = millis(); }
void toc() { ticToc = millis() - ticToc; Serial.println(ticToc); }

int mode = 0;			   // where we are in the frame

unsigned char id = 0;      // id of this frame
unsigned char length = 0;  // length of this frame
unsigned char ins = 0;     // instruction of this frame

unsigned char params[50];  // parameters
unsigned char index = 0;   // index in param buffer

int checksum;              // checksum

int speed[NUM_SERVOS];
unsigned int pose[NUM_SERVOS];
unsigned int nextpose[NUM_SERVOS];
unsigned long lastframe;

void interpolateSetup(int time) {
    int i;
    int frames = (time/BIOLOID_FRAME_LENGTH) + 1;
    lastframe = millis();
    // set speed each servo...
    for(i=0;i<NUM_SERVOS;i++){
        if(nextpose[i] > pose[i]){
            speed[i] = (nextpose[i] - pose[i])/frames + 1;
        }else{
            speed[i] = (pose[i]-nextpose[i])/frames + 1;
        }
    }
    //interpolating = 1;
}

void interpolateStep() {
    //if(interpolating == 0) return;
    int i;
    int complete = NUM_SERVOS;
    while(millis() - lastframe < BIOLOID_FRAME_LENGTH);
    lastframe = millis();
    // update each servo
    for(i=0;i<NUM_SERVOS;i++){
        int diff = nextpose[i] - pose[i];
        if(diff == 0){
            complete--;
        }else{
            if(diff > 0){
                if(diff < speed[i]){
                    pose[i] = nextpose[i];
                    complete--;
                }else
                    pose[i] += speed[i];
            }else{
                if((-diff) < speed[i]){
                    pose[i] = nextpose[i];
                    complete--;
                }else
                    pose[i] -= speed[i];                
            }       
        }
    }
    //if(complete <= 0) interpolating = 0;
    writePose();      
}

/* write pose out to servos using sync write. */
void writePose(){
    int temp;
    int count = NUM_SERVOS;
    int length = 4 + (NUM_SERVOS * 3);   // 3 = id + pos(2byte)
    int checksum = 254 + length + AX_SYNC_WRITE + 2 + AX_GOAL_POSITION_L;
    
    //tic("set tx");
    setTXall();
    //toc();
    
    //tic("write bytes");
    ax12write(0xFF);
    ax12write(0xFF);
    ax12write(0xFE);
    ax12write(length);
    ax12write(AX_SYNC_WRITE);
    ax12write(AX_GOAL_POSITION_L);
    ax12write(2);
    while(count > 0){
        count--;
        temp = pose[count] >> BIOLOID_SHIFT;
        checksum += (temp&0xff) + (temp>>8) + count + 1;
        ax12write(count + 1);
        ax12write(temp&0xff);
        ax12write(temp>>8);
    } 
    ax12write(0xff - (checksum % 256));
    //toc();
    
    //tic("Set rx");
    setRX(0);
    //toc();
}

/** Commands the robot to move into the given position vector over the course of dur milliseconds
  * Position vector values are in the range [0,270]
  *
  * Note: the actual command wants values in the range [0,~8250]. I just did a simple transformation
  * to get the input values to line up with the angle (in degrees) the servo is actually in.
  */
void commandOverTime(unsigned int pos[], unsigned int dur) {
  //tic("begin");
  
  int steps = dur/BIOLOID_FRAME_LENGTH;
  
  //int curTime = millis();
  int i;
  for (i = 0; i < steps; i++) {
    //interpolate
    int j;
    for (j = 0; j< 8; j++) {
      nextpose[j] = pose[j] * (float(steps - i)/float(steps)) + 30 * pos[j] * (float(i) / float(steps));
    }
    //nextpose = pos;
    interpolateSetup(dur/8);
    interpolateStep();
  }
  //toc();
}

/** Sends a return packet to the PC with details about the current position we are in.
  *
  * Format: ff ff servo1 servo2 ... servo8 checksum
  */
void returnPos() {
	Serial.write(0xff);
	Serial.write(0xff);
	Serial.write(AX_PRESENT_POSITION_L);
	Serial.write(18);  // length
	Serial.write(0x01); // error
	
	int checksum = AX_PRESENT_POSITION_L + 1 + 18;
	int i;
	for (i = 0; i < NUM_SERVOS; i++) {
		int p = ax12GetRegister(i, AX_PRESENT_POSITION_L, 2);
		byte a = (byte) (0x00ff & (p >> 8));
		byte b = (byte) (0x00ff & p);
		Serial.write(a);
		Serial.write(b);
		checksum += a + b;
	}
	Serial.write(checksum % 256);
}

//-----------------------------------------------------------------------------------------------------//
//------------------------------------------------Begin------------------------------------------------//
//-----------------------------------------------------------------------------------------------------//
//Motors2 drive = Motors2();

void setup(){
    Serial.begin(38400);    
    pinMode(0,OUTPUT);     // status LED
	
	//Go to a ready position
	int i;
    for (i = 0; i < 8; i++) pose[i] = 0;
    writePose();
    delay(500);
	
	char x = 100;
	char y = 150;
	Serial.print(x+y);
	Serial.print(x+x+y);
	
    tic("ret");
    returnPos();
    toc();
}

/*  Instruction formats: FF length instruction parameters checksum
 *    1. commandOverTime(): dur dur msB1 lsB1 msB2 lsB2 msB3 lsB3...
 */
void loop() {
	int i;
    // process messages
    while(Serial.available() > 0){
        // We need to 0xFF at start of packet
        if(mode == 0){         // start of new packet
            if(Serial.read() == 0xff){
                mode = 3;
                //digitalWrite(0,HIGH-digitalRead(0));
            }
        // }else if(mode == 2){   // next byte is index of servo
            // id = Serial.read();    
            // if(id != 0xff)
                // mode = 3;
        }else if(mode == 3){   // next byte is length
            length = Serial.read();
            checksum = length;
            mode = 4;
        }else if(mode == 4){   // next byte is instruction
            ins = Serial.read();
            checksum += ins;
            index = 0;
            mode = 5;
		}else if(mode == 5){   // read data in 
            params[index] = Serial.read();
            checksum += (int) params[index];
            index++;
            if(index >= length) mode = 6; // we've read params
        } else if (mode == 6) { // read the checksum
			mode = 0;
			unsigned int innerChecksum = Serial.read();
			
			if((checksum%256) != innerChecksum){ // there was some sort of error
				// return a packet: FF FF id Len Err params=None check
				Serial.print(0xff); //do I want to keep this return packet stuff?
				Serial.print(0xff);
				Serial.print(id);
				Serial.print(2);
				Serial.print(64);
				Serial.print(255-((66+id)%256));
			}else{
				int i;
				// pass thru
			   if(ins == AX_READ_DATA) {
					ax12GetRegister(id, params[0], params[1]);
					// return a packet: FF FF id Len Err params check
					if(ax_rx_buffer[3] > 0){
					for(i=0;i<ax_rx_buffer[3]+4;i++)
						Serial.print(ax_rx_buffer[i]);
					}
					ax_rx_buffer[3] = 0;
					
					
				} else if (ins == COMMAND_OVER_TIME) { // TODO: restart here!
					unsigned int dur = params[0] << 8;
					dur += params[1];
					
					unsigned int pos[NUM_SERVOS];
					for (i = 0; i < NUM_SERVOS; i++) {
						pos[i] = params[i*2+2] << 8;
						pos[i] += params[i*2+3];
					}
					
					commandOverTime(pos,dur);
					//returnPos();
					
					
				}else if(ins == AX_WRITE_DATA){
					if(length == 4){
						ax12SetRegister(id, params[0], params[1]);
					}else{
						int x = params[1] + (params[2]<<8);
						ax12SetRegister2(id, params[0], x);
					}
					// return a packet: FF FF id Len Err params check
					/*Serial.print(0xff);
					Serial.print(0xff);
					Serial.print(id);
					Serial.print(2);
					Serial.print(0);
					Serial.print(255-((2+id)%256));
					*/
				}else if (ins == AX_WRITE_POSE) { // read most significant byte first (2 bits really)
					for (i = 0; i < 2 * NUM_SERVOS; i+=2) {
						unsigned int temp = params[i] << 8;
						temp += params[i+1];
						pose[i/2] = temp;
					}
					
					// return packet
					/*Serial.print(0xff);
					Serial.print(0xff);
					Serial.print(id);
					Serial.print(2);
					Serial.print(0);
					Serial.print(255-((2+id)%256));
					Serial.flush();
					*/
				} else { // got an invalid instruction
					Serial.print("error");
				}
			}
		}
	}
}

