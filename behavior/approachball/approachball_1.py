from __future__ import division
import basebehavior.behaviorimplementation

import time
import almath
import math


class ApproachBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.idling = False
        self.__ball_threshold_y = 100

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
                self.__last_ball_recogtime = recogtime
                contours = obs["sorted_contours"]
                biggest_blob = contours[0]
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if biggest_blob['surface'] > 30 and biggest_blob['surface'] < 950:
                    #print "Approaching: %s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                    #    % ("red", biggest_blob['x'], biggest_blob['y'], biggest_blob['width'], biggest_blob['height'], biggest_blob['surface'])
                    self.__ball_last_seen = time.time()
                    blob_center_x = biggest_blob['x'] + biggest_blob['width']/2
                    blob_center_y = biggest_blob['y'] + biggest_blob['height']/2
                    #Is the ball in the correct location?:
                    if blob_center_y > self.__ball_threshold_y and blob_center_x > 30 and blob_center_x < 130 and not self.__is_looking_horizontal:
                        # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                        self.__nao.stopwalk()
                        self.m.add_item('ball_approached', time.time(),{}) 
                        print "Now aligning"
                        return                 
                    if blob_center_y > self.__ball_threshold_y and ( blob_center_x >= 130 or blob_center_x < 30 ) and not self.__is_looking_horizontal:
                        self.__nao.walkNav(-0.1, 0, 0, 0.01)                      
                    if blob_center_y < self.__ball_threshold_y:
                        if self.__is_looking_horizontal:
                            X = (((((blob_center_y -self.__ball_threshold_y)/self.__ball_threshold_y)**2)*0.25)+0.75)
                        else:
                            X = (((((blob_center_y -self.__ball_threshold_y)/self.__ball_threshold_y)**2)*0.75)+0.25)
                        
                        Theta = math.copysign(((((blob_center_x -80)/80)**(2))/2), ((blob_center_x -80)*-1))
                        #Value found after enourmous amounts of experiments by trial and error
                        self.__nao.moveToward(X, 0, Theta)
                        print "blob_center_Y=%d    Walk_X=%f,  blob_center_x=%d  Walk_Theta=%f" % (blob_center_y, X, blob_center_x, Theta)
                        pass
                    elif self.__is_looking_horizontal:
                        print "Now looking down"
                        self.__nao.look_down()
                        self.__is_looking_horizontal = False
        
        # Timeout after 5 seconds if the ball is not seen anymore:
        if (time.time() - self.__ball_last_seen) > 5:
            print "Stopped walking"
            self.__nao.stopwalk()
            self.__nao.say("Can't see ball! one")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True
        
        
