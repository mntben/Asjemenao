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
        self.nao.useTopCamera()
        self.nao.initCamera()
        self.nao.useBottomCamera()
        self.nao.initCamera()

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if self.shoot.is_finished():
            print "Goal scored. Reset robots to starting positions and restart."
            self.set_finished()
            return

        # Check to restart the system if a lower level has stopped.
        # This is a kinda tricky piece of code. Our architecture isn't optimal for implementing a subsumption-like structure.
        # That's why this kinda inefficient structure is here. Ask Marko Doornbos if you have questions about this part.
        if ((time.time()-self.restart_time)>5 and self.m.is_now('subsume_stopped', ['True'])):
            print "Lower level restarting."
            self.restart_time = time.time()
            self.findball = self.ab.findball({})
            self.approachball = self.ab.approachball({})
            self.aligngoal = self.ab.aligngoal({'target_goal': self.target_goal})
            self.shoot = self.ab.shoot({'target_goal': self.target_goal})
            return
