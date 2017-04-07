#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float32
import math

def move(i):

    rospy.init_node('robot_cleaner', anonymous=True)
    last_time = rospy.Time.now()
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pose_publisher = rospy.Publisher('/turtle1/pose', Pose, queue_size=10)
    turtle_pose = Pose()
    vel_msg = Twist()
    turtle_pose.x = 5
    turtle_pose.y = 5
    turtle_pose.theta = 0.5
    # if i == 1:
    #     turtle_pose.x = 0
    #     turtle_pose.y = 0
    #     turtle_pose.theta = 0
    #
    # else:
    #     turtle_pose.x = 8
    #     turtle_pose.y = 8
    #     turtle_pose.theta = 0.9
    vel_msg.linear.x = 0.5
    vel_msg.linear.y =0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0.5
    velocity_publisher.publish(vel_msg)
    # pose_publisher.publish(turtle_pose)
    # print turtle_pose


def main():
    # pdb.set_trace()
    i = 0
    while not rospy.is_shutdown():
        # i = i + 1
        # if i > 2:
        #     print 'the value of i {0}'.format(i)
        #     break

        move(i)


if __name__ == '__main__':
    main()
