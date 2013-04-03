import basebehavior.behaviorimplementation

import time
import random


class FindBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__nao.say("Lets find the ball!")
        self.__start_time = time.time()

        #Make sure the robot is standing and looks horizontal:
        self.__nao.start_behavior("standup")
        self.__nao.look_horizontal()

        #Possible states (WALK or TURN):
        self.__state = "WALK"
        self.__last_recogtime = time.time()



    def implementation_update(self):
        # Turn around in a certain direction unless you see the ball.
        # In that case, turn towards it until you have it fairly central in the Field of Vision.
        if (time.time() - self.__start_time) > 10:
            if self.__state == "TURN":
                if not self.__nao.isWalking():
                    self.__state = "WALK"
                    self.__nao.walkNav(random.random() * 10, 0, 0)
            elif self.__state == "WALK":
                if not self.__nao.isWalking():
                    self.__state = "TURN"
                    self.__nao.walkNav(0, 0, random.random() * 2 - 1, 0.1)

        #Try to see if there is a ball in sight:
        if (self.m.n_occurs("red.colorblob") > 0):
            (recogtime, obs) = self.m.get_last_observation("red.colorblob")
            if not obs == None and recogtime > self.__last_recogtime:
                print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['size'])
                self.__last_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if obs['size'] > 0.0015:
                    self.__nao.say("I see the ball!")
                    # Once the ball is properly found, use: self.m.add_item('ball_found',time.time(),{}) to finish this behavior.
                    self.m.add_item('ball_found',time.time(),{})
