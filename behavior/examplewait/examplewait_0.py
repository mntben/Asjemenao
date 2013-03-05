'''
This is just a simple example behavior that wait for a specific amount of observation in memory over time.
'''

import basebehavior.behaviorimplementation
import time

class ExampleWait_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.__last_recogtime = time.time()
        self.__recog_count = 0
        #Check if the proper configuration parameters are set:
        try:
            print "Example Wait Behavior Started; Params used: label = %s, required_recog_count = %d" \
                    % (self.label, self.required_recog_count)
        except:
            raise Exception("Either label or required_recog_count parameter not set!") 

    def implementation_update(self):
        #Simple look for the "example" observation and print the result if there is a new update:
        if (self.m.n_occurs("example") > 0):
            (recogtime, prop_dict) = self.m.get_last_observation("example")
            if recogtime > self.__last_recogtime:
                print "%s; new observation (%d) with values %f, %f received!" \
                        % (self.label, self.__recog_count, prop_dict["value_1"], prop_dict["value_2"])
                self.__last_recogtime = time.time()
                self.__recog_count += 1
                #Or received a couple of observation, so behavior is finished:
                if self.__recog_count == int(self.required_recog_count):
                    self.set_finished()

