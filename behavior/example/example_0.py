'''
This is just a simple example behavior.
'''

import basebehavior.behaviorimplementation
import time

class Example_x(basebehavior.behaviorimplementation.BehaviorImplementation):
    '''
    This is just a simple example behavior.
    '''

    def implementation_init(self):
        print "Example Behavior Started!"
#self.body.nao(0).say("Hello, lets get started!")
#        self.body.nao(0).start_behavior("wipe_forehead")

        #Subbehaviors:
        self.examplewait1 = self.ab.exampleWait({'required_recog_count':2, 'label':'First Behavior'})
        self.examplewait2 = self.ab.exampleWait({'required_recog_count':4, 'label':"Second Behavior"})
        self.examplewait3 = self.ab.exampleWait({'required_recog_count':6, 'label':"Third Behavior"})

        #Preconditions for each subbehavior:
        self.selected_behaviors = [ \
            ("examplewait1", "True"),
            ("examplewait2", "self.examplewait1.is_finished()"), \
            ("examplewait3", "self.examplewait2.is_finished()"), \
        ]


    def implementation_update(self):
        if self.examplewait1.is_finished() and self.examplewait2.is_finished() and self.examplewait3.is_finished():
            print "All behaviors finished, lets restart the first subbehavior..."     
            self.examplewait1 = self.ab.exampleWait({'required_recog_count':2, 'label':'First Behavior'})
