
/****
比较这两个人脸的相似度，这里用到了facedetect的功能，还有图像转换，图像剪切，以及直方图的比较。具体流程是:

1。分别用facedetect功能将两张图片中的人脸检测出来

2。将人脸部分的图片剪切出来，存到两张只有人脸的图片里。

3。将这两张人脸图片转换成单通道的图像

4。使用直方图比较这两张单通道的人脸图像，得出相似度。

这里对图的要求还是比较高的，光线和姿势不能有差别，脸的垂直或者左右角度偏差就会影响比较，但和两张图片的大小关系不大，本人觉得较适合于证件照的对比。

下面是代码，其中haarcascade_frontalface_alt.xml是opencv里facedetect例子用的样本。 比较的是srcImage和targetImage对应的文件.

*****/

#include "opencv/cv.hpp"  
#include "opencv2/objdetect/objdetect.hpp"  
#include "opencv2/highgui/highgui.hpp"  
#include "opencv2/imgproc/imgproc.hpp"  
  
#include <iostream>  
#include <stdio.h>  
  
using namespace std;  
using namespace cv;  
  
String cascadeName = "haarcascade_frontalface_alt.xml";  
  
IplImage* cutImage(IplImage* src, CvRect rect) 
{  
    cvSetImageROI(src, rect);  
    IplImage* dst = cvCreateImage(cvSize(rect.width, rect.height),  
            src->depth,  
            src->nChannels);  
  
    cvCopy(src,dst,0);  
    cvResetImageROI(src);  
    return dst;  
}  
  
IplImage* detect( Mat& img, CascadeClassifier& cascade, double scale)  
{  
    int i = 0;  
    double t = 0;  
    vector<Rect> faces;  
    Mat gray, smallImg( cvRound (img.rows/scale), cvRound(img.cols/scale), CV_8UC1 );  
  
    cvtColor( img, gray, CV_BGR2GRAY );  
    resize( gray, smallImg, smallImg.size(), 0, 0, INTER_LINEAR );  
    equalizeHist( smallImg, smallImg );  
  
    t = (double)cvGetTickCount();  
    cascade.detectMultiScale( smallImg, faces,  
        1.3, 2, CV_HAAR_SCALE_IMAGE,  
        Size(30, 30) );  
    t = (double)cvGetTickCount() - t;  
    printf( "detection time = %g ms\n", t/((double)cvGetTickFrequency()*1000.) );  
    IplImage* src = &(IplImage(img));

    for( vector<Rect>::const_iterator r = faces.begin(); r != faces.end(); r++, i++ )  
    {  
        IplImage* temp = cutImage(src,cvRect(r->x, r->y, r->width, r->height));  
        return temp;  
    }  
  
    return NULL;  
}  
//画直方图用  
int HistogramBins = 256;  
float HistogramRange1[2]={0,255};  
float *HistogramRange[1]={&HistogramRange1[0]};  
int CompareHist(IplImage* image1, IplImage* image2)  
{  
    IplImage* srcImage;  
    IplImage* targetImage;  
    if (image1->nChannels != 1) {  
        srcImage = cvCreateImage(cvSize(image1->width, image1->height), image1->depth, 1);  
        cvCvtColor(image1, srcImage, CV_BGR2GRAY);  
    } else {  
        srcImage = image1;  
    }  
  
    if (image2->nChannels != 1) {  
        targetImage = cvCreateImage(cvSize(image2->width, image2->height), srcImage->depth, 1);  
        cvCvtColor(image2, targetImage, CV_BGR2GRAY);  
    } else {  
        targetImage = image2;  
    }  
  
    CvHistogram *Histogram1 = cvCreateHist(1, &HistogramBins, CV_HIST_ARRAY,HistogramRange);  
    CvHistogram *Histogram2 = cvCreateHist(1, &HistogramBins, CV_HIST_ARRAY,HistogramRange);  
  
    cvCalcHist(&srcImage, Histogram1);  
    cvCalcHist(&targetImage, Histogram2);  
  
    cvNormalizeHist(Histogram1, 1);  
    cvNormalizeHist(Histogram2, 1);  
  
    // CV_COMP_CHISQR,CV_COMP_BHATTACHARYYA这两种都可以用来做直方图的比较，值越小，说明图形越相似  
    printf("CV_COMP_CHISQR : %.4f\n", cvCompareHist(Histogram1, Histogram2, CV_COMP_CHISQR));  
    printf("CV_COMP_BHATTACHARYYA : %.4f\n", cvCompareHist(Histogram1, Histogram2, CV_COMP_BHATTACHARYYA));  
  
  
    // CV_COMP_CORREL, CV_COMP_INTERSECT这两种直方图的比较，值越大，说明图形越相似  
    printf("CV_COMP_CORREL : %.4f\n", cvCompareHist(Histogram1, Histogram2, CV_COMP_CORREL));  
    printf("CV_COMP_INTERSECT : %.4f\n", cvCompareHist(Histogram1, Histogram2, CV_COMP_INTERSECT));  
  
    cvReleaseHist(&Histogram1);  
    cvReleaseHist(&Histogram2);  
    if (image1->nChannels != 1) {  
        cvReleaseImage(&srcImage);  
    }  
    if (image2->nChannels != 1) {  
        cvReleaseImage(&targetImage);  
    }  
    return 0;  
}  
String srcImage = "src.jpg";  
String targetImage = "dst.jpg";  
int main(int argc, char* argv[])  
{  
    CascadeClassifier cascade;  
    namedWindow("image1");  
    namedWindow("image2");  
    if( !cascade.load( cascadeName ) )  
    {  
	printf("[%s:%d]load %s error\n",__FILE__,__LINE__,cascadeName);
        return -1;  
    }  
  
    Mat srcImg, targetImg;  
    IplImage* faceImage1;  
    IplImage* faceImage2;  
    srcImg = imread(srcImage);  
    targetImg = imread(targetImage);  
    faceImage1 = detect(srcImg, cascade, 1);  
    if (faceImage1 == NULL) {  
	printf("[%s:%d] load srcImg error\n",__FILE__,__LINE__);
        return -1;  
    }  
    faceImage2 = detect(targetImg, cascade, 1);  
    if (faceImage2 == NULL) {  
	printf("[%s:%d] load dstImg error\n",__FILE__,__LINE__);
        return -1;  
    }  
    imshow("image1", Mat(faceImage1));  
    imshow("image2", Mat(faceImage2));  
  
    CompareHist(faceImage1, faceImage2);  
    cvWaitKey(0);  
    cvReleaseImage(&faceImage1);  
    cvReleaseImage(&faceImage2);  
    return 0;  
}  
