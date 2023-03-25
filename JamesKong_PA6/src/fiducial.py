#!/usr/bin/env python

'''
James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA6 - Fiducial Follower
'''

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from fiducial_msgs.msg import FiducialTransformArray

import math

class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.fiducial_sub = rospy.Subscriber('/fiducial_transforms', FiducialTransformArray, self.fiducial_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.twist = Twist()
        self.first_fiducial = 106
        self.second_fiducial = 101
        self.distance = 0
        self.angle = 0

    def fiducial_callback(self, data):
        #print(data.transforms)
        #if fiducial is detected
        if data.transforms != []:
            fiducial = data.transforms[0]
            # print(list(fiducial.transform.translation))
            translation = fiducial.transform.translation
            #x not an attribute, i dont understand since im able to print it successfully, why can i not compare it to numbers
            print()
            print(translation)
            print(self.distance)
            if translation.z != 0 and translation.z != None:
                self.distance = translation.z

            if translation.x != 0 and translation.x != None:
                self.angle = translation.x

            #keep moving until close enough distance
            if self.distance > 0.50:
                if self.angle < 0: 
                    self.twist.angular.z = 0.2
                elif self.angle > 0:
                    self.twist.angular.z = -0.2

                self.twist.linear.x = 0.2
            self.cmd_vel_pub.publish(self.twist)

        else:
            if self.distance <= 0.50 or self.distance == 0:
                self.twist.linear.x = 0
                self.twist.angular.z = -0.4
    
            self.cmd_vel_pub.publish(self.twist)
            
                


#make x 0, make z decrease, 
  

rospy.init_node('follower')
follower = Follower()
rospy.spin()
