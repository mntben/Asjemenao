import basebehavior.behaviorimplementation

import time
import random
import almath
import math

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__start_time = time.time()   
        self.idling = False        
        self.__state = "F1"  
        self.__approaching = 'void'  
        self.__nao.say("Align!")
        print "Target goal: "  + self.target_goal
        print "Own goal: "  + self.own_goal
        self.__is_looking_horizontal = True

    def implementation_update(self):   
        if self.idling:
            return    
        
        if not self.__nao.isMoving(): 
            if (time.time() - self.__start_time) > 30:
                print "Just kicking (timer expired)"
                self.idling = True
                self.m.add_item('goal_aligned',time.time(),{})
                
        if self.__state == "F1":
            self.__nao.look_up()
            self.check_blobs()
        elif self.__state == "F2":
            self.__nao.look_left()
            self.check_blobs()
        elif self.__state == "F3":
            self.__nao.look_horizontal()
            self.__nao.look_right()
            self.check_blobs()
        #self.__nao.walkNav(0, 0, (120 * almath.TO_RAD), 0.01)

    def check_blobs(self):
        biggest_target = None
        biggest_own = None
        recogtime_target = self.__start_time
        recogtime_own = self.__start_time
        headAngle = (self.__nao.get_angles("HeadYaw", True))
        headAngle = headAngle[0]        
        if (self.m.n_occurs("combined_" + self.own_goal) > 0):
            print "Blauw gezien"
            (recogtime, obs) = self.m.get_last_observation("combined_" + self.own_goal)
            contours = obs["sorted_contours"]
            print "Own goal found"
            biggest_own = contours[0]
            recogtime_own = recogtime
        if (self.m.n_occurs("combined_" + self.target_goal) > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_" + self.target_goal)
            contours = obs["sorted_contours"] 
            print "Target goal found" 
            biggest_target = contours[0]   
            recogtime_target = recogtime
        #if ( not biggest_target == None and (biggest_own == None or recogtime_own < (time.time() - 3)) ):                                    
        if not biggest_target == None and not biggest_own == None and recogtime_target > ( time.time() - 5 ):
            print "Two markers?"
            if biggest_target['surface'] > 50 and biggest_target['surface'] < 5000 and not biggest_target['height'] > 50:
                print "Big surface"
                print "Seen: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("yellow", biggest_target['x'], biggest_target['y'], biggest_target['width'], biggest_target['height'], biggest_target['surface'])                 
                print "Seen: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("blue", biggest_own['x'], biggest_own['y'], biggest_own['width'], biggest_own['height'], biggest_own['surface'])                 
                if biggest_own['surface'] > 500  and ( biggest_own['y'] < biggest_target['y'] ):
                    print "Own hoger dan Target"
                    self.__nao.look_forward()
                    self.__nao.walkNav(0.15,0.15,-((90 * almath.TO_RAD)))
                    self.__nao.wait_for(0.5)
                    self.__state = "F1"                    
                if biggest_own['surface'] > 500 and ( biggest_own['y'] > biggest_target['y'] ):
                    print "Target hoger dan Own"
                    self.__nao.look_forward()
                    self.__nao.walkNav(0.15,-(0.15),((90 * almath.TO_RAD)))
                    self.__nao.wait_for(0.5)
                    self.__state = "F1"
        if ( not biggest_target == None ):
            print "Something goal like seen"
            if ( recogtime_target > (time.time() - 5) ):
                print "Blob detected: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("yellow", biggest_target['x'], biggest_target['y'], biggest_target['width'], biggest_target['height'], biggest_target['surface']) 
                print "Blob detected: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("blue", biggest_own['x'], biggest_own['y'], biggest_own['width'], biggest_own['height'], biggest_own['surface'])                                    
                if biggest_target['surface'] >= 2000 and biggest_target['surface'] < 5000 and biggest_target['width'] > 40:
                    print "Big goal"
                    self.idling = True
                    # If the goal is seen while looking left
                    if self.__state == "F2":
                        self.__nao.walkNav(0,0,(45 * almath.TO_RAD), 0.01)
                        self.__nao.walkNav(-0.2, 0, 0, 0.01)
                        self.__nao.walkNav(0, -0.2, 0, 0.01)
                    # Elif the goal is seen while looking right
                    elif self.__state == "F3":
                        self.__nao.walkNav(0,0,-(45 * almath.TO_RAD), 0.01)
                        self.__nao.walkNav(-0.2, 0, 0, 0.01)
                        self.__nao.walkNav(0, 0.2, 0, 0.01)
                    self.__nao.look_forward_down()
                    self.__is_looking_horizontal = False
                    # Approachball (if -> while ?):
                    if (self.m.n_occurs("combined_red") > 0):
                        while self.approach_ball() == True:
                            print "Walking to ball"
                        if self.__approaching == 'ready':
                            return
                        elif self.__approaching == 'lost':
                            print "I've lost the ball.. :-("
                            self.__nao.stopwalk()
                            self.__nao.look_up()
                            self.__is_looking_horizontal = True
                            self.__state = "F1"
                            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ive lost the ball.'})
                            self.idling = True
                            return                    
        if not self.__nao.isMoving(): 
            if self.__state == "F1":
                self.__state = "F2"
            elif self.__state == "F2":
                self.__state = "F3"  
            elif self.__state == "F3":
                self.__state = "F1"
                
    def approach_ball(self):
        (recogtime, obs) = self.m.get_last_observation("combined_red")
        if not obs == None and recogtime > time.time()-5:
            self.__last_ball_recogtime = recogtime
            contours = obs["sorted_contours"]
            biggest_blob = contours[0]
            if biggest_blob['surface'] > 30 and biggest_blob['surface'] < 950:
                print "I have the ball in my sight!"
                blob_center_x = biggest_blob['x'] + biggest_blob['width']/2
                blob_center_y = biggest_blob['y'] + biggest_blob['height']/2
                if blob_center_y < 90:
                    if self.__is_looking_horizontal:
                        X = (((((blob_center_y -90)/90)**2)*0.25)+0.75)
                    else:
                        X = (((((blob_center_y -90)/90)**2)*0.75)+0.25)
                    Theta = math.copysign(((((blob_center_x -80)/80)**(2))/2), ((blob_center_x -80)*-1))
                    # Value found after enourmous amounts of experiments by trial and error
                    self.__nao.moveToward(X, 0, Theta)
                    print "blob_center_Y=%d    Walk_X=%f, blob_center_x=%d  Walk_Theta=%f" % (blob_center_y, X, blob_center_x, Theta) 
                    return True
                if blob_center_y > 90 and blob_center_x > 30 and blob_center_x < 130:
                    self.__nao.stopwalk()
                    print "I think I'm aligned with the ball and the goal now!"
                    self.m.add_item('goal_aligned',time.time(),{})
                    self.idling = True
                    self.__approaching = 'ready'
                    return False
        self.__approaching = 'lost'
        return False
