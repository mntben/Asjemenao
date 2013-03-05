import basebehavior.behaviorimplementation

import time
import almath

class ApproachBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.idling = False

        self.__nao = self.body.nao(0)
        self.__nao.say("Ay")

        self.__last_ball_recogtime = 0
        self.__ball_last_seen = time.time()

        self.__is_looking_horizontal = True


    def implementation_update(self):
        if self.idling:
            return

        # If the ball is seen but not close enough, just walk towards it:
        if (self.m.n_occurs("red.colorblob") > 0):
            (recogtime, obs) = self.m.get_last_observation("red.colorblob")
            if not obs == None and recogtime > self.__last_ball_recogtime:
                #print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['size'])
                self.__last_ball_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if obs['size'] > 0.0015:
                    self.__ball_last_seen = time.time()
                    #Is the ball in the correct location?:
                    if obs['y'] > 75 and obs['x'] > 60 and obs['x'] < 100 and not self.__is_looking_horizontal:
                        # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                        self.m.add_item('ball_approached', time.time(),{}) 
                        return
                    #~ if not self.__nao.isWalking():
                        #~ #Make sure that the ball is in the center of the camera:
                        #~ if obs['x'] < 60:
                            #~ self.__nao.walkNav(0, 0, 0.1)
                            #~ pass
                        #~ elif obs['x'] > 100:
                            #~ self.__nao.walkNav(0, 0, -0.1)
                            #~ pass
                    if not self.__nao.isWalking():
                        #Walk a bit if the ball is not really close:
                        if obs['y'] < 80 and self.__is_looking_horizontal:
                            print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['size'])
                            self.__nao.walkNav(((obs['y']-80)*(-0.005)), 0, ((obs['x']-80)*(-0.003)))
                            pass
                        elif obs['y'] < 80 and not self.__is_looking_horizontal:
                            self.__nao.walkNav(((obs['y']-85)*(-0.002)), 0, ((obs['x']-80)*(-0.005)))
                            pass
                        elif self.__is_looking_horizontal:
                            self.__nao.look_down()
                            self.__is_looking_horizontal = False
        
        # Timeout after 10 seconds if the ball is not seen anymore:
        if (time.time() - self.__ball_last_seen) > 10:
            self.__nao.say("I can not see the ball anymore!")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True
