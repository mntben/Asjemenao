import basebehavior.behaviorimplementation

import time

class Soccer_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''The core soccer behavior for PAS.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        try:
            self.target_goal # This should be specified in the config, but this is to catch it.
        except:
            print "You should specify your target goal as an argument in the config!"
            self.target_goal = "yellow"

        # The four sub-behaviors defined here are the steps in our soccer behavior.

        #define list of sub-behavior here
        self.findball = self.ab.findball({})
        self.approachball = self.ab.approachball({})
        self.aligngoal = self.ab.aligngoal({'target_goal': self.target_goal})
        self.shoot = self.ab.shoot({'target_goal': self.target_goal})
        
        self.selected_behaviors = [ \
            ("findball", "True"), \
            ("approachball", "self.findball.is_finished()"), \
            ("aligngoal", "self.approachball.is_finished()"), \
            ("shoot", "self.aligngoal.is_finished()"), \
        ]
        
        self.restart_time = time.time()

        #Select Nao to use:
        self.nao = self.body.nao(0)
        self.nao.say("Lets play soccer!")
        #self.nao.useTopCamera()
        #self.nao.initCamera()
        self.nao.useBottomCamera()
        self.nao.initCamera()

    def implementation_update(self):

        if ((time.time()-self.restart_time)>20 and self.m.is_now('subsume_stopped', ['True'])):
            print "Lower level restarting."
            self.restart_time = time.time()
            self.findball = self.ab.findball({})
            self.approachball = self.ab.approachball({})
            self.aligngoal = self.ab.aligngoal({'target_goal': self.target_goal})
            self.shoot = self.ab.shoot({'target_goal': self.target_goal})
            return
