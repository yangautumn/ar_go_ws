#!/usr/bin/env python
import sys
import numpy as np
import cv2
import rospy
from matplotlib import pyplot as plt
from std_msgs.msg import Int32
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class findCircle:
	def __init__(self):
		self.image_sub = rospy.Subscriber('cv_camera/image_raw', Image, self.callback)
		self.image_pub = rospy.Publisher('circle_image', Image, queue_size = 10)
		self.edge_pub = rospy.Publisher('edge_image', Image, queue_size = 10)
		self.gray_pub = rospy.Publisher('gray_image', Image, queue_size = 10)
		self.pos_pub = rospy.Publisher('circle_position', Int32, queue_size = 10)
		self.rate = rospy.Rate(10)
		self.bridge = CvBridge()
		self.pos = 0
		rospy.spin()
	
	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
		except CvBridgeError as e:
			print(e)

		cv_image = cv2.medianBlur(cv_image,5)
		gray_image = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)

		(rows, cols, channels) = cv_image.shape

		circles = cv2.HoughCircles(gray_image,cv2.HOUGH_GRADIENT,2,1000,param1=50,param2=180,minRadius=20,maxRadius=200)

		if circles != None:	
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
			    # draw the outer circle
				cv2.circle(cv_image,(i[0],i[1]),i[2],(0,255,0),2)
    			# draw the center of the circle
				cv2.circle(cv_image,(i[0],i[1]),2,(0,0,255),3)
				if i[0] < cols / 2:
					pos = 1
				else:
					pos = 2	

		self.pos_pub.publish(self.pos)
		self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		self.gray_pub.publish(self.bridge.cv2_to_imgmsg(gray_image, "mono8"))

if __name__ == '__main__':
	rospy.init_node('circle_detector', anonymous = True)
	detector = findCircle()
