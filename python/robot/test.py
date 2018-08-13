import os
import sys
import inspect
import json

# add robot path to access files within same folder as robot.py
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


from commanduino import CommandManager
from commanduino.devices.axis import Axis, MultiAxis
from pipette import Pipette


test_config = os.path.join(HERE_PATH, 'test_config.json')

cmdMng = CommandManager.from_configfile(test_config)


p_axis = Axis(cmdMng.P, 0.763/8, 0, 100)

p = Pipette(p_axis, 0, 100)
