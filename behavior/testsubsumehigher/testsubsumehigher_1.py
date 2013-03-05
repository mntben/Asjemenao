
import basebehavior.behaviorimplementation
import time


class TestSubsumeHigher_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''
    This is the upper level behavior to test a subsumption-like system for PAS.
    
    WARNING! If lower-level behaviors are restarted by this behavior, any currently running will restart without storing info about this run in the BBIE!
    '''

    def implementation_init(self):

        #define list of sub-behavior here
        self.lower1 = self.ab.testsubsumelower({})
        self.lower2 = self.ab.testsubsumelower({})
        
        self.selected_behaviors = [ \
            ("lower1", "True"),
            ("lower2", "self.lower1.is_finished()"), \
        ]
        
        self.restart_time = time.time()

    def implementation_update(self):

        # Check for postcondition.
        if self.lower2.is_finished():
            print "Upper level succeeded."
            self.set_finished()
            return

        # Check to restart the system if a lower level has stopped.
        print self.m.is_now('subsume_stopped', ['True'])
        if ((time.time()-self.restart_time)>5 and self.m.is_now('subsume_stopped', ['True'])):
            print "Lower level restarting."
            self.restart_time = time.time()
            self.lower2 = self.ab.testsubsumelower({})
            self.lower1 = self.ab.testsubsumelower({})
            return
        
        # Prints for debug purposes.
        if self.lower1.is_finished():
            print "Now running lower2."
        else:
            print "Now running lower1."
