#include <CommandHandler.h>
#include <CommandManager.h>
CommandManager cmdMng;

#include <AccelStepper.h>
#include <LinearAccelStepperActuator.h>
#include <CommandLinearAccelStepperActuator.h>

//AccelStepper stp_X(AccelStepper::DRIVER, 54, 55);
//CommandLinearAccelStepperActuator X(stp_X, 3, 38);
//
//AccelStepper stp_Y(AccelStepper::DRIVER, 60, 61);
//CommandLinearAccelStepperActuator Y(stp_Y, 14, 56);
//
//AccelStepper stp_Z(AccelStepper::DRIVER, 46, 48);
//CommandLinearAccelStepperActuator Z(stp_Z, 18, 62);

AccelStepper stp_P(AccelStepper::DRIVER, 37, 39);
CommandLinearAccelStepperActuator P(stp_P, 2, 35);

void setup()
{
  Serial.begin(115200);

//  X.registerToCommandManager(cmdMng, "X");
//  Y.registerToCommandManager(cmdMng, "Y");
//  Z.registerToCommandManager(cmdMng, "Z");
  P.registerToCommandManager(cmdMng, "P");

  cmdMng.init();
}

void loop()
{
  cmdMng.update();
}
