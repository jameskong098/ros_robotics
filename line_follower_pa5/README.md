James Kong
COSI 119A - Autonomous Robotics
Pito Salas
PA5 - Line Follower
=============================================================

EXTRA CREDIT DONE: Robot is able to double back along the line allowing it to follow the line infinitely

=============================================================

General Overview:

The provided code follows a yellow line on the ground. The program subscribes to the '/camera/rgb/image_raw' topic to receive an image stream from the builtin camera on the robot. It then takes that image stream and filters everything not within the range of Yellow values to then obtain a 20 pixel mask. This allows us to then use a centroid to center in the middle of the line in the mask where we can then direct the turtle to move in the direction of the centroid. Lastly, if the robot no longer detects a line in front of it, it will turn around and continue back along the line. 

=============================================================

Code Explanation:

# clear all but a 20 pixel band near the top of the image
    h, w, d = image.shape
    search_top = int(3 * h /4)
    search_bot = search_top + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0

 # Compute the "centroid" and display a red circle to denote it
        M = cv2.moments(mask)
        self.logcount += 1
        print("M00 %d %d" % (M['m00'], self.logcount))

        #yellow line detected
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00']) + 100
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1)

# Move at 0.2 M/sec
# add a turn if the centroid is not in the center
            err = cx - w/2
            self.twist.linear.x = 0.2
            ang_vel = ang_vel_control(-float(err) / 100)
            self.twist.angular.z = ang_vel
            self.cmd_vel_pub.publish(self.twist)
            self.centroid_pub.publish(self.bridge.cv2_to_imgmsg(image))
        else:
#yellow line not detected meaning robot has reached end of line, turn around
            self.twist.linear.x = 0
            self.twist.angular.z = 0.5
            self.cmd_vel_pub.publish(self.twist)
        #cv2.imshow("image", image)