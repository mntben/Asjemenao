import basebehavior.behaviorimplementation

import time

class Shoot_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will try to kick a ball at the Nao's feet into the goal.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.idling = False

        self.__start_time = time.time()
        self.__nao = self.body.nao(0)
        
        self.__nao.look_down()
        self.__nao.say("Kicking!")
        if (self.m.n_occurs("red.colorblob") > 0):
            (recogtime, obs) = self.m.get_last_observation("red.colorblob")
            if obs['x'] < 80:
                self.__nao.start_behavior("Asje_kick_L")
            elif obs['x'] >= 80:
                self.__nao.start_behavior("Asje_kick_R")

    def implementation_update(self):
        if self.idling:
            return

        # Simply time out after 5 seconds:
        if (time.time() - self.__start_time) > 10:
            self.__nao.say("I hope I kicked the ball.")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I kicked the ball.'})
            self.idling = True
