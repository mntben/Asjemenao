#TODO: create unit test

import socket
import time
import string
import math
import traceback

from navigation.obstacleavoidance.obstacleavoider import ObstacleAvoider
import logging
import util.nullhandler
import body.bodycontroller

ROS_ENABLED=False
try:
    import roslib; roslib.load_manifest('borg_pioneer')
    import rospy
    from std_msgs.msg import String
    from nav_msgs.msg import Odometry
    from geometry_msgs.msg import Pose, PoseStamped, Quaternion, Point, PoseWithCovarianceStamped
    import tf
    ROS_ENABLED = True
except:
    print "ROS IS NOT ENABLED"
    pass

logging.getLogger('Borg.Brain.BodyController.Pioneer').addHandler(util.nullhandler.NullHandler())

class PioneerConnector(util.threadedsocket.ThreadedSocket):
    def set_callback(self, cb):
        self.receive_callback = cb

    def handle_receive(self, data):
        if hasattr(self, "receive_callback") and self.receive_callback:
            self.receive_callback(data)

class Pioneer(object):
    """
    Controls a pioneer robot.
    (requires the motionController to run on the pioneer)
    """

    def __init__(self, ip_address, port, start_pose = False):
        self.logger = logging.getLogger('Borg.Brain.BodyController.Pioneer')
        self.__ip_address = ip_address
        self.__port = int(port)
        self.logger.info("Connecting to %s:%d" % (self.__ip_address, self.__port))
        self.__s = PioneerConnector(self.__ip_address, self.__port, giveup=-1, use_pickle=False, server=False)
        self.__s.set_verbose(False, True)
        self.__s.send("enslave\r\n")
        self.obstacleAvoider = ObstacleAvoider()
        self.emergency = False
        self.maxSpeed = 600
        self.doormaxSpeed = 500
        self.odo_offset = {"x": 0, "y": 0, "angle": 0}
        self.last_odometry = {"x": 0, "y": 0, "angle": 0, "time": time.time(), "frame_id": "odom_frame"}
        self.body = body.bodycontroller.BodyController()
        self.config = self.body.get_config()
        self.waypoint_skip_time = None
        self.detections = []

        # ROS node initialization
        self.ros_node_name = "borg_pioneer"
        self.ros_input_topic = "amcl_pose"
        self.ros_init_pose_topic = "initialpose"
        self.ros_output_topic = "odom"
        self.use_ros = ROS_ENABLED

        if self.use_ros:
            if not self.ros_init_topic():
                self.logger.error("ROS import succeeded, but setting up "    \
                                    "publisher failed. Is roscore running?")
                self.use_ros = False
            else:
                self.__s.set_callback(self.receive_callback)

            self.transformer = tf.TransformListener()

            if self.use_ros and not self.ros_init_subscription():
                self.logger.error("ROS publishing enabled, but ROS subscription failed.")
        else:
            self.logger.warning("Not publishing to ROS as ROS modules cannot "  \
                               "be imported")

        if start_pose and len(start_pose) == 3:
            self.set_odometry_offset(float(start_pose[0]), float(start_pose[1]), float(start_pose[2]))
            odo = {'x': self.odo_offset['x'],
                   'y': self.odo_offset['y'],
                   'angle': self.odo_offset['angle']}
            self.ros_publish_initial_pose(odo)

    def __del__(self):
        self.__s.close()
        self.__s.join()

    def stop(self):
        print "Stopping Pioneer connector"
        self.__s.close()
        self.__s.join()

        if self.use_ros:
            self.ros_publisher.unregister()
            self.use_ros = False
            self.logger.info("Unregistering ROS node %s" % self.ros_node_name)
        else:
            self.logger.info("ROS publishing disabled, so not unregistering")

    def ros_init_topic(self):
        try:
            self.ros_publisher = rospy.Publisher(self.ros_output_topic, Odometry)
            self.ros_init_publisher = rospy.Publisher(self.ros_init_pose_topic, PoseWithCovarianceStamped)
            rospy.init_node(self.ros_node_name)
            self.logger.info("Starting publishing to ROS on ROS-topic %s as " \
                             "node %s" % (self.ros_output_topic, self.ros_node_name))
            return True
        except:
            traceback.print_exc()
            return False

    def ros_init_subscription(self):
        try:
            self.ros_subscription = rospy.Subscriber(self.ros_input_topic, 
                                                     PoseWithCovarianceStamped,
                                                     self.ros_subscription_cb)
            return True
        except:
            traceback.print_exc()
            self.ros_subscription = None
            return False

    def ros_publish(self, odometry):
        if self.use_ros:
            if rospy.is_shutdown():
                self.logger.warning("ROSPY is shutting down. Disabling ROS publishing")
                self.ros_publisher.unregister()
                self.use_ros = False
                return odometry

            try:
                odo = Odometry()
                theta = odometry['angle'] * (math.pi / 180.0)
                quat = tf.transformations.quaternion_from_euler(0, 0,theta)
                odo.pose.pose = Pose(Point(odometry['x']/1000., odometry['y']/1000., 0.), Quaternion(*quat))
                time = odometry['time']
                secs = int(time)
                nsecs = int((time - secs) * 1000000000)
                odo.header.stamp = rospy.Time(secs, nsecs)
                odo.header.frame_id = "odometry_frame"
                
                self.ros_publisher.publish(odo)
            except rospy.ROSInterruptException:
                self.logger.warning("ROSPY generated exception. Disabling ROS publishing")
                self.ros_publisher.unregister()
                self.use_ros = False
                return odometry

            try:
                # Transform the odometry using the AMCL tf message
                pose = PoseStamped()
                pose.header.stamp = rospy.Time(secs, nsecs)
                pose.header.frame_id = "base_link"
                pose.pose = Pose(Point(0, 0, 0), Quaternion())

                translation, rotation = self.transformer.lookupTransform("map", "base_link", rospy.Time(0))

                orientation = tf.transformations.euler_from_quaternion(rotation)
                new_theta = orientation[2] / (math.pi / 180.0)
                new_odo = {"x": translation[0] * 1000.0,
                           "y": translation[1] * 1000.0, 
                           "angle": new_theta}

                # Return the transformed odometry
                return new_odo
            except Exception as e:
                self.logger.error("Exception (%s) in transform. Probably AMCL is not working (yet)" % repr(e))
                return odometry

    def ros_publish_initial_pose(self, odometry):
        init_pose = PoseWithCovarianceStamped()
        theta = odometry['angle'] * (math.pi / 180.0)
        quat = tf.transformations.quaternion_from_euler(0, 0, theta)
        init_pose.pose.pose = Pose(Point(odometry['x']/1000., odometry['y']/1000., 0.), Quaternion(*quat))
        init_pose.pose.covariance = [0.01] * 36
        init_pose.header.stamp = rospy.Time.now()

        self.ros_init_publisher.publish(init_pose)

    def ros_subscription_cb(self, data):
        """
        This method is called by ROS when new data has been received on the AMCL
        corrected pose topic
        """
        new_x = data.pose.pose.position.x * 1000.0
        new_y = data.pose.pose.position.y * 1000.0
       
        quat = data.pose.pose.orientation
        quaternion = [quat.x, quat.y, quat.z, quat.w]
        orientation = tf.transformations.euler_from_quaternion(quaternion)
        new_theta = orientation[2]
        new_time = data.header.stamp.secs + (data.header.stamp.nsecs / 1000000000)

        cur_x = self.last_odometry['x']
        cur_y = self.last_odometry['y']
        cur_theta = self.last_odometry['angle']

        #self.odo_offset['x'] += (new_x - cur_x)
        #self.odo_offset['y'] += (new_y - cur_y)
        #self.odo_offset['angle'] += (new_theta - cur_theta)
        pose = {'x': new_x, 'y': new_y, 'angle': new_theta}
        pose['battery_level'] = self.last_odometry['battery_level']
        pose['time'] = new_time
        print repr(pose)
        command = {'name':'odometry', 'time': new_time, 'property_dict': pose}          
        self.logger.info("Received odometry offset from ROS: %s" % repr(self.odo_offset))
        self.detections.append(command)

    def set_odometry_offset(self, x, y, angle):
        self.odo_offset['x'] = x
        self.odo_offset['y'] = y
        self.odo_offset['angle'] = angle
        self.logger.info("Set odometry offset to %s" % repr(self.odo_offset))

    def get_odometry_offset(self):
        return self.odo_offset

    def get_ip_address(self):
        """
        Returns the IP address as specified in the constructor.
        """
        return self.__ip_address

    def get_port(self):
        """
        Returns the port as specified in the constructor.
        """
        return self.__port

    def head_direction(self, target, useAvoidance=False, verbose=False, turnSpeed=1, door = False):
        """
        Set the target where the pioneer should go to.
        format = (speed, angle)
            speed in range 0 to 1
            positive values are to the right
            angle in range -180 to 180, where +-180 is backwards and 0 is forward
        This is the function behaviors should call when they want the robot
        to go to some direction.
        """

        if useAvoidance:
            endVector = self.obstacleAvoider.avoid(target) # endVector (length, direction)
        else:
            endVector = target

        speedLeft, speedRight = self.target_to_left_right_speeds(endVector, turnSpeed=turnSpeed, door=door)

        self.logger.debug("endVector: %s" % repr(endVector))
        self.logger.debug("Wheel speeds: %d, %d" % (speedLeft, speedRight))

        if self.config.get_option("body", "pioneer_simulation") == "True":
            l = speedLeft
            speedLeft = speedRight
            speedRight = l
        self.__s.sendall("leftright " + str(int(speedLeft)) + " " +str(int(speedRight)) + "\n")

        return endVector
    def table_move(self, target, useAvoidance=False, verbose=False, turnSpeed=1, move=False):
        """
        Set the target where the pioneer should go to.
        format = (speed, angle)
            speed in range 0 to 1
            positive values are to the right
            angle in range -180 to 180, where +-180 is backwards and 0 is forward
        This is the function behaviors should call when they want the robot
        to go to some direction.
        """
        endVector2 = None
        door = False
        if useAvoidance:
            endVector = self.obstacleAvoider.avoid(target) # endVector (length, direction)
        else:
            endVector = target
            endVector2 = self.obstacleAvoider.avoid(target)
        
        if not move:
            if endVector2:
                return endVector2
            return endVector
        speedLeft, speedRight = self.target_to_left_right_speeds(endVector, turnSpeed=turnSpeed, door=door)

        self.logger.debug("endVector: %s" % repr(endVector))
        self.logger.debug("Wheel speeds: %d, %d" % (speedLeft, speedRight))

        if self.config.get_option("body", "pioneer_simulation") == "True":
            l = speedLeft
            speedLeft = speedRight
            speedRight = l
        self.__s.sendall("leftright " + str(int(speedLeft)) + " " +str(int(speedRight)) + "\n")

        return endVector
    
    def follow_direction(self, target, useAvoidance=False, verbose=False, turnSpeed=1, door = False, move=True,force=False):
        """
        Set the target where the pioneer should go to.
        format = (speed, angle)
            speed in range 0 to 1
            positive values are to the right
            angle in range -180 to 180, where +-180 is backwards and 0 is forward
        This is the function behaviors should call when they want the robot
        to go to some direction.
        """

        if useAvoidance:
            endVector = self.obstacleAvoider.avoid(target) # endVector (length, direction)
        else:
            endVector = target
        if move:   
            if abs(endVector[1]) < 100 or force:
                if abs(endVector[1]) > 20:
                    speedLeft, speedRight = self.target_to_left_right_speeds((0.3, endVector[1]), turnSpeed=turnSpeed, door=door)
                else:
                    speedLeft, speedRight = self.target_to_left_right_speeds(endVector, turnSpeed=turnSpeed, door=door)
    
                self.logger.debug("endVector: %s" % repr(endVector))
                self.logger.debug("Wheel speeds: %d, %d" % (speedLeft, speedRight))
        
                if self.config.get_option("body", "pioneer_simulation") == "True":
                    l = speedLeft
                    speedLeft = speedRight
                    speedRight = l
                self.__s.sendall("leftright " + str(int(speedLeft)) + " " +str(int(speedRight)) + "\n")
        
                return endVector
            else:
                return (-1,-1)
        
        return 0
    
    def RL_Navigation(self, action, turnSpeed=1, door = False, Go = False, speed = 0.7, turndegree = 90):
        endVector = self.obstacleAvoider.avoid((speed, 0))
        if Go:
            if action == "left" or action == "mleft":
                self.turn(turndegree)
                return (0,(0,0))
            if action == "right" or action == "mright":
                self.turn(-turndegree)
                return (0,(0,0))
            if action == "move" or action == "mmove":
                speedLeft, speedRight = self.target_to_left_right_speeds(endVector, turnSpeed=turnSpeed, door=door)
                if abs(endVector[1]) < 25:
                    self.logger.debug("endVector: %s" % repr(endVector))
                    self.logger.debug("Wheel speeds: %d, %d" % (speedLeft, speedRight))
    
                    if self.config.get_option("body", "pioneer_simulation") == "True":
                        l = speedLeft
                        speedLeft = speedRight
                        speedRight = l
                    self.__s.sendall("leftright " + str(int(speedLeft)) + " " +str(int(speedRight)) + "\n")
                    return (0,endVector)
                else:
                    return (1,endVector)

    def set_target(self, target, useAvoidance=False, verbose=False):
        """
        deprecated function.
        use head_direction instead
        """
        self.logger.info("Deprecated function set_target called. Please call head_direction.")
        self.head_direction(self, target, useAvoidance, verbose)

    def target_to_left_right_speeds(self, target, turnSpeed=1, door = False):
        """
        Convert an target vector to left and right wheel speeds.
        This function should be optimized
        """

        angle = target[1] # direction in range of -90 to 90
        speed = target[0] # speed in range [0, 1]
        if door == True:
            maxSpeed = self.doormaxSpeed * speed
        else:
            maxSpeed = self.maxSpeed * speed
        
        left = 100 # percent
        right = 100 # percent

        # determines how much the the turnspeed should be inhibited
        turnInhibitor = 1-turnSpeed

        # inhibit correct wheel according to the angle of the target
        if angle < 0: #turn left
            left += angle
            right += angle*turnInhibitor
        else: #turn right
            right -= angle
            left -= angle*turnInhibitor

        # avoid to fast spinning when target is behind robot
        if abs(angle) > 90:
            maxSpeed /= 2

        # scale leftright speeds to maxspeed
        left = maxSpeed * (left/100.0)
        right = maxSpeed * (right/100.0)

        return (left, right)

    def rotate_to_direction(self, angle, fixed_speed=False):
        #normalize speed
        print "Angle IS: ", angle
        speed = (self.maxSpeed / 2) * (abs(angle)/180.0)
        if fixed_speed:
            speed = 100

        if angle < 0:
            #turn left
            self.set_left_right_speeds(-speed, speed)
        else :
            # turn right
            self.set_left_right_speeds(speed, -speed)

    def set_left_right_speeds(self, speedLeft, speedRight):
        """
        Send command to set left and right wheel speed
        This is the function behaviors used to call to move the robot.
        Do NOT use it anymore.
        Behaviors should call set_target(target)
        """
        self.logger.debug("Speed as received %d, %d" % (speedLeft, speedRight))
        self.__s.send("leftright " + str(int(speedLeft)) + " " +str(int(speedRight)) + "\n") 

###
    def forward(self, distance):
        """
        Forward in mm. Take care, this will continue until receives a new command or is finished
        DOES NOT USE OBSTACLE AVOIDANCE!
        """
        self.__s.send("forward "+str(distance)+"\n")

    def turn(self, angle):
        """
        Turn in degrees. Take care, this will continue until receives a new command or is finished
        left is positive
        DOES NOT USE OBSTACLE AVOIDANCE!
        """
        self.__s.sendall("turn "+str(angle)+"\n")
    
    def set_options(self, option1, option2):
        """
        Usage:
        Option1: 0- Rotational Velocity 1- Rotational Acceleration 2- Rotational Deceleration 3- Translational Accelration
        4- Translational Deceleration
        
        Option2: 0- Degree Per second 1- & 2- Degree Per Second^2
        """  
        self.__s.send("options " + str(int(option1)) + " " +str(int(option2)) + "\n") 

    def stop_robot(self):
        ''' Send command to stop the robot'''
        self.__s.send("stop\n")
        
    # The Functions to read odometry from the pioneer 
    def update(self):
        try:
            msg = self.__s.get_data()

            for entry in msg:
                lines = entry.split("\n")
                for line in lines:
                    self.processMessage(line)
            if self.emergency:
                self.detections.append("EMERGENCY")
        except Exception as e:
            #TODO:XXX: check if the exception is indeed raised just because
            #there is no data available
            self.logger.warn("Exception in reading data: %s" % repr(e))
        detections = self.detections
        self.detections = []
        return detections  

    def receive_callback(self, data):
        for msg in data:
            lines = msg.split("\n")
            for line in lines:
                self.processMessage(line)

    def processMessage(self, msg):
        """
        Process a message received from the pioneer controller.
        This can either be a notification that the emergency
        button has been pressed (or the pioneer is not available)
        or the odometry data.
        """
        
        if not msg:
            return
       
        #self.logger.debug("This is the received string: %s" % msg) 
        value_list = msg.split()
        if "EMERGENCY" in value_list:
            if not self.emergency:
                self.logger.info("Storing last odometry %s as odometry offset" % repr(self.last_odometry))
                self.odo_offset['x'] = self.last_odometry['x']
                self.odo_offset['y'] = self.last_odometry['angle']
                self.odo_offset['angle'] = self.last_odometry['angle']

            
            self.emergency = True
            return

        # Assume odometry data
        # Remove multiple occurrences of the space characters:
        correct_value_list = filter(None, value_list)
        
        dict = {}
        
        
        #Checking Pioneer returned value numbers
        if len(correct_value_list) == 4:
            self.logger.debug("The time is not from Pioneer")
            dict["time"] = time.time()
        elif len(correct_value_list) == 5:
            self.logger.debug("The time is from Pioneer")
            dict["time"] = float(value_list[4])
        else:
            self.logger.warn("Pionner returning less than 4 values")
            return
        x = float(value_list[0])
        y = float(value_list[1])
        angle_rad = math.radians(self.odo_offset['angle'])
        
        
        # Apply rotation by offset angle
        dict["x"] = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        dict["y"] = x * math.sin(angle_rad) + y * math.cos(angle_rad)

        # Translate point
        dict["x"] += self.odo_offset["x"]
        dict["y"] += self.odo_offset["y"]
        
        # Update angle
        dict["angle"] = float(value_list[2]) + self.odo_offset['angle']

        # Add battery level
        dict["battery_level"] = float(value_list[3])
        #dict["time"] = float(value_list[4])
        #dict["time"] = time.time()
        
        dict["frame_id"] = self.last_odometry['frame_id']

        self.last_odometry = dict
        
        command = {'name':'odometry', 'time':time.time(), 'property_dict':dict}          
        if self.emergency:
            self.__s.send("enslave\r\n")

        self.emergency = False
        if self.use_ros:
            transformed = self.ros_publish(self.last_odometry)
            command['property_dict'] = transformed

        self.detections.append(command)
