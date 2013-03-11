import basebehavior.behaviorimplementation

import time

class Basicloc_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.__nao = self.body.nao(0)
        
        self.m.add_item('loc',time.time(),{'x': 0, 'y': 0})
        
        self.__nao.walkNav(0.2, 0, 0)
        
        self.m.add_item('loc',time.time(),{'x': 0, 'y': 0})
        
 
                 
    def implementation_update(self):
        (recogtime, loc) = self.m.get_last_observation("loc")
        
        print "X-location: x=%d y=%d" \
            % (loc['x'], loc['y']) 
