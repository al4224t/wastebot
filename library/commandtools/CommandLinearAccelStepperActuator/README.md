# CommandLinearAccelStepperActuator

Device bonjour id is ```LINEARACCELSTEPPER```

## Incoming

| Command ID | operand(s) | Action |
|:-:|---|---|
|```SP```| ```int``` position (step) | Set Current Position |
|```SS```| ```float``` stepsPerSecond | Set stepper speed|
|```SMS```| ```float```stepsPerSecond| Set stepper maxspeed|
|```SA```| ```float```stepsPerSecondPerSecond| Set stepper acceleration|
|```EA```| | Enable Acceleration Mode|
|```DA```| | Disable Acceleration Mode|
|```ES```| | Enable Switch Revert Mode|
|```DS```| | Disable Switch Revert Mode|
|```H```| | Go home (using last set speed)|
|```MT```| ```int``` steps | Move to absolute steps|
|```M```| ```int``` steps | Move relative steps|
|```S```| | Stop the stepper|
|```RS```| | Request switch state <br> Send back ```S``` command|
|```RM```| | Request moving status <br> Send back ```M``` command|
|```RD```| | Request distance to go <br> Send back ```D``` command|
|```RT```| | Request target position <br> Send back ```T``` command|
|```RP```| | Request current position <br> Send back ```P``` command|
|```RIS```| | Request set speed <br> Send back ```IS``` command|
|```RIMS```| | Request set max speed <br> Send back ```IMS``` command|
|```RIA```| | Request set acceleration <br> Send back ```IA``` command|


## Outgoing

| Command ID | operand(s) | Action |
|:-:|---|---|
|```S```| ```bool``` [0,1]| Switch state|
|```M```| ```bool``` [0,1]| Is the stepper moving|
|```D```| ```int``` steps | Steps to target |
|```T```| ```int``` steps | Target position |
|```P```| ```int``` steps | Current Position|
|```IS```| ```float``` stepsPerSecond | Internal speed |
|```IMS```| ```float``` stepsPerSecond | Internal maxspeed |
|```IA```| ```float``` stepsPerSecondPerSecond | Internal Acceleration|
