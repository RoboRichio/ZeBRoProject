#include <stdio.h>
#include <iostream>
#include <fstream>
#include <math.h>
#include "opencv2/core.hpp"
#include "opencv2/features2d.hpp"
#include "opencv2/xfeatures2d.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/calib3d.hpp"
#include "opencv2/imgproc.hpp"
using namespace std;
using namespace cv;
using namespace cv::xfeatures2d;

//vector of keypoints   
std::vector< cv::KeyPoint > keypoints_1; //keypoints for object
std::vector< cv::KeyPoint > keypoints_2; //keypoints for scene

Mat descriptors_object, descriptors_scene;
bool debug = true;
int realLifeDistance = 100; //real life distance from object
int realLifeWidth = 20; //real life size of object in cm
int calibrationVal = 605;
/* @function main */
int main(int argc, char* argv[])
{
	
	if ((int)argv[2] == 48) {
		debug == false;
	}
	else {
		debug == true;
	}

	Mat objectImg = imread("image1.jpg");
	//Mat sceneImg = imread("image2.jpg"); //testing purpose only
	Mat sceneImg = imread(argv[1]);

	if (!objectImg.data || !sceneImg.data)
	{
		std::cout << "Error reading images " << std::endl;
		return -1;
	}


	
	int minHessian = 400;
	Ptr<SURF> detector = SURF::create(minHessian);



	std::vector<KeyPoint> keypoints_object, keypoints_scene;
	Mat descriptors_object, descriptors_scene;
	detector->detectAndCompute(objectImg, Mat(), keypoints_object, descriptors_object);
	detector->detectAndCompute(sceneImg, Mat(), keypoints_scene, descriptors_scene);


	if (!keypoints_1.empty() || !keypoints_2.empty())
	{
		std::cout << "No feature points found! \n";
		return -1;
	}
		
	std::vector<std::vector<cv::DMatch> > matches; //watch space between '> >' without the space it won't run on linux
	cv::BFMatcher matcher;
	matcher.knnMatch(descriptors_object, descriptors_scene, matches, 3);  // Find two nearest matches
	
	vector<cv::DMatch> good_matches;
	for (int i = 0; i < matches.size(); ++i)
	{
		const float ratio = 0.8; 
		if (matches[i][0].distance < ratio * matches[i][1].distance)
		{
			good_matches.push_back(matches[i][0]);
		}
	}


	Mat img_matches;
	drawMatches(objectImg, keypoints_object, sceneImg, keypoints_scene,
		good_matches, img_matches, Scalar::all(-1), Scalar::all(-1),
		std::vector<char>(), DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);

	std::vector<Point2f> obj;
	std::vector<Point2f> scene;
	for (size_t i = 0; i < good_matches.size(); i++)
	{
		obj.push_back(keypoints_object[good_matches[i].queryIdx].pt);
		scene.push_back(keypoints_scene[good_matches[i].trainIdx].pt);
	}
	Mat H = findHomography(obj, scene, RANSAC);

	std::vector<Point2f> obj_corners(4);
	obj_corners[0] = cvPoint(0, 0); 
	obj_corners[1] = cvPoint(objectImg.cols, 0);
	obj_corners[2] = cvPoint(objectImg.cols, objectImg.rows);
	obj_corners[3] = cvPoint(0, objectImg.rows);
	std::vector<Point2f> scene_corners(4);
	perspectiveTransform(obj_corners, scene_corners, H); //convert to the corners of the object found in the scene

	Point leftTop = scene_corners[0] + Point2f(objectImg.cols, 0);
	Point rightTop = scene_corners[1] + Point2f(objectImg.cols, 0);
	Point rightBottom = scene_corners[2] + Point2f(objectImg.cols, 0);
	Point leftBottom = scene_corners[3] + Point2f(objectImg.cols, 0);

	line(img_matches, leftTop, rightTop, Scalar(0, 255, 0), 4);
	line(img_matches, rightTop, rightBottom, Scalar(0, 255, 0), 4);
	line(img_matches, rightBottom, leftBottom, Scalar(0, 255, 0), 4);
	line(img_matches, leftBottom, leftTop, Scalar(0, 255, 0), 4);
	int avgX1 = ceil((leftTop.x + leftBottom.x)/2);
	int avgX2 = ceil((rightTop.x + rightBottom.x)/2);
	int avgY1 = ceil((leftTop.y + leftBottom.y)/2);
	int avgY2 = ceil((rightTop.y + rightBottom.y)/2);
	Point newAvg1 = Point(avgX1, avgY1);
	Point newAvg2 = Point(avgX2, avgY2);

	float sizeOnScreen = abs(newAvg1.x - newAvg2.x);
	
	
	float focalLenght = (sizeOnScreen  * realLifeDistance) / realLifeWidth; // becomes new value for calibrationval on new images
	int afstand = ceil((realLifeWidth * calibrationVal) / sizeOnScreen);
	std::cout << "Calibratie : " << focalLenght << std::endl;
	std::cout << "afstand : " << afstand << "cm\n";
	int rotatie = 0;
	int xVal = (leftTop.x + rightTop.x + rightBottom.x + leftBottom.x) / 4;
	int yVal = (leftTop.y + rightTop.y + rightBottom.y + leftBottom.y) / 4;
	circle(img_matches, newAvg1, 5, Scalar(0, 255, 0), 5);
	circle(img_matches, newAvg2, 5, Scalar(0, 255, 0), 5);
	circle(img_matches, Point(xVal, yVal), 5, Scalar(0, 0, 255), 4);
	line(img_matches, Point(xVal , sceneImg.rows), Point(xVal, 0), Scalar(255, 0, 0), 1);
	line(img_matches, Point(objectImg.cols, yVal), Point(sceneImg.cols+ objectImg.cols, yVal), Scalar(255, 0, 0), 1);

	if (debug)imshow("Good Matches & Object detection", img_matches);

	std::cout << "Write to file \n";
	ofstream dataFile;
	dataFile.open("data.txt", ios::out | ios::trunc);
	dataFile << afstand << "," << rotatie << "," << xVal << "," << yVal;
	dataFile.close();
	std::cout << "Done writing! \n";
	if (debug)waitKey(0);
	return 0;
}
