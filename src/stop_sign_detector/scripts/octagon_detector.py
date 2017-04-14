#!/usr/bin/env python
import sys
import numpy as np
import rospy
import imutils
import cv2
from matplotlib import pyplot as plt
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
 
class ss_detector:

	def __init__(self):
		self.image_sub = rospy.Subscriber('cv_camera/image_raw', Image, self.callback)
		self.ss_pub = rospy.Publisher('stop_sign_bool', Int32, queue_size = 10)
		self.image_pub = rospy.Publisher('stop_sign_image', Image, queue_size = 10)
		self.thresh_pub = rospy.Publisher('stop_sign_thresh', Image, queue_size = 10)
		self.bridge = CvBridge()
		#self.img2 = cv2.imread(data_path + 'ss1.jpeg', 0)
		self.rate = rospy.Rate(10)
		rospy.spin()

	def detect_shape(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		if len(approx) == 8:
			shape = "octagon"
		else:
			shape = "circle"
 
		# return the name of the shape
		return shape

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
		except CvBridgeError as e:
			print(e)

		(rows, cols, channels) = cv_image.shape
		if cols > 60 and rows > 60:
			cv2.circle(cv_image, (50,50), 10, 255)
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		image = gray
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)[1]
		
		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		
		# loop over the contours
		oct_num = 0
		for c in cnts:
			# compute the center of the contour
			M = cv2.moments(c)
			#cX = int((M["m10"] / (M["m00"] +1e-7)) * ratio)
			#cY = int((M["m01"] / (M["m00"] +1e-7)) * ratio)
			cX = int(M["m10"] / (M["m00"] +1e-7))
			cY = int(M["m01"] / (M["m00"] +1e-7))
			shape = self.detect_shape(c)
			if shape != 'octagon':
				continue
			oct_num += 1	
			# draw the contour and center of the shape on the image
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, shape, (cX, cY),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		 
		self.image_pub.publish(self.bridge.cv2_to_imgmsg(image, "mono8"))	
		self.thresh_pub.publish(self.bridge.cv2_to_imgmsg(thresh, "mono8"))	
			# show the image
			#cv2.imshow("Image", image)
			#plt.imshow(image, 'gray')
			#cv2.waitKey(0)
		print("There are %d octagons"%oct_num)
		
if __name__ == '__main__':
	rospy.init_node('stop_sign_detector', anonymous = True)
	detector = ss_detector()
