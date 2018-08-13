#include <CommandHandler.h>
#include <CommandManager.h>
CommandManager cmdMng;

#include <AccelStepper.h>
#include <LinearAccelStepperActuator.h>
#include <CommandLinearAccelStepperActuator.h>

AccelStepper stp_P(AccelStepper::DRIVER, 37, 39);
CommandLinearAccelStepperActuator P(stp_P, 2, 35);

void setup()
{
  Serial.begin(115200);

  P.registerToCommandManager(cmdMng, "P");

  cmdMng.init();
}

void loop()
{
  cmdMng.update();
}
