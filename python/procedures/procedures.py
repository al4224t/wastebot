"""
    coding: UTF-8
    Python 2.7

    procedures.py

    Created 07/06/2016
    Kevin Donkers, The Cronin Group, University of Glasgow

    Experimental procedures combining functions from Robot and Sensor classes
    Each Procedure class contains a set of functions for specific experiments
"""
# system imports
import os
import sys
import inspect
import time

# add root path to access project modules
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT_PATH = os.path.join(HERE_PATH, '..')
sys.path.append(ROOT_PATH)

# project modules
from robot.robot import Robot
#from sensors.sensors import Sensors

# logging
import logging
logging.basicConfig(level=logging.INFO)

# defauls parameters
DEFAULT_OD_WAIT = 60 #seconds

class Procedures(object):
    '''Procedures common to all procedure classes (inherited by subsiquent classes)'''
    def __init__(self, robot_configfile):
        self.robot = Robot.from_configfile(robot_configfile)
        #self.sensors = Sensors()

    def load_wellplate_volume_list(self, volumes, reservoir, wellplate='wellplate1', pipette='pipette1', tiprack=None):
    	'''Aspirates and dispenses each volume into well until end of volumes list'''
    	self.robot.change_tip()
    	for i in range(len(volumes)):
            self.robot.aspirate_from_reservoir(reservoir, volumes[i], pipette)
            self.robot.dispense_to_well('current', wellplate, volume[i], pipette)
            if tiprack:
                self.robot.change_tip(pipette, tiprack)
            self.robot.next_well(wellplate)

    def load_wellplate_fully(self, initial_volume, volume, reservoir='medium', wellplate='wellplate1', pipette='pipette1', tiprack='tiprack1'):
    	'''Aspirates inital_volume then dispenses volume into each well in wellplate'''
        n_wells = self.robot.wellplates[wellplate][0][0] * self.robot.wellplates[wellplate][0][1]
        self.robot.change_tip(pipette, tiprack)
    	current_volume = 0
    	self.robot.aspirate_from_reservoir(reservoir, initial_volume, pipette)
    	current_volume = initial_volume
    	for well in n_wells:
            if current_volume > (volume + 5):
                self.robot.dispense_to_well('current', wellplate, volume, pipette)
                self.robot.next_well(wellplate)
                current_volume = current_volume - volume
            else:
                self.robot.change_tip()
                self.robot.aspirate_from_reservoir(reservoir, initial_volume, pipette)
                self.robot.dispense_to_well('current', wellplate, volume, pipette)
                self.next_well(wellplate)
                current_volume = inital_volume - volume
        print "Wellplate loaded"

    def measure_od_to_limit(self, od_limit, wait_time=DEFAULT_OD_WAIT):
        '''Measures OD continuously using sensor until od_limit achieved'''
        limit_reached = False
        while limit_reached == False:
            self.sensors.measure_OD()
            if self.sensors.avOD >= od_limit:
                limit_reached = True
            else:
                time.sleep(wait_time)
        return self.sensors.avOD

    def wait_for_user_input(self, message, continuation_condition):
        '''Wait for user input before proceeding'''
        proceed = False
        while proceed==False:
            user = raw_input(message)
            if user.lower() == continuation_condition.lower():
                proceed = True
            else:
                print "Response {} not recognised".format(user)
                proceed = False


class DummyExperiment(Procedures):
	''' Dummy procedure to test experiments without robot conducting actual experiment'''
	def perform_experiment(self, command):
		if command:
			return "Command {} received: Experiment performed".format(command)
		else:
			return "Command empty: Experiment not performed"


class Experiment1(Procedures):
    '''Mixing two cultures in one medium then measuring time to achieve OD limit'''
    # Names of components in this experiment
    MEDIUM = 'medium'
    CULTURE1 = 'culture1'
    CULTURE2 = 'culture2'
    WELLPLATE = 'wellplate1'
    PIPETTE = 'pipette1'
    TIPRACK = 'tiprack1'
    # Perform experiment, given culture_formulations as a dictionary of lists and od_limit as a scalar
    def perform_experiment(self, culture_formulations, od_limit):
        # Extract lists of volumes from culture_formulations
        medium = culture_formulations[MEDIUM]
        culture1 = culture_formulations[CULTURE1]
        culture2 = culture_formulations[CULTURE2]
        # Load wellplate with different volumes of culture1, without changing tips
        self.load_wellplate_volume_list(volumes=culture1, reservoir=CULTURE1, wellplate=WELLPLATE, pipette=PIPETTE)
        # Load each well with different volumes of culture2, changing tips each times
        self.load_wellplate_volume_list(volumes=culture2, reservoir=CULTURE2, wellplate=WELLPLATE, pipette=PIPETTE, tiprack=TIPRACK)
        # Load same volume of medium to all wells
        self.load_wellplate_fully(initial_volume=medium[0], volume=medium[1], reservoir=MEDIUM, wellplate=WELLPLATE, pipette=PIPETTE, tiprack=TIPRACK)
        # Home robot to allow user access
        self.robot.z.home()
        self.robot.xy.home()
        # Wait for user to place sensor lid on wellplate
        self.wait_for_user_input('Place lid onto sensor then press (y) to continue.', 'y')
        # Set experiment start time
        start_time = time.time()
        # Measure OD until od_limit achieved
        self.measure_od_to_limit(od_limit,DEFAULT_OD_WAIT)
        # Return time it took to achieve od_limit
        return time.time-start_time


class Experiment2(Procedures):
    '''Mixing one culture in two media then measuring time to achieve OD limit'''
    # Names of components in this experiment
    MEDIUM1 = 'medium1'
    MEDIUM2 = 'medium2'
    CULTURE = 'culture'
    WELLPLATE = 'wellplate1'
    PIPETTE = 'pipette1'
    TIPRACK = 'tiprack1'
    # Perform experiment, given culture_formulations as a dictionary of lists and od_limit as a scalar
    def perform_experiment(self, culture_formulations, od_limit):
        # Extract lists of volumes from culture_formulations
        medium1 = culture_formulations[MEDIUM1]
        medium2 = culture_formulations[MEDIUM2]
        culture = culture_formulations[CULTURE]
        # Load wellplate with different volumes of medium1, without changing tips
        self.load_wellplate_volume_list(volumes=medium1, reservoir=MEDIUM1, wellplate=WELLPLATE, pipette=PIPETTE)
        # Load each well with different volumes of medium2, changing tips each times
        self.load_wellplate_volume_list(volumes=medium2, reservoir=MEDIUM2, wellplate=WELLPLATE, pipette=PIPETTE, tiprack=TIPRACK)
        # Load same volume of culture to all wells
        self.load_wellplate_fully(initial_volume=culture[0], volume=culture[1], reservoir=CULTURE, wellplate=WELLPLATE, pipette=PIPETTE, tiprack=TIPRACK)
        # Home robot to allow user access
        self.robot.z.home()
        self.robot.xy.home()
        # Wait for user to place sensor lid on wellplate
        self.wait_for_user_input('Place lid onto sensor then press (y) to continue.', 'y')
        # Set experiment start time
        start_time = time.time()
        # Measure OD until od_limit achieved
        self.measure_od_to_limit(od_limit,DEFAULT_OD_WAIT)
        # Return time it took to achieve od_limit
        return time.time-start_time
