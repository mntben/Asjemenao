
import basebehavior.behaviorimplementation


class SoccerDefender_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        #Select Nao and make it stand up.
        self.__nao = self.body.nao(0)
        self.__nao.say("Lets defend the goal!")
        self.__nao.start_behavior("standup")

        self.__position = 0.25

    def implementation_update(self):
        #Make the Nao move to the right and left:
        if not self.__nao.isWalking():
            self.__nao.walkNav(0, self.__position, 0)
            self.__position *= -1
