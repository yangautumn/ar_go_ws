#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float32
import math
import pdb

def move():

    rospy.init_node('robot_cleaner', anonymous=True)
    last_time = rospy.Time.now()
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pose_publisher = rospy.Publisher('/turtle1/pose', Pose, queue_size=10)
    error_publisher = rospy.Publisher('/turtle1/norm', Float32, queue_size=10)
    vel_msg = Twist()
    turtle_pose = Pose()

    x_ref = 8
    y_ref = 8

    theta_ref = math.atan((y_ref - 0)/(x_ref - 0))
    norm = math.sqrt(math.pow((x_ref - turtle_pose.x),2) + math.pow((y_ref - turtle_pose.y),2))
    if norm > 0.01:
        vel_msg.linear.x = 0.5
        vel_msg.linear.y =0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 1 * (theta_ref - turtle_pose.theta)
    # print vel_msg
    print 'norm {0}'.format(norm)
    current_time = rospy.Time.now()
    dt = (current_time - last_time).to_sec()
    # pdb.set_trace()
    # simplified unicycle dynamics
    turtle_pose.x = turtle_pose.x + dt * vel_msg.linear.x * math.cos(math.radians(turtle_pose.theta))
    turtle_pose.y = turtle_pose.y + dt * vel_msg.linear.x * math.sin(math.radians(turtle_pose.theta))
    turtle_pose.theta = turtle_pose.theta + dt * vel_msg.angular.z



    print turtle_pose
    velocity_publisher.publish(vel_msg)
    # pose_publisher.publish(turtle_pose)
    error_publisher.publish(norm)

def main():
    # pdb.set_trace()
    i = 0
    while not rospy.is_shutdown():
        i = i + 1
        if i > 100000:
            print 'the value of i {0}'.format(i)
            break

        move()





if __name__ == '__main__':
    main()
