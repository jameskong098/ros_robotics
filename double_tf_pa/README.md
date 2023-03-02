James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA4 - Double TF PA

EXTRA CREDIT DONE: 3. Have three or more in a chain where turtle3 goes after turtle2 and turtle2 after turtle1

General Overview:

The provided code simulates 4 turtles following one after another with the very first one following the teleop turtle which is controlled by the user. Each turtle will follow the next turtle (i.e. turtle2 -> turtle1, turtle3 -> turtle2, turtle4 -> turtle3, turtle5 -> turtle4). This will form a line of ducks formation where the teleop turtle leads the line of turtles. All of this is done via the turtle_tf2_listener and the turtle_tf2_broadcaster. What the listener does is it listens for transformation updates between two coordinate frames (in our case the positional information between two turtles). What the broadcaster does is it publishes the transformation information between two coordinate frames. Basically the listener subscribes to the transformation information that is produced by the broadcaster.

Code Explanation:

=============================================================
Launch File:

Parameter nodes contain the turtle values so that other nodes can have access to the same information (i.e. broadcaster can access turtle information and listener)

Wrap all parameter turtles with broadcaster nodes to broadcast their information

Launch all necessary turtle sim packages (turtlesim node and teleop node)

Launch listener node
=============================================================

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

turtleNum = 1
for turtle in turtleVels:
    #format the current turtle to follow the previous turtle excluding the first turtle (first turtle should follow teleop turtle)
    followTurtle = 'turtle' + str(turtleNum)
    #get the transformation information between the current turtle and the previous turtle (excluding first turtle that is following teleop)
    turtleVels[turtle] = tfBuffer.lookup_transform(turtleVelsStr[turtle], followTurtle, rospy.Time())
    turtleNum += 1

for turtle in turtleVels:
    #loop through all turtles, publish the corresponding angular and linear velocity to each turtle's publishers
    msg = geometry_msgs.msg.Twist()

    trans = turtleVels[turtle]

    msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
    msg.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
    
    turtle.publish(msg)
