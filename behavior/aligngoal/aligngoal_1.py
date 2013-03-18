import basebehavior.behaviorimplementation

import time
import almath

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal in in a line.'''

    #this implementation should not define an __init__ !!!
    
    __state = "FIND"
    __lookuptime = 0


    def implementation_init(self):
        self.idling = False

        self.__start_time = time.time()

        self.__nao = self.body.nao(0)
        self.__nao.say("Aligning with goal!")
        print "Aligning!"
        
        self.__checked = False
        self.__nao.look_forward()
        self.__last_ball_recogtime = 0
        self.__greenturn = False
        
        # With a self.target_goal goal:
        while self.__checked is False:
            if self.timeout() is True:
                return
            self.__last_ball_recogtime = time.time()
            if (self.m.n_occurs("combined_"+self.target_goal) > 0):
                (recogtime, obs) = self.m.get_last_observation("combined_"+self.target_goal)
                if not obs == None and recogtime > self.__last_ball_recogtime:
                    contours = obs["sorted_contours"]
                    biggest_blob = contours[0]
                        
                    print "%s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                        % (self.target_goal, biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
                    self.__last_recogtime = recogtime
                    # Goal is found if the detected blob is big enough (thus filtering noise)
                    if biggest_blob['height'] > 20 and biggest_blob['surface'] > 300:
                        print "One blob Detected"
                        if AlignGoal_x.__state == "FIND":       
                            if len(contours) > 1:
                                second_biggest_blob = contours[1]  
                                print "Second biggest %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                                    % (self.target_goal, second_biggest_blob['x'], second_biggest_blob['y'], second_biggest_blob['width'], second_biggest_blob['height'], second_biggest_blob['surface'])
                                if biggest_blob['height'] > 10 and biggest_blob['surface'] > 100:
                                    print "Goal Detected"
                                    self.__checked = True
                                    self.__nao.say("In front of the goal")
                                    self.m.add_item('goal_aligned',time.time(),{})
                            else:
                                AlignGoal_x.__state = "FIND_RIGHT"
                        elif AlignGoal_x.__state == "FIND_RIGHT":
                            self.__nao.say("Turning right")
                            self.__nao.walkNav(0.15, 0.15,-(1.570), 0.01)
                            self.__nao.look_forward()
                            AlignGoal_x.__state = "FIND"
                        elif AlignGoal_x.__state == "FIND_LEFT":
                            self.__nao.say("Turning left")
                            self.__nao.walkNav(0.15, -(0.15), 0.78, 0.01)
                            self.__nao.look_forward()
                            AlignGoal_x.__state = "FIND"
                        #~ elif AlignGoal_x.__state == "FIND_UP":
                            #~ self.__nao.look_forward()
                            #~ self.__nao.useBottomCamera()
                            #~ AlignGoal_x.__state = "FIND" 
                    #~ elif self.m.n_occurs("combined_green") > 0:
                        #~ (recogtime, obs) = self.m.get_last_observation("combined_green")
                        #~ if not obs == None and recogtime > self.__last_ball_recogtime:
                            #~ contours = obs["sorted_contours"]
                            #~ biggest_blob = contours[0]
                            #~ if biggest_blob['height'] > 10 and biggest_blob['surface'] > 200:
                                #~ print "Green marker seen.. moving to the right!"
                                #~ self.__nao.walkNav(0.15, 0.15,-(1.570), 0.01)
                                #~ self.__greenturn = True
                        #~ elif AlignGoal_x.__state == "FIND_UP" and self.__greenturn == True:
                            #~ self.__checked = True
                            #~ self.__nao.say("Kicking, whooo")
                            #~ self.__nao.useBottomCamera()
                            #~ self.m.add_item('goal_aligned',time.time(),{})                           
                        #~ else:
                            #~ self.find_goal()
                    #~ elif AlignGoal_x.__state == "FIND_UP" and self.__greenturn == True:
                        #~ self.__checked = True
                        #~ self.__nao.say("Kicking, whooo")
                        #~ self.__nao.useBottomCamera()
                        #~ self.m.add_item('goal_aligned',time.time(),{})                            
                    else:
						print "Blob not big enough"
						self.find_goal()                  
            else:
                self.find_goal()	

    def find_goal(self):
        #~ if AlignGoal_x.__state == "FIND":
            #~ self.__nao.useTopCamera()
            #~ AlignGoal_x.__lookuptime = time.time()
            #~ self.__nao.say("Looking up")
            #~ AlignGoal_x.__state = "FIND_UP"
        if AlignGoal_x.__state == "FIND":
            #self.__nao.useBottomCamera()
            self.__nao.look_right()
            AlignGoal_x.__state = "FIND_RIGHT"
            self.__nao.say("Looking Right")
        elif AlignGoal_x.__state == "FIND_RIGHT":
            self.__nao.look_forward()
            self.__nao.look_left()
            AlignGoal_x.__state = "FIND_LEFT"
            self.__nao.say("Looking left")
        elif AlignGoal_x.__state == "FIND_LEFT":
            self.__nao.look_forward()
            self.__nao.look_right()
            AlignGoal_x.__state = "FIND"
            self.__nao.say("Looking forward and turning right")
            self.__nao.walkNav(0.15, 0.15,-(1.570), 0.01)  

    def timeout(self):
        if not self.__nao.isMoving(): 
            #print "Not moving.."
            if (time.time() - self.__start_time) > 10:
                print "Just kicking"
                #self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
                self.idling = True
                self.m.add_item('goal_aligned',time.time(),{})
                return True
        else:
            print "Moving.."
            return False
            

    def implementation_update(self):
        print "UPDATE"
        if self.idling:
            return
        
        #TODO: Remove the following with the steps mentioned below (e.d. align the robot so that it can kick the ball in the direction of the goal):
        #It now simply assumes that it is already aligned:
        if not self.__nao.isMoving(): 
            print "Not moving.."
            if (time.time() - self.__start_time) > 10:
                print "Just kicking"
                #self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
                self.idling = True
                self.m.add_item('goal_aligned',time.time(),{})
        else:
            print "Still moving"
            
        # If the ball and the goal are both in sight, check if they are in line with each other.
        # If they are aligned, use self.m.add_item('goal_aligned',time.time(),{}) to finish this behavior.
        # Else, turn to align them.
        # If the ball is in sight but the goal is not, strafe/circle in a single direction, keeping the ball in sight.

        # TODO: Remove simple timeout with:
        # Check if you can see the ball. If you can't, go idle so the structure resets.
        #~ if not self.__nao.isWalking() and (time.time() - self.__start_time) > 5:
            #~ self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            #~ self.idling = True

