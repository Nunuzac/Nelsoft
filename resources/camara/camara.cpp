#include <iostream>
#include </usr/include/opencv2/core/core.hpp>
#include </usr/include/opencv2/highgui/highgui.hpp>
#include <string>
#include <sstream>
#include <unistd.h>

using namespace std;
using namespace cv;

VideoCapture cap;
Mat img;
char key = 0;

int main(int argc, char *argv[]) {

    cap.open(0);
    if (!cap.isOpened())
        return -1;

    while (key!=27 && cap.grab()) {
        cap.retrieve(img);
        cv::imshow("Camara", img);
        cv::moveWindow("Camara", 550, 100);
        key = cv::waitKey(20);
    }
}

