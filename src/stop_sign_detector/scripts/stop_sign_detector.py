#!/usr/bin/env python
import sys
import numpy as np
import cv2
import rospy
from matplotlib import pyplot as plt
from std_msgs.msg import Int32
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class ss_detector:
    
    def __init__(self):
        #data_path = '/home/yang/ar_go_ws/src/stop_sign_detector/data/'
        data_path = '/home/ao/self-driving-car/src/stop_sign_detector/data/'
        #self.image_sub = rospy.Subscriber('cv_camera/image_raw/compressed', CompressedImage, self.callback)
        self.image_sub = rospy.Subscriber('cv_camera/image_raw', Image, self.callback)
        self.ss_pub = rospy.Publisher('stop_sign_bool', Int32, queue_size = 10)
        self.image_pub = rospy.Publisher('stop_sign_image', Image, queue_size = 10)
        self.bridge = CvBridge()
        self.img1 = cv2.imread(data_path + 'ss1.jpeg', 0)
        self.img2 = cv2.imread(data_path + 'ss1.jpeg', 0)          # queryImage
        self.rate = rospy.Rate(10)
        rospy.spin()

         
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            print(e)

        (rows, cols, channels) = cv_image.shape

        self.img2 = cv_image 
        #cv2.waitkey(2)
    
        # Initiate SIFT detector
        img1 = self.img1
        img2 = self.img2
        sift = cv2.xfeatures2d.SIFT_create()
        
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        
        MIN_MATCH_COUNT = 10
        
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()
        
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
        
            img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
            self.ss_pub.publish(1)
            self.rate.sleep()
        
        else:
            print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
            matchesMask = None
        
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                singlePointColor = None,
                matchesMask = matchesMask, # draw only inliers
                flags = 2)
        

        img4 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
        #plt.imshow(img4, 'gray'), plt.show()
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(img4, "bgr8"))

if __name__ == '__main__':
    rospy.init_node('stop_sign_detector', anonymous = True)
    detector = ss_detector()
