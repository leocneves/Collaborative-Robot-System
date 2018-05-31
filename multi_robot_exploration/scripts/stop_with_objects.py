#!/usr/bin/env python
import time as tm
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty, Float32MultiArray
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata

vel = Twist()
pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10 )
time = 0
msg = 0
alt_default = 1500

def callback(msg1):
    global msg
    global vel
    global pub_vel
    msg = msg1
    print msg.data
    if not (len(msg.data) == 0):
        vel.linear.x = 0.0
        pub_vel.publish(vel)
        pub_vel.publish(vel)
        pub_vel.publish(vel)
        print 'ENTROU'
        tm.sleep(10)

def callback_alt(data):
    global pub_vel
    global vel
    h = int(data.altd)
    print h
    if h < (alt_default - 200):
        vel.linear.z = 0.2
        pub_vel.publish(vel)
    elif h >= (alt_default + 200):
        vel.linear.z = -0.2
        pub_vel.publish(vel)
    else:
        vel.linear.z = 0.0
        pub_vel.publish(vel)

def takeoff():
        global pub_vel
        global pub
        global time
        global msg
        rospy.init_node('takeoff', anonymous=True)

        rospy.Subscriber("/objects", Float32MultiArray, callback)
        rospy.Subscriber("/ardrone/navdata", Navdata, callback_alt)

        rate = rospy.Rate(10) # 10hz
        # pub.publish(Empty())
        rate.sleep()
        tm.sleep(5)
        while not rospy.is_shutdown():
            time = rospy.get_time()
            while (rospy.get_time() - time <= 2) and (len(msg.data) == 0):
                vel.linear.x = 0.03
                vel.angular.z = 0.0
                pub_vel.publish(vel)
                print (rospy.get_time() - time)


            time = rospy.get_time()
            while (rospy.get_time() - time <= 2) and (len(msg.data) == 0):
                vel.linear.x = -0.03
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
