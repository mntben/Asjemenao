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

        #Make sure the robot is standing and looks horizontal:
        self.__nao.complete_behavior("standup")
        self.__nao.look_horizontal()
        self.__nao.look_up()
        self.__walkback = False
        self.__state = "Middle"
        
        
        #Possible states (WALK or TURN):

        self.__last_recogtime = time.time()



    def implementation_update(self):
		if not self.__nao.isMoving() and self.__walkback == False:
			self.__nao.walkNav(-0.1, 0, 0)
			self.__walkback = True
		  
		if not self.__nao.isMoving() and self.__walkback == True:
			if self.__state == "Middle":
				self.__nao.look_left()
				self.__state = "Left"
			elif self.__state == "Left":
				self.__nao.look_horizontal()
				self.__nao.look_right()
				self.__state = "Right"
			elif self.__state == "Right":
				self.__nao.look_down()
				self.__state = "Right_down"	
			elif self.__state == "Right_down":
				self.__nao.look_horizontal()
				self.__state = "Middle_down"
			elif self.__state == "Middle_down":
				self.__nao.look_left()
				self.__state = "Left_down"	
			elif self.__state == "Left_down":
				self.__nao.look_forward()
				self.__nao.look_up()
				self.__state = "Middle"			
	  
		# Turn around in a certain direction unless you see the ball.
		# In that case, turn towards it until you have it fairly central in the Field of Vision.
		#Try to see if there is a ball in sight:
		if (self.m.n_occurs("combined_red") > 0):
			(recogtime, obs) = self.m.get_last_observation("combined_red")
			contours = obs["sorted_contours"]
			biggest_blob = contours[0]            
			if not biggest_blob == None and recogtime > self.__last_recogtime:
				print "red: x=%d, y=%d, size=%f" % (biggest_blob['x'], biggest_blob['y'], biggest_blob['surface'])
				self.__last_recogtime = recogtime
				#Ball is found if the detected ball is big enough (thus filtering noise):
				if biggest_blob['surface'] > 100:
					self.__nao.say("I see the ball!")
					# Once the ball is properly found, use: self.m.add_item('ball_found',time.time(),{}) to finish this behavior.
					self.m.add_item('ball_found',time.time(),{})
