#!/usr/bin/env python

'''
James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA2 - Teach Your Robot To Dance
'''

import rospy
import sys
import math
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

#scanner callback that returns laser info and closeness to objects
def scan_cb(msg):
   global state
   ranges = msg.ranges
   if state != 'h':
      for distance in ranges:
        #ignore inf distance in sim and 0.0 distance in real due to laser inaccuracies
         if math.isinf(distance) == False and distance != 0.0:
            if distance <= 0.2:
               state = 'h'

#key call back that updates the pressed key state
def key_cb(msg):
   global state; global last_key_press_time; global previousState
   previousState = state
   state = msg.data
   last_key_press_time = rospy.Time.now()

#determines what kind of speed should be displayed
def determineSpeedType(state, msg):
    global curSpeed
    if state == "f" or state == "b":
       curSpeed = " [Linear]: " + f"{msg.twist.twist.linear.x:.8f}"
    elif state == "l" or state == "r":
       curSpeed = " [Angular]: " + f"{msg.twist.twist.angular.z:.8f}"
    elif state == "s" or state == "z" or state == "c":
       curSpeed = " [Linear, Angular]:  " + f"{msg.twist.twist.linear.x:.8f}" + ", " + f"{msg.twist.twist.angular.z:.8f}"
    else:
        curSpeed = " [Linear, Angular]: 0, 0"

#odom callback that updates location info
def odom_cb(msg):
   global curLocation
   if state == "h":
       determineSpeedType(previousState, msg)
   else:
       determineSpeedType(state, msg)
   #format the (x,y z) positions into a more readable format and update curLocation with new array of positions
   curLocation = [f"{msg.pose.pose.position.x:.8f}", f"{msg.pose.pose.position.y:.8f}", f"{msg.pose.pose.position.z:.8f}"]

#prints the state of the robot
def print_state():
   print("---")
   print("STATE: " + stateDict[state])
   print("PREVIOUS STATE: " + stateDict[previousState])
   print("SPEED" + str(curSpeed))
   print("POSITION: " + "x: " + str(curLocation[0]) + " y: " + str(curLocation[1]) + " z: " + str(curLocation[2]))
   # calculate time since last key stroke
   time_since = rospy.Time.now() - last_key_press_time
   print("SECS SINCE LAST KEY PRESS: " + str(time_since.secs))

#makes robot move in a spiral movement
def spiral(t):
    global spiralVal
    if spiralVal < 0.6:
        t.linear.x = 0.2
        t.angular.z = spiralVal
        spiralVal += 0.001
    else: 
        state = "h"
        spiralVal = 0.3

#calculates the time elapsed from start of program
def calcElapsed(start_secs):
    current_secs = rospy.Time.now().secs
    elapsed = current_secs - start_secs
    return elapsed

#makes robot move in a zigzag movement
def zigZag(t):
    global zigTimeStart; global zigStatus; global zagStatus; global forwardStatus; global prevStatus
    if zigTimeStart == 0:
        zigTimeStart = rospy.Time.now().secs
    duration = calcElapsed(zigTimeStart)
    #if the robot has not performed the current action for 3 seconds, continue to perform it
    if duration <= 3:
        if forwardStatus == True:
            t.linear.x = 0.2
            if prevStatus == "zig":
                zagStatus = True
            elif prevStatus == "zag":
                zigStatus = True
        elif zigStatus == True:
            t.angular.z = 0.3
        elif zagStatus == True:
            t.angular.z = -0.3
    else: 
        #if robot finished current action, change status to perform the next appropriate action 
        zigTimeStart = 0
        if forwardStatus == True:
            forwardStatus = False
        elif zigStatus == True:
            zigStatus = False
            prevStatus = "zig"
            forwardStatus = True
        elif zagStatus == True:
            zagStatus = False
            prevStatus = "zag"
            forwardStatus = True

#makes robot move in a circle motion
def circle(t):
    t.linear.x = 0.2
    t.angular.z = 0.5
    
# init node
rospy.init_node('dancer')

# subscribers/publishers
scan_sub = rospy.Subscriber('scan', LaserScan, scan_cb)

# RUN rosrun kong_pa2 key_publisher.py to get /keys
key_sub = rospy.Subscriber('keys', String, key_cb)
odom_sub = rospy.Subscriber('odom', Odometry, odom_cb)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

#variables that are used for print_state function
#dictionary for better readability for printing
stateDict = {"h": "Halt", "l": "Left", "r": "Right", "f": "Forward", "b": "Backward", "s": "Spiral", "z": "Zig-Zag", "c": "Circle", "": "n/a"}
state = "h"
previousState = ""
curSpeed = 0
curLocation = [0, 0, 0]
spiralVal = 0.3

#variables used for zigZag function
zigTimeStart = 0
forwardStatus = False
zigStatus = True
zagStatus = False
prevStatus = ""

last_key_press_time = rospy.Time.now()

# set rate
rate = rospy.Rate(10)

# Wait for published topics, exit on ^c
while not rospy.is_shutdown():

   # print out the current state and time since last key press
   print_state()

   # publish cmd_vel from here 
   t = Twist()
   
   #check if each key obtained from key_publisher to match to its corresponding state
   if state == "l":
       t.angular.z = 0.2
   elif state == "r":
       t.angular.z = -0.2
   elif state == "f":
       t.linear.x = 0.2
   elif state == "b":
       t.linear.x = -0.2
   elif state == "h":
       t.linear.x = 0
   elif state == "s":
        spiral(t)
   elif state == "z":
        zigZag(t)
   elif state == "c":
        circle(t)
       
   cmd_vel_pub.publish(t)

   # run at 10hz
   rate.sleep()
  
  #Extra Credit: Run this example with a real robot, Invent additional commands that do other motions