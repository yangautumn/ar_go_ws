#include <ros/ros.h>
#include <stdio.h>
#include <iostream>
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>     //make sure to include the relevant headerfiles
#include <opencv2/highgui/highgui.hpp>
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <cv_bridge/cv_bridge.h>
#include <cvaux.h>
#include <math.h>
#include <cxcore.h>
#include <highgui.h>

/*here is a simple program which demonstrates the use of ros and opencv to do image manipulations on video streams given out as image topics from the monocular vision
of robots,here the device used is a ardrone(quad-rotor).*/
 
using namespace std;
using namespace cv;
namespace enc = sensor_msgs::image_encodings;
 
static const char WINDOW[] = "Image window";
class findcircle
{
    ros::NodeHandle nh_;
    ros::NodeHandle n;
    ros::Publisher pub ;
    image_transport::ImageTransport it_;    
    image_transport::Subscriber image_sub_; //image subscriber 
    image_transport::Publisher image_pub_; //image publisher(we subscribe to ardrone image_raw)
    image_transport::Publisher edges_pub_; //image publisher(we subscribe to ardrone image_raw)
    image_transport::Publisher gray_pub_; //image publisher(we subscribe to ardrone image_raw)
	ros::Publisher pos_pub_;
    std_msgs::String msg;

public:
    findcircle()
    : it_(nh_)
    {
        image_sub_ = it_.subscribe("/cv_camera/image_raw", 1, &findcircle::imageCallBack, this);
        image_pub_= it_.advertise("/camera/image_processed",100);
        gray_pub_= it_.advertise("/camera/image_gray",100);
        edges_pub_= it_.advertise("/camera/image_edges",100);
		pos_pub_ = n.advertise<std_msgs::Int32>("circle_position", 100);
		//pos_pub_ = n.advertise<int>("circle_position", 100);
        //namedWindow(WINDOW);
    }

    ~findcircle()
    {
        //destroyWindow(WINDOW);
    }
    void imageCallBack(const sensor_msgs::ImageConstPtr& original_image)
    { //Convert from the ROS image message to a CvImage suitable for working with OpenCV for processing
        cv_bridge::CvImagePtr cv_ptr, edge_ptr, gray_ptr;
        try
        {
            //Always copy, returning a mutable CvImage
            //OpenCV expects color images to use BGR channel order.
            cv_ptr = cv_bridge::toCvCopy(original_image, enc::BGR8);
            edge_ptr = cv_bridge::toCvCopy(original_image, enc::BGR8);
            gray_ptr = cv_bridge::toCvCopy(original_image, enc::MONO8);
        }
        catch (cv_bridge::Exception& e)
        {
            //if there is an error during conversion, display it
            ROS_ERROR("tutorialROSOpenCV::main.cpp::cv_bridge exception: %s", e.what());
            return;

        }
 
        Mat src_gray;

        /// Convert it to gray
        cvtColor( cv_ptr->image, src_gray, CV_BGR2GRAY );
        cvtColor( cv_ptr->image, gray_ptr->image, CV_BGR2GRAY );

        /// Reduce the noise so we avoid false circle detection
        GaussianBlur( src_gray, src_gray, Size(9, 9), 2, 2 );

        vector<Vec3f> circles;
        /// Apply the Hough Transform to find the circles
        /*
        void HoughCircles(
                        InputArray image, 
                        OutputArray circles, 
                        int method, 
                        double dp, 
                        double minDist, 
                        double param1=100, 
                        double param2=100, 
                        int minRadius=0, 
                        int maxRadius=0 )
        */

        cout << src_gray.size() << endl;
		int ratio = 2;
		int lowThreshold = 100;
		int kernel_size = 3;
		int highThreshold = lowThreshold * ratio;

        //HoughCircles( src_gray, circles, CV_HOUGH_GRADIENT, 2, 20, 100, 245, 20, 300);  // NEEDS TO BE TUNED
        HoughCircles( src_gray, circles, CV_HOUGH_GRADIENT, 2, 10, highThreshold, 100, 20, 300);  // NEEDS TO BE TUNED

        ROS_INFO("Number of circles = %d", circles.size());

		std_msgs::Int32 pos;
		pos.data = 0;
		//int pos = 0;
        /// Draw the circles detected
		Mat detected_edges, dst;
		Canny( src_gray, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );
		edge_ptr->image = Scalar::all(0);
		cv_ptr->image.copyTo(edge_ptr->image, detected_edges);			
        for( size_t i = 0; i < circles.size(); i++ )
        {
            ROS_INFO("DRAWING CIRCLE");
            Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
            int radius = cvRound(circles[i][2]);
            // circle center
            circle( cv_ptr->image, center, 3, Scalar(0,255,0), -1, 8, 0 );
            // circle outline
            circle( cv_ptr->image, center, radius, Scalar(0,0,255), 3, 8, 0 );
			if (center.x < src_gray.size().width / 2)
				pos.data = 1;
			else
				pos.data = 2;
        }

        /// Show your results
        //imshow( WINDOW, cv_ptr->image );
		image_pub_.publish(cv_ptr->toImageMsg());	
		gray_pub_.publish(gray_ptr->toImageMsg());
		edges_pub_.publish(edge_ptr->toImageMsg());
		pos_pub_.publish(pos);
        ROS_INFO("%d", pos.data);

        waitKey(3);   
 
    }
};
 
 
int main(int argc, char** argv)
{
    ros::init(argc, argv, "find_circle");
    findcircle ic;
    ros::spin();

    return 0;
}




/*

Parameters: 
image – 8-bit, single-channel, grayscale input image.
circles – Output vector of found circles. Each vector is encoded as a 3-element floating-point vector  (x, y, radius) .
circle_storage – In C function this is a memory storage that will contain the output sequence of found circles.
method – Detection method to use. Currently, the only implemented method is CV_HOUGH_GRADIENT , 
    which is basically 21HT , described in [Yuen90].
dp – Inverse ratio of the accumulator resolution to the image resolution. For example, if dp=1 , 
    the accumulator has the same resolution as the input image. If dp=2 , the accumulator has half as big width and height.
minDist – Minimum distance between the centers of the detected circles. If the parameter is too small, 
    multiple neighbor circles may be falsely detected in addition to a true one. If it is too large, some circles may be missed.
param1 – First method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the higher threshold of the two 
    passed to the Canny() edge detector (the lower one is twice smaller).
param2 – Second method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the accumulator threshold 
    for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. 
    Circles, corresponding to the larger accumulator values, will be returned first.
minRadius – Minimum circle radius.
maxRadius – Maximum circle radius.

*/
