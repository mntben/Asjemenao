import basebehavior.behaviorimplementation

import time

class Shoot_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will try to kick a ball at the Nao's feet into the goal.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.idling = False

        self.__start_time = time.time()
        self.__nao = self.body.nao(0)
        self.__nao.start_behavior("simple_kick")

    def implementation_update(self):
        if self.idling:
            return

        # Simply time out after 5 seconds:
        if (time.time() - self.__start_time) > 10:
            self.__nao.say("I hope I kicked the ball.")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I kicked the ball.'})
            self.idling = True
