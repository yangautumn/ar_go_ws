#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float32
import math
import pdb


class turt:

    def __init__(self):
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        self.turtle_pose = Pose()
        self.vel_msg = Twist()
        self.dt = 0
        self.current_time = rospy.Time.now()
        self.last_time = self.current_time
        self.last_error_x = 0
        self.last_error_theta = 0
        self.error_x_sum = 0
        self.error_theta_sum = 0

    def callback(self, t_pose):
        self.turtle_pose = t_pose

    def get_pose(self):
        return self.turtle_pose

    def pub_velocity(self):
        # x_ref = rospy.Time.now().to_sec()
        # y_ref = math.sin(10*rospy.Time.now().to_sec())
        x_ref = 8
        y_ref = 8
        theta_ref = math.atan((y_ref - 0)/(x_ref - 0))
        self.current_time = rospy.Time.now()
        self.dt = (self.current_time - self.last_time).to_sec()

        error_x = x_ref - self.turtle_pose.x
        error_theta = theta_ref - self.turtle_pose.theta

        derror_x = (error_x - self.last_error_x) / float(self.dt)
        derror_theta = (error_theta - self.last_error_theta) / float(self.dt)

        self.error_x_sum += error_x * self.dt

        norm = math.sqrt(math.pow((x_ref - self.turtle_pose.x), 2) + math.pow((y_ref - self.turtle_pose.y), 2))
        if norm > 0.01:

            self.vel_msg.linear.x = 1 * error_x + 2 * derror_x + 0.01 * self.error_x_sum
            if self.vel_msg.linear.x > 3:
                    self.vel_msg.linear.x = 3
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0
            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = 1 * error_theta
            self.vel_pub.publish(self.vel_msg)
        else:
            self.vel_msg.linear.x = 0
            self.vel_msg.angular.z = 0
        print 'norm {0}'.format(norm)
        self.last_time = self.current_time
        self.last_error_x = error_x
        self.last_error_theta = error_theta

def main():
    rospy.init_node('turtle_class', anonymous=True)
    t1 = turt()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():

        t1.pub_velocity()
        print t1.get_pose()
        # rate.sleep()
        # rospy.spin()


if __name__ == '__main__':
    main()
