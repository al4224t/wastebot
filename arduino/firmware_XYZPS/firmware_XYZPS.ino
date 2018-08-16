
#include <CommandHandler.h>
#include <CommandManager.h>
CommandManager cmdMng;

#include <AccelStepper.h>
#include <LinearAccelStepperActuator.h>
#include <CommandLinearAccelStepperActuator.h>

//AccelStepper stp_X(AccelStepper::DRIVER, 54, 55);
//CommandLinearAccelStepperActuator X(stp_X, 3, 38);

//AccelStepper stp_Y(AccelStepper::DRIVER, 60, 61);
//CommandLinearAccelStepperActuator Y(stp_Y, 14, 56);

//AccelStepper stp_Z(AccelStepper::DRIVER, 46, 48);
//CommandLinearAccelStepperActuator Z(stp_Z, 18, 62);

//26 = E0 STEP, 28 = E0 DIR, 19 = ZMAX, 24 = E0 EN
AccelStepper stp_P(AccelStepper::DRIVER, 26, 28);
CommandLinearAccelStepperActuator P(stp_P, 19, 24);

//36 = E1 STEP, 34 = E1 DIR, 2 = XMAX, 30 = E1 EN
//AccelStepper stp_S(AccelStepper::DRIVER, 36, 34);
//CommandLinearAccelStepperActuator S(stp_S, 2, 30); 

void setup()
{

  Serial.begin(115200);

  //X.registerToCommandManager(cmdMng, "X");
  //Y.registerToCommandManager(cmdMng, "Y");
  //Z.registerToCommandManager(cmdMng, "Z");
  P.registerToCommandManager(cmdMng, "P");
  //S.registerToCommandManager(cmdMng, "S");

  cmdMng.init();
}

void loop()
{
  cmdMng.update();
}
