#!/usr/bin/env python

'''
James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA3 - Wall Follower
'''

import rospy
from state_definitions import *
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16, Float32

#Makes the state message global
def cb_state(msg):
    global state
    state = msg

'''
#Makes the twist object sent from PID global
def cb_twist(msg):
    global t_pid
    t_pid = msg
    pub_vel.publish(t_pid)
'''

#See if any wall is within the front range of the robot
def checkInFront(distance):
    return closestDegree > leftFront or closestDegree < rightFront

#check if the robot is parallel to the wall
def checkParallel():
    threshold = 10
    lowRight = rightSide - threshold
    highRight = rightSide + threshold
    lowLeft = leftSide - threshold
    highLeft = leftSide + threshold
    if closestSide == "Right":
        if closestDegree >= lowRight and closestDegree <= highRight:
            return True
    elif closestSide == "Left":
        if closestDegree >= lowLeft and closestDegree <= highLeft:
            return True
    return False

#see if the robot is within range to the wall
def checkCloseEnough():
    return closest >= 0.2 and closest <= 0.7

#If the robot is too far from the wall while following it, signal if it's too close, too far, or nothing if it is within range
def adjustTrajectory():
    if closest < 0.4:
        return "Too Close"
    elif closest > 0.6:
        return "Too Far"
    return ""

#see which side of the robot is closer to a wall
def checkCloserSide():
    if abs(closestDegree - rightSide) < abs(closestDegree - leftSide):
        return "Right"
    return "Left"

#laser scan call back, filters location data and degree data, then updates appropriate state
def scan_cb(msg):
    global closest; global state; global closestDegree
    distance = msg.ranges
    closest = min(distance)
    closestDegree = distance.index(closest)
    if closest >= 1:
        if checkInFront(distance) == False:
            state = 0
        else:
            state = 1
    elif checkCloseEnough() == True:
        if checkParallel() == False:
            state = 2
        else:
            state = 3

#Init node
rospy.init_node('driver')

#Make publisher for cmd_vel
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

#Make all subscribers
sub_state = rospy.Subscriber('state', Int16, cb_state)
#sub_pid_twist = rospy.Subscriber('pid_twist', Twist, cb_twist)
sub_laser = rospy.Subscriber('scan', LaserScan, scan_cb)

#odom_sub = rospy.Subscriber('odom', Odometry, odom_cb)

#Rate object
rate = rospy.Rate(10)

#state of the robot and the closest wall to the robot
state = 0
closest = 0

#range of degree values for what determines is in front of the robot
leftFront = 329
rightFront = 29

#range of degree values for what determines is on the side of the robot
rightSide = 269
leftSide = 89

#the degree of the closest wall relative to the robot and which side is the closest to the robot
closestDegree = 0
closestSide = "N\A"


#Create two twist variable, one is modified here, one is copied from the PID messages
t_pub = Twist()
t_pid = Twist()

#Linear speed of the robot
LINEAR_SPEED = 0.3
#Angular speed of the robot
ANGULAR_SPEED = 3.1415926/6

#dictionary for better readability when printing (good for debugging)
stateDict = {0: "SEARCHING", 1: "APPROACHING", 2: "ALIGNING", 3: "FOLLOWING", 4: "LOST"}

print("STARTING")

while not rospy.is_shutdown():
    print("STATE: ", stateDict[state])
    print("DISTANCE: " + str(closest))
    print("DEGREE OF WALL: " + str(closestDegree) + "°")
    print("Parallel Status: " + str(checkParallel()))
    print("Closest Side: " + str(closestSide))
    print()
    if (state == SEARCHING):
        if closestDegree < leftFront:
            #wall is to the left of the robot, turn left to face direction of wall
            t_pub.linear.x = 0
            t_pub.angular.z = ANGULAR_SPEED
        elif closestDegree > rightFront:
            #wall is to the right of the robot, turn right to face direction of wall
            t_pub.linear.x = 0
            t_pub.angular.z = -1 * ANGULAR_SPEED

    elif (state == APPROACHING):
        t_pub.angular.z = 0
        t_pub.linear.x = LINEAR_SPEED

    elif (state == ALIGNING):
        if closestSide == "N\A":
            closestSide = checkCloserSide()
        elif closestSide == "Right":
            #wall is closer to the right of the robot, turn left to face parallel to the wall
            t_pub.linear.x = 0
            t_pub.angular.z = ANGULAR_SPEED
        else:
            #wall is closer to the left of the robot, turn right to face parallel to the wall
            t_pub.linear.x = 0
            t_pub.angular.z = -1 * ANGULAR_SPEED

    elif (state == FOLLOWING):
        #check if robot is drifting off track or not
        whichBounds = adjustTrajectory()
        if whichBounds == "Too Close":
            if closestSide == "Right":
                #too close to the wall on the right side of robot, move left away from the robot
                t_pub.linear.x = LINEAR_SPEED
                t_pub.angular.z = ANGULAR_SPEED
            else:
                #too close to the wall on the left side of robot, move right away from the robot
                t_pub.linear.x = LINEAR_SPEED
                t_pub.angular.z = -1 * ANGULAR_SPEED
        elif whichBounds == "Too Far":
            if closestSide == "Right":
                #too far away from wall on the right side of robot, move right towards the robot
                t_pub.linear.x = LINEAR_SPEED
                t_pub.angular.z = -1 * ANGULAR_SPEED
            else:
                #too far away from wall on the left side of robot, move left towards the robot
                t_pub.linear.x = LINEAR_SPEED
                t_pub.angular.z = ANGULAR_SPEED
        else:
            #right on track within threshold, continue moving straight
            t_pub.angular.z = 0
            t_pub.linear.x = LINEAR_SPEED

    else:
        print("STATE NOT FOUND")

    pub_vel.publish(t_pub)
    rate.sleep()
