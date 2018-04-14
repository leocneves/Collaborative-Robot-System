#!/usr/bin/env python
import time as tm
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty, Float32MultiArray
from geometry_msgs.msg import Twist

vel = Twist()
pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10 )
time = 0
msg = 0

def callback(msg1):
    global msg
    global vel
    msg = msg1
    print msg.data
    if not (len(msg.data) == 0):
        vel.linear.x = 0.0
        pub_vel.publish(vel)
        print 'entrou'
        tm.sleep(0.1)

def takeoff():
        global pub_vel
        global pub
        global time
        global msg
        rospy.init_node('takeoff', anonymous=True)

        rospy.Subscriber("/objects", Float32MultiArray, callback)

        rate = rospy.Rate(10) # 10hz
        pub.publish(Empty())
        rate.sleep()
        tm.sleep(5)
        while not rospy.is_shutdown():
            time = rospy.get_time()
            while (rospy.get_time() - time <= 2) and (len(msg.data) == 0):
                vel.linear.x = 0.1
                vel.angular.z = 0.0
                pub_vel.publish(vel)
                print (rospy.get_time() - time)


            time = rospy.get_time()
            while (rospy.get_time() - time <= 2) and (len(msg.data) == 0):
                vel.linear.x = -0.1
                vel.angular.z = 0.0
                pub_vel.publish(vel)
                print (rospy.get_time() - time)


        rate.sleep()
        vel.linear.x = 0.0
        vel.angular.z = 0.0
        pub_vel.publish(vel)

if __name__ == '__main__':
        try:
          takeoff()
        except rospy.ROSInterruptException:
          pass
