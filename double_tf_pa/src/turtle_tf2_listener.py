#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)

    #get all 4 turtles from parameters
    firstTurtle = rospy.get_param('turtle', 'turtle2')
    secondTurtle = rospy.get_param('turtle', 'turtle3')
    thirdTurtle = rospy.get_param('turtle', 'turtle4')
    fourthTurtle = rospy.get_param('turtle', 'turtle5')

    #spawn 4 turtles in the (x,y,z) locations
    spawner(4, 2, 0, firstTurtle)
    spawner(6, 6, 0, secondTurtle)
    spawner(8, 8, 0, thirdTurtle)
    spawner(10, 10, 0, fourthTurtle)

    #create 4 publishers for each respective turtle
    turtle1_vel = rospy.Publisher('%s/cmd_vel' % firstTurtle, geometry_msgs.msg.Twist, queue_size=1)
    turtle2_vel = rospy.Publisher('%s/cmd_vel' % secondTurtle, geometry_msgs.msg.Twist, queue_size=1)
    turtle3_vel = rospy.Publisher('%s/cmd_vel' % thirdTurtle, geometry_msgs.msg.Twist, queue_size=1)
    turtle4_vel = rospy.Publisher('%s/cmd_vel' % fourthTurtle, geometry_msgs.msg.Twist, queue_size=1)

    #create dictionaries for easy and space saving access
    turtleVels = {turtle1_vel: None, turtle2_vel: None, turtle3_vel: None, turtle4_vel: None}
    turtleVelsStr = {turtle1_vel: firstTurtle, turtle2_vel: secondTurtle, turtle3_vel: thirdTurtle, turtle4_vel: fourthTurtle}

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            turtleNum = 1
            for turtle in turtleVels:
                #format the current turtle to follow the previous turtle excluding the first turtle (first turtle should follow teleop turtle)
                followTurtle = 'turtle' + str(turtleNum)
                #get the transformation information between the current turtle and the previous turtle (excluding first turtle that is following teleop)
                turtleVels[turtle] = tfBuffer.lookup_transform(turtleVelsStr[turtle], followTurtle, rospy.Time())
                turtleNum += 1
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        for turtle in turtleVels:
            #loop through all turtles, publish the corresponding angular and linear velocity to each turtle's publishers
            msg = geometry_msgs.msg.Twist()

            trans = turtleVels[turtle]

            msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
            msg.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
            
            turtle.publish(msg)

        rate.sleep()