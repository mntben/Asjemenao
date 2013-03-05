#TODO: test and create unit test

import nao
import fake_nao
import pioneer
import fake_pioneer
import brain
import sys
import time
import logging
import util.nullhandler
import memory

import serial


logging.getLogger('Borg.Brain.BodyController').addHandler(util.nullhandler.NullHandler())

class BodyController(object):
    """
    Controls the robots, via specific nao and pioneer objects
    (Singleton)
    """

    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(BodyController, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.logger = logging.getLogger('Borg.Brain.BodyController')
        self.memory = memory.Memory()
        self.emergency = False

    def set_config(self, param_dict):
        '''this method sets the config, and is called in the brain
        this is _not_ done in the constructor, since the behaviors construct this
        class as well, and they dont have the param_dict'''

        self.__nao_list = [] #list of the nao objects
        self.__pioneer_list = [] #list of the pioneer objects
        self.__param_dict = param_dict
        self.__create_robots()

    def get_config(self):
        return self.__param_dict

    def __del__(self):
        '''destroy the class and its data'''
        #TODO: maybe implement sometime?
        pass

    def __create_robots(self):
        '''creates the correct objects for all the robots'''

        number_of_naos = int(self.__param_dict.get_option('body','number_of_naos'))
        number_of_pioneers = int(self.__param_dict.get_option('body','number_of_pioneers'))
        
        if number_of_pioneers > 1:
            raise Exception("Currently, no more then 1 pioneer is supported!")
        
        self.logger.debug("Connecting to %d NAO(s)" % number_of_naos)
        for i in range(number_of_naos):
            ip = self.__param_dict.get_option('body','nao_ip_%d' % i)
            port = self.__param_dict.get_option('body','nao_port_%d' % i)
            self.__nao_list.append(nao.Nao(ip, port))
            self.logger.debug("Connection to NAO %d running on %s:%s made" % (i, ip, port))

        self.logger.debug("Connecting to %d Pioneer(s)" % number_of_pioneers)
        for i in range(number_of_pioneers):
            ip = self.__param_dict.get_option('body','pioneer_ip_%d' % i)
            port = self.__param_dict.get_option('body','pioneer_port_%d' % i)
            str_start_pose = self.__param_dict.get_option('body', 'pioneer_pose_%d' % i)
            if str_start_pose:
                start_pose = str_start_pose.split()
            else:
                start_pose = False
            self.__pioneer_list.append(pioneer.Pioneer(ip, port, start_pose))
            self.logger.debug("Connection to Pioneer %d running on %s:%s made" % (i, ip, port))

    def stop(self):
        for pioneer in self.__pioneer_list:
            pioneer.stop()
        for nao in self.__nao_list:
            nao.stop()
        
    def update(self):
        """
        This method is only adding the update for pioneer odometry to the memory
        """
        for pio in self.__pioneer_list:
            data = pio.update()
            if "EMERGENCY" in data:
                if not self.emergency:
                    self.emergency = True
                    self.logger.warn("Emergency button pressed on Pioneer. Setting NAO's in emergency mode")
                    for nao in self.__nao_list:
                        # Set in emergency button pressed mode
                        nao.emergency()
                        nao.emergencyLeds(True)
                    time.sleep(1)
            else:
                if self.emergency:
                    self.emergency = False
                    self.logger.warn("Emergency situation on Pioneer recovered. Re-enabling NAO's")
                    for nao in self.__nao_list:
                        nao.say("I will now resume normal operation")
                        #nao.set_stifness()
                self.add_to_memory(data)

    def add_to_memory(self, objects):
        """add a list of dictionaries describing objects to memory database"""
        if objects:
            for object in objects:
                self.memory.add_item(object['name'], object['time'], object['property_dict'])

    def nao(self, index):
        '''return the object that represents the specified nao'''
        if index >= len(self.__nao_list):
            self.logger.error("Requested unavailable NAO %d. Returning fake NAO" % index)
            return fake_nao.FakeNao("localhost")
        return self.__nao_list[index]

    def pioneer(self, index):
        '''return the object that represents the specified pioneer'''
        if index >= len(self.__pioneer_list):
            self.logger.error("Requested unavailable Pioneer %d. Returning fake Pioneer" % index)
            return fake_pioneer.FakePioneer("localhost", 12345)
        return self.__pioneer_list[index]

    def get_nr_naos(self):
        return len(self.__nao_list)

    def get_nr_pioneers(self):
        return len(self.__pioneer_list)

    def turn_head(self, angle):
        if angle > 90:
            raise Exception("Angle cannot be bigger than 90 degrees.")
        if angle < -90:
            raise Exception("Angle cannot be lower than -90 degrees.")
        try:
            ser = serial.Serial("/dev/ttyACM0", 9600)
            ser.open()
            ser.write(chr(angle + 90))
            ser.close()
        except Exception as e:
            print e


if __name__ == "__main__":
    param_dict = brain.load_config(sys.argv)

    bc = BodyController()
    bc.set_config(param_dict)

    #specify command and speed:
    speed_left = 0
    speed_right = 0
    bc.pioneer(0).set_left_right_speeds(self, speed_left, speed_right)
    #then, update the bodycontroller as many times as possible (usally done
    for i in range(10): #drive for one second
        time.sleep(0.1)
        bc.pioneer(0).set_left_right_speeds(self, speed_left, speed_right)
    bc.pioneer(0).stop_robot()
