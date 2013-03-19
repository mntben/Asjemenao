import basebehavior.behaviorimplementation

import time
import almath

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal in in a line.'''

    #this implementation should not define an __init__ !!!

    def implementation_init(self):
        pass


    def implementation_update(self):
        (recogtime, obs) = self.m.get_last_observation("combined_yellow")
        contours = obs["sorted_contours"]
        biggest_blob = contours[0]
        print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
            % ("yellow", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
        
        if not self.__nao.isMoving(): 
            if (time.time() - self.__start_time) > 10:
                print "Just kicking"
                self.idling = True
                self.m.add_item('goal_aligned',time.time(),{})
                
        
        self.__nao.lookup()
        check_blobs()
        self.__nao.look_left()
        check_blobs()
        self.__nao.look_right()
        check_blobs()
        self.__nao.walkNav(0, 0, (120 * almath.TO_RAD), 0.01)

    def check_blobs(self):
        
        self.target_goal
        self.own_goal
        
