import basebehavior.behaviorimplementation

import time
import almath

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__start_time = time.time()   
        self.idling = False            
        self.__nao.say("Align!")
        print "Target goal: "  + self.target_goal
        print "Own goal: "  + self.own_goal

    def implementation_update(self):   
        if self.idling:
            return    
     
        (recogtime, obs) = self.m.get_last_observation("combined_yellow")
        contours = obs["sorted_contours"]
        biggest_blob = contours[0]
        print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
            % ("yellow", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
        (recogtime, obs) = self.m.get_last_observation("combined_blue")
        contours = obs["sorted_contours"]
        biggest_blob = contours[0]
        print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
            % ("blue", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
        
        
        if not self.__nao.isMoving(): 
            if (time.time() - self.__start_time) > 20:
                print "Just kicking"
                self.idling = True
                self.m.add_item('goal_aligned',time.time(),{})
                
        
        self.__nao.look_up()
        self.check_blobs()
        #self.__nao.look_left()
        #self.check_blobs()
        #self.__nao.look_right()
        #self.check_blobs()
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
        if ( not biggest_target == None ):
            print "Something yellow"
            if ( recogtime_target > (time.time() - 5) ):
                print "Just now"
                print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("yellow", biggest_target['x'], biggest_target['y'], biggest_target['width'], biggest_target['height'], biggest_target['surface']) 
                print "Seen: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("blue", biggest_own['x'], biggest_own['y'], biggest_own['width'], biggest_own['height'], biggest_own['surface'])                                    
                if biggest_target['surface'] >= 2000:
                    print "Big goal"
                    self.idling = True
                    #self.__nao.walkNav(0,0,headAngle)
                    self.m.add_item('goal_aligned',time.time(),{})
                    return              
        elif not biggest_target == None and not biggest_own == None and recogtime_target > ( time.time() - 5 ):
            print "Two markers"
            if biggest_target['surface'] > 50 and biggest_target['surface'] < 2000:
                print "Big surface"
                print "Seen: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("yellow", biggest_target['x'], biggest_target['y'], biggest_target['width'], biggest_target['height'], biggest_target['surface'])                 
                print "Seen: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    % ("blue", biggest_own['x'], biggest_own['y'], biggest_own['width'], biggest_own['height'], biggest_own['surface'])                 
                if biggest_own['surface'] > 500  and ( biggest_own['y'] < biggest_target['y'] ):
                    print "Own hoger dan Target"
                    self.__nao.walkNav(0.15,0.15,-((90 * almath.TO_RAD) + headAngle))
                if biggest_own['surface'] > 50 and ( biggest_own['y'] > biggest_target['y'] ):
                    print "Target hoger dan Own"
                    self.__nao.walkNav(0.15,-(0.51),((90 * almath.TO_RAD) + headAngle))
