
import basebehavior.behaviorimplementation
import time

class ExampleSpeech_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        print "Speech Example Behavior Started!"
        self.__speech_start_time = 0

    def implementation_update(self):
        #Check to see if the following strings are understood since self.__speech_start_time
        if self.m.has_understood(self.__speech_start_time, ['please give me the beer', 'give the beer', 'please give the beer']):
            print "Yeah sure, I'll give you a beer, what flavor do you like?"
        if self.m.has_understood(self.__speech_start_time, ['please give me the coffee', 'give the coffee', 'please give the coffee']):
            print "Sorry, we ran out of coffee pads, do you like to have a beer maybe?"

        #An alternative way is to do the following:
        """
        if (self.m.n_occurs("voice_command") > 0):
            (recogtime, prop_dict) = self.m.get_last_observation("voice_command")
            print "Ok, received: " + prop_dict['message']
        """

        #Remember the previous time we checked for speech, this will ensure that we ignore everything in the past:
        self.__speech_start_time = time.time()
