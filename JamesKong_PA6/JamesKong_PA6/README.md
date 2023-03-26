James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA6 - Fiducial Follower
=============================================================

EXTRA CREDIT: Robot starts without either fiducial in sight

=============================================================

General Overview:

The provided code will recognize fiducials (a marker placed in the field of view of an imaging system that appears in the image produced, for use as a point of reference or a measure, kinda similar to QR codes). It uses aruco_detect which publishes /fiducial_transforms which contains information such as the translation xyz info relative to the fiducial from the robots camera. The x information gives you which direction the fiducial is from the robots front facing camera (less than 0 being to the left of the robot, more than 0 being to the right of the robot). The z information gives you the distance from the robots front facing camera to the fiducial. The y information is not as relevant, as that concerns more the height. In my case, I focused on the x to navigate directly straight to the fiducial and the z variable to detect when I was at an appropriate distance.

=============================================================

Code Explanation:

#if fiducial is detected
if data.transforms != []:
    fiducial = data.transforms[0]
    translation = fiducial.transform.translation
...
    
#make sure we are always updating the distance, making sure it is not being set to 0 or a None value due to disconnect from fiducial
if translation.z != 0 and translation.z != None:
    self.distance = translation.z
if translation.x != 0 and translation.x != None:
    self.angle = translation.x

#keep moving until close enough distance
if self.distance > 0.50:
    #less than 0 is to the left of the camera, more than 0 is to the right, turn accordingly to stay on track
    if self.angle < 0: 
        self.twist.angular.z = 0.2
    elif self.angle > 0:
        self.twist.angular.z = -0.2

    #move forward
    self.twist.linear.x = 0.2
self.cmd_vel_pub.publish(self.twist)

else:
    #robot is close enough to the fiducial or fiducial is not found -> keep turning
    if self.distance <= 0.50 or self.distance == 0:
        self.twist.linear.x = 0
        self.twist.angular.z = -0.4

    self.cmd_vel_pub.publish(self.twist)