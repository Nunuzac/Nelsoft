#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <string>
#include <unistd.h>

using namespace std;
using namespace cv;

int main(int argc, char *argv[]) {

    if (argc != 2)
        return -1;

    String file_name = argv[1];

    Mat img;
    VideoCapture cap;
    cap.open(0);

    vector<int> compression_params;
    compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
    compression_params.push_back(100);

    cap.set(CV_CAP_PROP_FRAME_WIDTH, 1920);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 1080);

    cap >> img;
    imwrite(file_name + ".jpg", img, compression_params);
    return 0;
}

