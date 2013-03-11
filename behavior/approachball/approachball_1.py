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
        self.__nao.look_horizontal()
        self.__is_looking_horizontal = True

    def implementation_update(self):
        if self.idling:
            return

        # If the ball is seen but not close enough, just walk towards it:
        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.__last_ball_recogtime:
                #print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['size'])
                self.__last_ball_recogtime = recogtime
                contours = obs["sorted_contours"]
                biggest_blob = contours[0]
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if biggest_blob['surface'] > 100 and biggest_blob['surface'] < 950:
                    print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                        % ("red", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
                    self.__ball_last_seen = time.time()
                    #Is the ball in the correct location?:
                    if biggest_blob['y'] > 75 and biggest_blob['x'] > 20 and biggest_blob['x'] < 120 and not self.__is_looking_horizontal:
                        # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                        self.__nao.stopwalk()
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
                    #Walk a bit if the ball is not really close:
                    if biggest_blob['y'] < 80 and self.__is_looking_horizontal:
                        #print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['size'])
                        Y = ((biggest_blob['y']-80)*(-0.00625)+0.5)
                        Theta = ((biggest_blob['x']-80)*(-0.004))
                        self.__nao.moveToward(Y, 0, Theta)
                        pass
                    elif self.__is_looking_horizontal:
                        self.__nao.look_down()
                        self.__is_looking_horizontal = False
        
        # Timeout after 5 seconds if the ball is not seen anymore:
        if (time.time() - self.__ball_last_seen) > 5:
            self.__nao.say("Can't see ball!")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True
        elif (time.time() - self.__ball_last_seen) > 2:
            self.__nao.stopwalk()
