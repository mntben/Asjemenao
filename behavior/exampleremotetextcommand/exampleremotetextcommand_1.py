
import basebehavior.behaviorimplementation
import time

class ExampleRemoteTextcommand_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        print "Example Remote Text Command Behavior Started!"
        self.__last_recogtime = time.time()

    def implementation_update(self):
        if (self.m.n_occurs("text_command") > 0):
            (recogtime, prop_dict) = self.m.get_last_observation("text_command")
            if recogtime > self.__last_recogtime:
                print "Ok, so the command you typed is: %s" % prop_dict["text_command"]
                self.__last_recogtime = time.time()

