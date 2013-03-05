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
        self.__nao.say("Align!")
        
        self.__nao.look_forward()
        #self.__nao.walkNav(0.15, 0.12, -(90 * almath.TO_RAD))

    def implementation_update(self):
        if self.idling:
            return
        
        #TODO: Remove the following with the steps mentioned below (e.d. align the robot so that it can kick the ball in the direction of the goal):
        #It now simply assumes that it is already aligned:
        if not self.__nao.isWalking(): 
            if (time.time() - self.__start_time) > 10:
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

