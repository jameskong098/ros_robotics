#!/usr/bin/env python

'''
James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA1 - Out and Back
'''

from geometry_msgs.msg import Twist
import rospy
import math

vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

rospy.init_node('PA1')

start_secs = rospy.Time.now().secs

#how long to travel
duration = 6
#how long to rotate
timeToRotate = 4

twist = Twist()

#calculates the time elapsed from start of program
def calcElapsed():
    current_secs = rospy.Time.now().secs
    elapsed = current_secs - start_secs
    return elapsed

#stops the node from running, kills all movement
def stop():
    twist.linear.x = 0
    twist.angular.z = 0
    vel_pub.publish(twist)
    rospy.signal_shutdown("Robot returned!")

#rotates for a inputted amount of time with an inputted amount of radians per second
def timedRotate(angular, elapsed):
    tempDuration = elapsed + timeToRotate
    twist.linear.x = 0
    while elapsed <= tempDuration:
        twist.angular.z = angular
        vel_pub.publish(twist)
        elapsed = calcElapsed()
    twist.angular.z = 0
    vel_pub.publish(twist)

#makes robot go in a square formation when run 4 times in while loop, / 4.476 since 
# we are given 4 seconds for rotation, extra .476 to account for random factors
def drawSquare(elapsed):
    if elapsed == 6:
        timedRotate((math.pi / 2) / 4.476, elapsed)
    elif elapsed == 16:
        timedRotate((math.pi / 2) / 4.476, elapsed)
    elif elapsed == 26:
        timedRotate((math.pi / 2) / 4.476, elapsed)
    elif elapsed == duration * 4 + timeToRotate * 3:
        stop()
    else:
        twist.linear.x = 0.2
        vel_pub.publish(twist)

#makes robot go forward and backwards when run two times in while loop, / 4.476 since 
# we are given 4 seconds for rotation, extra .476 to account for random factors
def forwardBackward(elapsed):
    if elapsed == duration:
        timedRotate(math.pi / 4.476, elapsed)
    elif elapsed == duration * 2 + timeToRotate:
        stop()
    else:
        twist.linear.x = 0.2
        vel_pub.publish(twist)

while not rospy.is_shutdown():
    elapsed = calcElapsed()
    forwardBackward(elapsed)
    #drawSquare(elapsed)

#Extra Credit Done: modularity, forming a square
#Note: uncomment drawSquare and comment out forwardBackward to test drawSquare as only one can run at a time