#include <CommandHandler.h>
#include <CommandManager.h>
CommandManager cmdMng;

#include <CommandAnalogRead.h>
#include <CommandAnalogWrite.h>

namespace heater0{
  int PID = 8; // pin ID of heater0.
  char command_id[] = "WHB0"; // command ID of heater0.
};

namespace thermistor0{
  int PID = 13; // pin ID of thermistor0.
  char command_id[] = "RTM0"; // command ID of thermistor0.
};

namespace thermistor1{
  int PID = 14; // pin ID of thermistor1.
  char command_id[] = "RTM1"; // command ID of thermistor1.
};

namespace thermistor2{
  int PID = 15; // pin ID of thermistor2.
  char command_id[] = "RTM2"; // command ID of thermistor2.
};

CommandAnalogRead cmdReadThermistor0(thermistor0::PID);
CommandAnalogRead cmdReadThermistor1(thermistor1::PID);
CommandAnalogRead cmdReadThermistor2(thermistor2::PID);
CommandAnalogWrite cmdWriteHeatbed0(heater0::PID);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); // start serial communication
  cmdReadThermistor0.registerToCommandManager(cmdMng, thermistor0::command_id);
  cmdReadThermistor1.registerToCommandManager(cmdMng, thermistor1::command_id);
  cmdReadThermistor2.registerToCommandManager(cmdMng, thermistor2::command_id);
  cmdWriteHeatbed0.registerToCommandManager(cmdMng, heater0::command_id);

  cmdMng.init();
}

void loop() {
  // put your main code here, to run repeatedly:
  cmdMng.update();
}
