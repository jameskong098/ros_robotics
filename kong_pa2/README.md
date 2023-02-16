James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA2 - Teach Your Robot To Dance

General Overview:

Executable Python program that allows control of a robot via keyboard keys being pressed. Keyboard keys are published via key_publisher.py and received by key_publisher subscriber in program. Program includes code to process laser scan data. Laser scan subscriber has callback function scan_cb(msg) which takes the ranges array and finds the closest object by searching the array for any value less than or equal to 0.2 that is not inf or 0.0 (inf in gazebo or 0.0 in real). Zig-zag was programed based off duration. Function would continually check the current elapsed time and change the state to either zig, zag, or forward in each function call once the duration was up. Time elapsed would be reset and rechecked after each status change. All other keys (left, right, forward, backwards, halt) are straight forward and just required single line commands with t.linear.x or t.angular.z). Circle function required simultaneous changes to both linear and angular to achieve a circular motion since you need to be turning while moving forward. Spiral was a similar process but required increasing the angular speed to achieve a circle motion that progressively gets smaller due to the angular speed increasing (and thus turning faster to make the circle smaller and into a spiral). To determine the speed, I would check the previous state with a prevState variable to display the appropriate corresponding speed. 

Reflection: 

This assignment was fun to code, and I feel like I learned a lot about how publishers and subscribers work. I learned how to figure out the message type and then obtain the necessary information from it and basically clean the information up to be more presentable and useful. It reminded me a lot of API calls and how you have to sometimes clean up the information. Lastly, this assignment really helped me understand how ROS processes each command as for the zig-zag function I really had to think of a method that would accommodate ROS's one by one command execution as this was tough to figure out due to the required sequential forwards, zigs, and zags each for specific durations.

List of functions and what they do:

scan_cb(msg) - scanner callback that returns laser info and closeness to objects

key_cb(msg) - key call back that updates the pressed key state

determineSpeedType(state, msg) - determines what kind of speed should be displayed

odom_cb(msg) - odom callback that updates location info

print_state() - prints the state of the robot

spiral(t) - makes robot move in a spiral movement

calcElapsed(start_secs) - calculates the time elapsed from start of program

zigZag(t) - makes robot move in a zigzag movement

circle(t) - makes robot move in a circle motion