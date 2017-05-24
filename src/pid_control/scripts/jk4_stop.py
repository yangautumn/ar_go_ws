#!/usr/bin/env python

from ros_pololu_servo.msg import MotorStateList
from ros_pololu_servo.msg import MotorState
from ros_pololu_servo.msg import MotorCommand
from std_msgs.msg import Float64
from std_msgs.msg import Int32

import rospy
import sys, signal


class car:

	def __init__(self):

		self.actuator_states = MotorStateList()
		self.states_sub = rospy.Subscriber("/pololu/motor_states", MotorStateList, self.callback_states)
		self.steering_pub = rospy.Publisher("/pololu/command", MotorCommand, queue_size=1)
		self.distance_pub_r = rospy.Publisher("/right_ir",Float64, queue_size=1)
		self.distance_pub_l = rospy.Publisher("/left_ir",Float64, queue_size=1)
		self.error_pub = rospy.Publisher("/error",Float64, queue_size=1)
		self.controlEffort_pub = rospy.Publisher("/u",Float64, queue_size=1)
		self.stop_sub = rospy.Subscriber("/stop_sign_bool", Int32, self.callback_stop)
		self.dt = 0
		self.current_time = rospy.Time.now()
		self.last_time = self.current_time
		self.last_error = 0
		self.error_sum = 0
		self.Kp = 3 
		self.Kd = .2
		self.i = 1
		self.stop_detected = False
		

	def callback_stop(self,data):

		
		if data.data==1:
			self.stop_detected = True
			print "stop detected"
		else:
			self.stop_detected = False
			print "no stop detected"

	def callback_states(self, states):
		self.actuator_states = states
		left_ir = states.motor_states[0].pulse
		right_ir = states.motor_states[1].pulse
		d_ref = 142
		#d_ref = 95
		#d_ref = 120
		
		print states.motor_states[1].pulse

		# Publish left IR state : distance from the wall
		self.distance_pub_r.publish(states.motor_states[1].pulse)
		self.distance_pub_l.publish(states.motor_states[0].pulse)
		servo_cmd = MotorCommand()
		self.current_time = rospy.Time.now()
		#self.dt = (self.current_time - self.last_time).to_sec()

		error = left_ir - right_ir
		self.error_pub.publish(error)

		if error<-2:
			u = float(self.Kp)*error/5.58
		elif error>2:
			u = float(self.Kp)*error/25.67
		else:
			u = 0
			
		
		
		if u>3:
			u = 2.2
		elif u<-17:
			u = -17
				
		# Publish steering control effort
		self.controlEffort_pub.publish(u)
		#print u
		servo_cmd.position = u					
		servo_cmd.joint_name = "steering"	
		self.steering_pub.publish(servo_cmd)

		
		servo_cmd.joint_name = "thrust"
		servo_cmd.speed = float(0)
		servo_cmd.acceleration = float(0)

		if self.stop_detected == True:
				
				servo_cmd.position = float(0)
		else:
				servo_cmd.position = float(0.48)

		#servo_cmd.position = float(0)	

		self.steering_pub.publish(servo_cmd)			

		
		self.last_time = self.current_time
		self.last_error = error
		

	def steer_pub(self):
		servo_cmd = MotorCommand()
		#print self.actuator_states.motor_states[1].pulse
		servo_cmd.position = float (1*(140-self.actuator_states.motor_states[1].pulse))/215
		servo_cmd.joint_name = "steering"	
		self.steering_pub.publish(servo_cmd)		



def main():
    
	rospy.init_node('jk_steering',anonymous=True)
	c1 = car()
	rate = rospy.Rate(100)
	rospy.spin()
	#while not rospy.is_shutdown():
		#rospy.spin()
		#c1.steer_pub()
		
	rate.sleep() 
		
	

if __name__ == '__main__':
	main()
