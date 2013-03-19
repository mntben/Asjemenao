
import basebehavior.behaviorimplementation
import time


class SoccerDefender_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #define list of sub-behavior here
        self.findballdefender = self.ab.findballdefender({})
        self.sitball = self.ab.sitball({})
        
        self.selected_behaviors = [ \
            ("findballdefender", "True"), \
            ("sitball", "self.findballdefender.is_finished()"), \
        ]
        
        #Select Nao to use:
        self.nao = self.body.nao(0)
        self.nao.say("Lets defend the goal!")
        self.nao.useBottomCamera()
        self.nao.initCamera()
        
        print "test"
        
        
        self.nao.start_behavior("standup")        
        
        self.restart_time = time.time()

    def implementation_update(self):

        # Check to restart the system if a lower level has stopped.
        # This is a kinda tricky piece of code. Our architecture isn't optimal for implementing a subsumption-like structure.
        # That's why this kinda inefficient structure is here. Ask Marko Doornbos if you have questions about this part.
        if ((time.time()-self.restart_time)>5 and self.m.is_now('subsume_stopped', ['True'])):
            print "Lower level restarting."
            self.restart_time = time.time()
            self.findballdefender = self.ab.findballdefender({})
            self.sitball = self.ab.sitball({})
            return
