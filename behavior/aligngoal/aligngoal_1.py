import basebehavior.behaviorimplementation

import time
import almath

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal in in a line.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.idling = False

        self.__start_time = time.time()

        self.__nao = self.body.nao(0)
        self.__nao.say("Aligning with goal!")
        self.__state = "FIND"
		self.__checked = False
		
        self.__nao.look_forward()
		
		# With a yellow goal:
		while self.__checked is False:
			if (self.m.n_occurs("combined_yellow") > 0):
				(recogtime, obs) = self.m.get_last_observation("combined_yellow")
				if not obs == None and recogtime > self.__last_ball_recogtime:
					contours = obs["sorted_contours"]
					biggest_blob = contours[0]
					print "%s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
							% ("yellow", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
					self.__last_recogtime = recogtime
					
					# Goal is found if the detected blob is big enough (thus filtering noise)
					if biggest_blob['width'] < 80 and biggest_blob['height'] > 100:
						print "Goal Detected"
						if self.__state == "FIND":
							self.__nao.say("In front of the goal")						
						elif self.__state == "FIND_RIGHT":
							self.__nao.say("Possibly turning to the goal")
							self.__nao.walkNav(0.15,0.12,-((45 * almath.TO_RAD)+((biggest_blob['x']-80)*(-0.005))))
							self.__nao.look_forward()
						elif self.__state == "FIND_LEFT":
							self.__nao.say("Possibly turning to the goal")
							self.__nao.walkNav(0.15,0.12,((45 * almath.TO_RAD)+((biggest_blob['x']-80)*(-0.005))))
							self.__nao.look_forward()
			else:
				if self.__state == "FIND":
					self.__nao.look_right()
					self.__state = "FIND_RIGHT"
					self.__nao.say("Looking Right")
				elif self.__state == "FIND_RIGHT":
					self.__nao.look_forward()
					self.__nao.look_left()
					self.__state = "FIND_LEFT"
					self.__nao.say("Looking left")
				elif self.__state == "FIND_LEFT":
					# Dit moet nog beter, en waarschijnlijk op een andere plek:
					self.__nao.say("Maybe the goal is on the other side?")
					self.__checked = True
					self.__nao.walkNav(0.3,0.2,(180 * almath.TO_RAD))
					self.__nao.look_forward()	


    def implementation_update(self):
        if self.idling:
            return
        
        #TODO: Remove the following with the steps mentioned below (e.d. align the robot so that it can kick the ball in the direction of the goal):
        #It now simply assumes that it is already aligned:
        if not self.__nao.isMoving(): 
            if (time.time() - self.__start_time) > 20:
                self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
                self.idling = True
            self.m.add_item('goal_aligned',time.time(),{})    
            
        # If the ball and the goal are both in sight, check if they are in line with each other.
        # If they are aligned, use self.m.add_item('goal_aligned',time.time(),{}) to finish this behavior.
        # Else, turn to align them.
        # If the ball is in sight but the goal is not, strafe/circle in a single direction, keeping the ball in sight.

        # TODO: Remove simple timeout with:
        # Check if you can see the ball. If you can't, go idle so the structure resets.
        #~ if not self.__nao.isWalking() and (time.time() - self.__start_time) > 5:
            #~ self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            #~ self.idling = True

