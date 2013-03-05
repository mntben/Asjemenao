
import basebehavior.behaviorimplementation
import time
import random

class TestSubsumeLower_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''
    This is the lower-level behavior to test a subsumption-like behavior structure for PAS.
    '''

    def implementation_init(self):

        #define list of sub-behavior here
        self.start_time = time.time()
        self.idling = False

    def implementation_update(self):
        
        if self.idling:
            return
            
        # After a short wait...
        if time.time() - self.start_time > 2:
            if random.randint(0,1) is 0:
                print "Lower level succeeded."
                self.set_finished()
            else:
                print "Lower level stopped."
                self.m.add_item('subsume_stopped',time.time(),{'reason':'Bad luck.'})
                self.idling = True



