HOW TO RUN: Enter the code into the shell:

roslaunch kong_pa3 kong_pa3.launch

This will launch all three of the nodes correctly if they are marked as executable.

===================================================================================================

General Overview:

This package contains Python code that will direct a robot to

1) Find a wall
2) Turn to become parallel to the wall
3) Follow along the side of the wall
4) Make any adjustments to its trajectory if necessary (any deviations outside a threshold will automatically guide the robot back within the threshold)

The code works based off a number of checks for the trajectory of the robot. It depends on using the LiDAR scanner to get the corresponding 360 degree values of the robot.
The robot detects which direction the wall is based off of the degrees detected by the robot. The robot also continuously checks the orientation of the robot 
by seeing if the distance from the wall is within a certain threshold and will guide itself back to within that threshold. It will also check if it is parallel to the
wall during each step. There are multiple states for the robot to be in: SEARCHING, APPROACHING, ALIGNING, and FOLLOWING. Searching is for finding the wall to follow.
Approaching is for when the wall is found and the robot must move towards the robot. Aligning is when the robot is within following distance of the robot but must
be aligned parallel to the wall in order to properly following the side of the wall. Following is the final stage where the robot moves straight along the wall
and makes any necessary corrections based off a range of distance values the robot is allowed to be a certain distance away from the wall from.

This programming assignment was rather difficult, and there was a lot of trouble figuring out small issues as you have to consider how the different states
can overlap with each other and cause issues. Multiple times I had to change previous states because one state would accidentally be entered when its not supposed to.
This issue would be very annoying because certain states would not be reached when they were supposed to and then the robot will get lost, get stuck doing the
same task (continuously turning), and other troubles.
