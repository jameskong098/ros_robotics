#!/usr/bin/env python

#This processes all of the scan values


import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16, Float32
from constants import *

#Process all the data from the LIDAR
def cb(msg):
    #Determine state
    #degree threshold for the front of the robot, 30 degrees from 0 and 30 degrees from 360
    distance = msg.ranges
    degrees = len(distance)
    proportion = 1/12
    lowFront = degrees - degrees * proportion
    highFront = degrees * proportion
    turnStatus = ""
    closest = min(distance)
    closestDegree = index(min(distance))

    if closest >= 1:
        state = 0
    elif closestDegree > lowFront and closestDegree < highFront:
        state = 1
    elif closest == 1:
        state = 2
    '''
    closest = index(min(distance))
    state = ""
    if closest > lowFront and closest < highFront:
        #wall is directly in front of robot
        state = "APPROACHING"
        turnStatus = "N/A"
    elif closest < lowFront:
        #wall is to the left of the robot
        state = "SEARCHING"
        turnStatus = "Left"
    elif closest > highFront:
        #wall is to the right of the robot
        state = "SEARCHING"
        turnStatus = "Right"
    stateInfo = [state, turnStatus]
    pub_state.publish(stateInfo)
    '''
    
        

    pub_state.publish(s)
    #CALCULATE AND PUBLISH ANYTHING ELSE FOR THE PID



#Init node
rospy.init_node('scan_values_handler')

#Subscriber for LIDAR
sub = rospy.Subscriber('scan', LaserScan, cb)

#Publishers
pub_state = rospy.Publisher('state',Int16, queue_size = 1)
#THINK OF WHAT INFO TO PUBLISH TO THE PID

#Rate object
rate = rospy.Rate(10)

#Keep the node running
while not rospy.is_shutdown():
    rate.sleep() 