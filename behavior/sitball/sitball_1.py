import basebehavior.behaviorimplementation

import time

class Sitball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

	'''This behavior will try to kick a ball at the Nao's feet into the goal.'''

	#this implementation should not define an __init__ !!!


	def implementation_init(self):
		self.idling = False
		self.__start_time = time.time()
		self.__nao = self.body.nao(0)
		self.__nao.start_behavior("Asje_sitdown")   
		self.__nao.look_down()

	def implementation_update(self):
		if self.idling:
			return

		(recogtime, obs) = self.m.get_last_observation("combined_red")
		contours = obs["sorted_contours"]
		biggest_blob = contours[0]


		if ((time.time() - self.__start_time) > 5) and ( ( not self.m.n_occurs("combined_red") > 0 ) or biggest_blob['surface'] < 100 ):
			print "Can't see the bal anymore 1"
			self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I am on the ground.'})
			self.idling = True
		elif (self.m.n_occurs("combined_red") > 0):
			if biggest_blob['surface'] > 300:
				self.__last_recogtime = recogtime
				print "Still see the ball: red: x=%d, size=%f" % (biggest_blob['x'], biggest_blob['surface']) 
			else:
				print "Can't see the bal anymore 2"
				self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I am on the ground.'})
				self.idling = True
		else:
			print "Can't see the bal anymore 3"
			self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I am on the ground.'})
			self.idling = True
		if ((time.time() - self.__start_time) > 10):
			print "I've been sitting too long!"
			self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I am on the ground.'})
			self.idling = True
