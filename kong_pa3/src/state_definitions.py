'''
state_definitions.py

Purpose: To define various states the robot will be in
'''

#Find the closest wall to follow
SEARCHING = 0

#Wall has been found, start approaching the robot until appropriate following parallel distance is reached
APPROACHING = 1

#Align parallel to the wall (90 Degrees)
ALIGNING = 2

#Robot is aligned so start moving along the wall, making sure to make nay corrections along the way if it
#deviates away from a certain threshold range
FOLLOWING = 3
