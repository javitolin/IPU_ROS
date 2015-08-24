/*
 * FirstTaskGate.cpp
 *
 *  Created on: Jan 11, 2015
 *      Author: jdorfsman
 */

#include "../SecondTask/SecondTaskCollision.h"


/// Global variables
Mat pic_src,pic_end;
Rect boundRectC;
//RNG rngC(12345);
//config file vars START HERE:
//int thresh = 250;
int minArea = 500;
int threshold1 = 17;
int threshold2 = 35;
//int bb_max_thresh = 255;

//config file vars END HERE.
int collision_found = 0;
string src_picName = "";

void SecondTaskCollision::Run(Mat mat){
	collision_found = 0;
	//Mat threshold_output;
	cvtColor(mat,pic_end, CV_RGB2GRAY);
	blur(pic_end, pic_end, Size(1.5,1.5));
	Canny( pic_end, pic_end, threshold1, threshold2,3 );
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;

	 findContours( pic_end, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

		//vector<vector<Point> > contours_poly( contours.size() );
	 	 vector<Point> allContours;
	 	 for (uint i=0 ; i<contours.size() ; i++){
	 	allContours.insert(allContours.end(),contours[i].begin(),contours[i].end());

	 	 }

		Scalar color = Scalar(255,255,255 );
		 Mat drawing = Mat::zeros( pic_end.size(), CV_8UC3 );
			if(contours.size()>0){
		 	 boundRectC = boundingRect( Mat(allContours) );
		 	 if(boundRectC.area()>minArea){
				collision_found = 1;
				rectangle( pic_end, boundRectC.tl(), boundRectC.br(), Scalar(255, 0, 0), 1, 8, 0 );
		 	 }
			}

}
void SecondTaskCollision::Load(map<string, string>& params){
	ParamUtils::setParam(params, "minArea", minArea);
	ParamUtils::setParam(params, "threshold1", threshold1);
	ParamUtils::setParam(params, "threshold2", threshold2);
}
void SecondTaskCollision::ToMesseges(vector<MissionControlMessage>& res){

	//send back to ros part:

		if(collision_found){
			MissionControlMessage msg;
			msg.MissionCode = 2;
			//need to return:
			Point topLeft =boundRectC.tl();
			msg.bounds.push_back(std::make_pair(topLeft.x,topLeft.y));
			Point bottomRight = boundRectC.br();
			msg.bounds.push_back(std::make_pair(bottomRight.x,bottomRight.y));
			Point topRight = Point(bottomRight.x, topLeft.y);
			msg.bounds.push_back(std::make_pair(topRight.x,topRight.y));
			Point bottomLeft = Point(topLeft.x, bottomRight.y);
			msg.bounds.push_back(std::make_pair(bottomLeft.x,bottomLeft.y));
			res.push_back(msg);
		}
}
void SecondTaskCollision::ClearProcessData(){
	//TODO
}
void SecondTaskCollision::SetDefaultParams(){
	int minArea = 500;
	int threshold1 = 17;
	int threshold2 = 35;
}
void SecondTaskCollision::Draw(Mat& draw){
	pic_end.copyTo(draw);
}
void SecondTaskCollision::InitProcessData(){
	SetDefaultParams();
}
void SecondTaskCollision::InitResult(){

}
