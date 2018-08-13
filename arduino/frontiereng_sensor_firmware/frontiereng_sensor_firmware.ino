// ==========================================================================
//                                                                                      Time-stamp: <Mon May 16 18:52:45 GMT Daylight Time 2016>
//   mstat_firmware.ino
//
//   by Soichiro Tsuda, Cronin Group, University of Glasgow                                                                                                                               
//                                                                                                                                                  
//   Description: 
//     Firmware for Turbidostat for E.coli morbidostat control. 
//     This version is designed for Morbidostat 2, which requires waste pump BT100S-1 
//     with DG6-16 (16ch channel head).     
//                                                                                                                                                                                   
//   Hardware requirements:                                                                                                                                                           
//        - Arduino Mega, or equivalent 
//        - DC-motor controlled peristaltic pumps
//                                                                                                                                                                                    
//    Software requirements: 
//        - Serial command processing library 
//            -- Download from https://github.com/kroimon/Arduino-SerialCommand
//            -- How to install library http://arduino.cc/en/Guide/Libraries
// 
// 
// ========================================================================== 


#include <SerialCommand.h>

// SerialCommand object
SerialCommand sCmd; 

// duraton of delay (default: 1 min = 60,000ms)
unsigned long delay_duration = 1000;

// define the number of iteration for sensor measurement
int numIteration = 10;

// definite loop variable for sensor measurement
int c, i; 

// Circulation pump control:
//   read potentiometer value and set speed from a PWM pin
// circ. pump mode:
//  0: digital control from PC
//  1: analog control using potentiometer
int cpump_mode = 1; 
int potValue;

void setup() {
/*
    One of the two needed methods for an Arduino.
    This is run exactly once, when the Arduino reset (reset button, power on, new firmware).
*/
    // start serial connection with baud rate of 115200
    Serial.begin(115200);

    // For sensor readings. All pins to input
    //pinMode(A0, INPUT);
    pinMode(A0, OUTPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);
    pinMode(A4, INPUT);
    pinMode(A5, INPUT);    
    pinMode(A6, INPUT);
    pinMode(A7, INPUT);    
    pinMode(A8, INPUT);    
    pinMode(A9, INPUT);    
    pinMode(A10, INPUT);    
    pinMode(A11, INPUT);    
    pinMode(A12, INPUT);    
    pinMode(A13, INPUT);    
    pinMode(A14, INPUT); 
    pinMode(A15, INPUT); 

    // For digital output 
    for (i = 0; i < 54; i++) { 
      pinMode(i, OUTPUT);
      digitalWrite(i, 0);
    }

    // Setup callbacks for SerialCommand commands
    sCmd.addCommand("MEASURE", readSensorAll); // Read voltage values from all the sensors (16 ch)
    sCmd.addCommand("READS", readSpecificSensor); // Read voltage values from each sensor
    sCmd.addCommand("READCONT", readSpecificSensorContinuously); // Read voltage values from each sensor
    sCmd.addCommand("PUMP", pumpCtrl); // Turn on/off peristaltic pump 
    sCmd.addCommand("PWM", pwmCtrl); // Analog output with PWM
    sCmd.addCommand("RELAY", relayCtrl); // Turn on/off relay to control waste pump (BT100S-1)
    sCmd.addCommand("ALLOFF", allPumpOff); // Turn on/off peristaltic pump 
    sCmd.addCommand("ALLON", allPumpOn); // Turn on/off peristaltic pump 
    sCmd.setDefaultHandler(unrecognized); // Handler for command that isn't matched (says "What?")
    // abbreviated commands
    sCmd.addCommand("M", readSensorAll); 
    //sCmd.addCommand("R", readSpecificSensor); 
    sCmd.addCommand("P", pumpCtrl); 
    sCmd.addCommand("F", pwmCtrl); 
    sCmd.addCommand("R", relayCtrl);
}

void loop() {
  
  sCmd.readSerial(); // We don't do much, just process serial commands

}

void readSpecificSensorContinuously() {    
  //
  //  Syntax: READS <sensor no1> 
  //   e.g. "READCONT 4 " (read #4 sensor continuously)
  //  Note that sensor numbers are #0-7. Same as Analog In numbers. 
  //
  //Serial.println("Reading specific sensor");
  int sNum; // sensor number 
  char *arg;
  int loop_count = 0;

  arg = sCmd.next();
  sNum = atoi(arg);

  while(1) {
    // initialise buffer variable
    unsigned long voltagebuff = 0; 
    
    // call analogRead once to switch the pin to the ADC.
    // this will help the measurement accurate and consistent. 
    // see http://forums.adafruit.com/viewtopic.php?f=25&t=11597
    analogRead(54+sNum);  
    delay(1);
    
    // read sensor <numIteration> times 
    for (c = 0; c <= numIteration; c++) {
      // Read from A0-A7. 
      // pin assignments are A0=54, A1=55, and so on. See c:/Program Files (x86)/Arduino/hardware/arduino/variants/mega/pins_arduino.h for details.
      voltagebuff += analogRead(54+sNum);  
      delayMicroseconds(1);
      //delay(1);
    }  
    delay(5);
    // return averaged value
    Serial.print(voltagebuff/numIteration, DEC);
    Serial.print(" ");  
    Serial.println(loop_count, DEC);
    loop_count = loop_count + 1;
    // pause for some time 
    delay(delay_duration);
  }
}



void readSpecificSensor() {    
  //
  //  Syntax: READS <sensor no1> [sensor no2, ....]
  //   e.g. "READS 0 4 5 7" (read #0,4,5,7 sensors)
  //  Note that sensor numbers are #0-7. Same as Analog In numbers. 
  //
  //Serial.println("Reading specific sensor");
  int sNum; // sensor number 
  char *arg;

  arg = sCmd.next();
  while(arg != NULL) {
    sNum = atoi(arg);

    // initialise buffer variable
    unsigned long voltagebuff = 0; 

    // call analogRead once to switch the pin to the ADC.
    // this will help the measurement accurate and consistent. 
    // see http://forums.adafruit.com/viewtopic.php?f=25&t=11597
    analogRead(54+sNum);  
    delay(1);

    // read sensor <numIteration> times 
    for (c = 0; c <= numIteration; c++) {
      // Read from A0-A7. 
      // pin assignments are A0=54, A1=55, and so on. See c:/Program Files (x86)/Arduino/hardware/arduino/variants/mega/pins_arduino.h for details.
      voltagebuff += analogRead(54+sNum);  
      delayMicroseconds(1);
      //delay(1);
    }  
    delay(5);
    // return averaged value
    Serial.print(voltagebuff/numIteration, DEC);
    //Serial.print(" ");  
    arg = sCmd.next();
  }
  //Serial.print("\n");  

}

void readSensorAll() {
  //
  //  Syntax:  "MEASURE" (No parameter. Read all 8 analog inputs)
  // 

  for (i = 0; i < 16; i++) { 
    // initialise buffer variable
    unsigned long voltagebuff = 0; 

    // call analogRead once to switch the pin to the ADC.
    // this will help the measurement accurate and consistent. 
    // see http://forums.adafruit.com/viewtopic.php?f=25&t=11597
    analogRead(54+i);  
    delay(1);

    // read sensor <numIteration> times 
    for (c = 0; c <= numIteration; c++) {
      // Read from A0-A7. 
      // pin assignments are A0=54, A1=55, and so on. See c:/Program Files (x86)/Arduino/hardware/arduino/variants/mega/pins_arduino.h for details.
      voltagebuff += analogRead(54+i);  
      delayMicroseconds(1);
      //delay(1);
    }  
    // return averaged value
    Serial.println(voltagebuff/numIteration, DEC);
    //Serial.print(" ");  
  }
  //Serial.print("\n");  
}

void pumpCtrl() {
  //
  //  Syntax: PUMP <pin no.> <1/0>
  //     e.g. "PUMP 28 1" (turn on a waster pump connected to pin 28)
  //

  int pNum; // waste pump number 
  int pState; // pump state 
  char *arg;
  int readOK; 
  
  //Serial.println("We're in processCommand");

  // read pump number 
  arg = sCmd.next();
  if (arg != NULL) {
    pNum = atoi(arg); // N-th pump (N=0-8?)
    
    // read pump state
    arg = sCmd.next();
    if (arg != NULL) {
      pState = atoi(arg); // 0 or 1
      
      // set pump state 
     digitalWrite(pNum, pState); 
    }
  }
}

void allPumpOff() {
  //
  //  Syntax: ALLOFF (no arguments)
  //
    for (i = 0; i < 54; i++) { 
      digitalWrite(i, LOW);
    }
}

void allPumpOn() {
  //
  //  Syntax: ALLON (no arguments)
  //
    for (i = 0; i < 54; i++) { 
      digitalWrite(i, HIGH);
    }
}

void pwmCtrl() {
  //
  //  Syntax: PWM <pin no.> <pwm level>
  //     e.g. "PWM 13 155 " (Set a pwm level connected to pin 13 to 155)
  //     Note: <PWM level> takes 0-255
  //
  int pwmNum;
  int pwmLevel;
  char *arg;  

  // read PWM channel number 
  arg = sCmd.next();
  if (arg != NULL) {
    pwmNum = atoi(arg); // N-th pump (N=0-8?)
    
    // read pwm level
    arg = sCmd.next();
    if (arg != NULL) {
      pwmLevel = atoi(arg); // Converts a char string to an integer
      //char outputMessage[50];
      //snprintf(outputMessage, 50, "Setting pwm level for pin%d to %d.", pwmNum, pwmLevel);
      //Serial.println(outputMessage);      
      analogWrite(pwmNum, pwmLevel);
    }
  }
}

void relayCtrl() {
  //
  //  Syntax: RELAY <pin no.>
  //     e.g. "RELAY 13" (Send a HIGH signal to the designated pin followed by LOW signal immediately)
  //
  int pNum;
  char *arg;  

  // read pin number 
  arg = sCmd.next();
  if (arg != NULL) {
    pNum = atoi(arg); 
  }
  
  // set pin state 
  digitalWrite(pNum, 0);
  Serial.println("turned pin LOW");
  delay(100); 
  digitalWrite(pNum, 1); 
  Serial.println("turned pin HIGH");

}


// This gets set as the default handler, and gets called when no other command matches.
void unrecognized(const char *command) {
  Serial.println("What?");
}
