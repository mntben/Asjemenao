import time
import random

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Intervalestimationtest_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #Set random time till completion
        self.completion_time = time.time() + random.randrange(5, 10, 1)
        print "Starting version 1."

    def implementation_update(self):

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        if (time.time()>self.completion_time):
            print "Version 1 completed."
            self.m.add_item('ie_test', time.time(), {'finished': True})
