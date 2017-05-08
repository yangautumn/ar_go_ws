#include "ros/ros.h"
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "std_msgs/Int32.h"
#include "sensor_msgs/Image.h"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/features2d.hpp"
#include "opencv2/xfeatures2d/nonfree.hpp"
#include <image_transport/image_transport.h>

class ss_detector {
private:
	ros::NodeHandle nh_;
	image_transport::Subscriber image_sub_;
	image_transport::Publisher image_pub_;
	image_transport::ImageTransport it_;
	cv::Mat ss_image = cv::imread("../data/ss1.jpeg", 0);	
public:
	ss_detector(): it_(nh_) {
		image_sub_ = it_.subscribe("/cv_camera/image_raw", 100, &ss_detector::callback, this);
		image_pub_ = it_.advertise("/stop_sign_image", 100);
	}	
	~ss_detector(){}
	void callback(const sensor_msgs::ImageConstPtr& msg) {
		cv_bridge::CvImagePtr camera_image, output;
		try {
			camera_image = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
		}
		catch (cv_bridge::Exception& e) {
			ROS_ERROR("cv_bridge exception: %s", e.what());
			return ;
		}
		
		//cv::SiftFeatureDetector sift;
		cv::xfeatures2d::SIFT sift;
		//std::vector<cv::KeyPoint> camera_kp, ss_kp;
		//sift(camera_image, camera_kp, cv::noArray());
		//sift.detect(camera_image, camera_kp);
		//sift.detect(ss_image, ss_kp);
		//cv::drawKeypoints(camera_image, camera_kp, output);
		//image_pub_.publish(camera_image->toImageMsg());
		image_pub_.publish(output->toImageMsg());
	}
};

int main(int argc, char **argv)
{
	ros::init(argc, argv, "stop_sign_detector");
	ss_detector detector;
	ros::spin();
	return 0;
}
