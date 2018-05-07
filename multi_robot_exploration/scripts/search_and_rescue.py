#!/usr/bin/env python

import sys
import rospy
import os
import numpy as np
import time
import roslaunch
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from hector_uav_msgs.msg import Altimeter
from hector_uav_msgs.srv import EnableMotors
from sensor_msgs.msg import NavSatFix


class Rips:

    def __init__(self):

        # rospy.Subscriber('/scan', LaserScan, self.laser_callback)

        self.cmd_vel_pub_pelican = rospy.Publisher("pelican/cmd_vel", Twist, queue_size=10)
        rospy.Service('pelican/enable_motors', EnableMotors, 'true')
        # rospy.Subscriber('pelican/altimeter', Altimeter, self.altimeter_callback)
        rospy.Subscriber('pelican/fix', NavSatFix, self.altimeter_callback)
        rospy.Subscriber('objects', Float32MultiArray, self.search_callback)
        self.height = 0
        self.count = 0
        self.vel_pelican = Twist()
        self.control = False
        self.file = '/home/leonardo/catkin_ws/src/waypoint_nav/outdoor_waypoint_nav/waypoint_files/points_sim.txt'

        t = rospy.get_time()

        while (rospy.get_time() - t) <= 4:
            self.vel_pelican.linear.x = 0.0
            self.vel_pelican.angular.z = 0.0
            self.vel_pelican.linear.z = 0.3
            self.cmd_vel_pub_pelican.publish(self.vel_pelican)
            print 'o'
        self.vel_pelican.linear.x = 0.0
        self.vel_pelican.angular.z = 0.0
        self.vel_pelican.linear.z = 0.0
        self.cmd_vel_pub_pelican.publish(self.vel_pelican)


    def search_callback(self, data):
        self.control = len(data.data) == 0
        if not self.control:
            self.count += 1
            if self.count >= 20:
                self.goTo()
        else:
            self.count = 0

    def goTo(self):
        print 'FOIII'
        os.remove(self.file)
        file = open(self.file,'w+')
        file.write(str(np.round(self.latitude,8)) + " " + str(np.round(self.longitude,8)) + "\n")
        # file.flush()
        file.close()
        time.sleep(3)
        os.system("roslaunch outdoor_waypoint_nav send_goals_sim.launch")
        time.sleep(60)

    def altimeter_callback(self, msg):
        self.latitude = msg.latitude
        self.longitude = msg.longitude
        self.height = msg.altitude

        print msg.altitude

        if self.height <= 2.5:
            self.vel_pelican.linear.x = 0.0
            self.vel_pelican.linear.y = 0.0
            self.vel_pelican.linear.z = 0.4
            self.vel_pelican.angular.x = 0.0
            self.vel_pelican.angular.y = 0.0
            self.vel_pelican.angular.z = 0.0
            self.cmd_vel_pub_pelican.publish(self.vel_pelican)
            print 'sobe'

        elif self.height >= 3.0:
            self.vel_pelican.linear.x = 0.0
            self.vel_pelican.linear.y = 0.0
            self.vel_pelican.linear.z = -0.4
            self.vel_pelican.angular.x = 0.0
            self.vel_pelican.angular.y = 0.0
            self.vel_pelican.angular.z = 0.0
            self.cmd_vel_pub_pelican.publish(self.vel_pelican)
            print 'desce'
        else:
            # self.vel_pelican.linear.z = 0.0
            # self.cmd_vel_pub_pelican.publish(self.vel_pelican)
            # self.control = True
            print 'ok'
            if self.control:
                self.vel_pelican.linear.x = 0.4
                self.vel_pelican.linear.z = 0.0
                self.vel_pelican.angular.z = 0.1
                self.cmd_vel_pub_pelican.publish(self.vel_pelican)
            else:
                self.vel_pelican.linear.x = 0.0
                self.vel_pelican.linear.z = 0.0
                self.vel_pelican.angular.z = 0.0
                self.cmd_vel_pub_pelican.publish(self.vel_pelican)

        # time.sleep(0.1)


def main(args):
    rospy.init_node('search_and_rescue', anonymous=True)
    Rips()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main(sys.argv)
