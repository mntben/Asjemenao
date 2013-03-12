import basebehavior.behaviorimplementation

import time
import random


class FindBallDefender_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__nao.say("Lets find the ball!")
        self.__start_time = time.time()
        
	if (self.m.n_occurs("sitting") > 0):
	  (sitting, sitobs) = self.m.get_last_observation("sitting")
	  self.sittingT = sitting
	
	if (self.m.n_occurs("standing") > 0):
	  (standing, standobs) = self.m.get_last_observation("standing")
	  self.standingT = standing
	 

        #Make sure the robot is standing and looks horizontal:
        if (self.m.n_occurs("sitting") > 0) and (self.m.n_occurs("standing") > 0):
	  if not self.__nao.isMoving() and (self.m.n_occurs("sitting") > 0) and ( self.sittingT > self.standingT ):
	    self.__nao.start_behavior("standup")
	    self.m.add_item('standing',time.time(),{})
	  
        self.__nao.look_horizontal()
        self.__walkback = False
        
        #Possible states (WALK or TURN):

        self.__last_recogtime = time.time()



    def implementation_update(self):
	if not self.__nao.isMoving() and self.__walkback == False:
	  self.__nao.walkNav(-0.1, 0, 0)
	  self.__walkback = True
	
        # Turn around in a certain direction unless you see the ball.
        # In that case, turn towards it until you have it fairly central in the Field of Vision.
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
                    
        elif not self.__nao.isMoving() and (self.m.n_occurs("sitting") > 0) and ( self.sittingT > self.standingT ):
	  self.__nao.start_behavior("standup")