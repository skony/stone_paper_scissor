#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
import numpy
import cv2
#include <iostream>

#using namespace cv;
#using namespace std;

#/// Global Variables
#Mat src; Mat hsv; Mat hue;
#hsv = numpy.array([])
hue = numpy.array([])
bins = 25

def Hist_and_Backproj():#int, void):
#  MatND hist;
  histSize = max( bins, 2 )
  hue_range = [0, 180]
  ranges = hue_range

#  /// Get the Histogram and normalize it
  hist = cv2.calcHist([hue], [0], None, [180], [0, 180]) #histSize, hue_range)
  cv2.normalize( hist, hist, 0, 255, NORM_MINMAX, -1, Mat() )

  #/// Get Backprojection
  #MatND backproj
  cv2.calcBackProject( hue, 1, 0, hist, backproj, ranges, 1, true )

  #/// Draw the backproj
  imshow( "BackProj", backproj )

  #/// Draw the histogram
  w = 400
  h = 400
  bin_w = cvRound( w / histSize )
  histImg = numpy.zeros( w, h, CV_8UC3 )

  for i in range (0, bins):
    rectangle( histImg, Point( i*bin_w, h ), Point( (i+1)*bin_w, h - cvRound( hist.at<float>(i)*h/255.0 ) ), Scalar( 0, 0, 255 ), -1 )

  imshow( "Histogram", histImg )

#/// Function Headers
#void Hist_and_Backproj(int, void* );

#/** @function main */
#int main( int argc, char** argv )
#{
#  /// Read the image
def main():
  src = cv2.imread("Webcam/2013-11-23-144314.jpg")
#  /// Transform it to HSV
  hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

 # /// Use only the Hue value

#hue.cv2.create( hsv.size(), hsv, hsv.depth() )
  ch = { 0, 0 }
  #hue = numpy.array([])
#cv2.mixChannels( hsv, hue, ch)

#  /// Create Trackbar to enter the number of bins
  window_image = "Source image"
  cv2.namedWindow( window_image, cv2.CV_WINDOW_AUTOSIZE )
  cv2.createTrackbar("* Hue  bins: ", window_image, bins, 180, Hist_and_Backproj )
  Hist_and_Backproj() #(0, 0)

#  /// Show the image
  imshow( window_image, src )

#  /// Wait until user exits the program
  waitKey(0)

if __name__ == '__main__':
  main()

#/**
# * @function Hist_and_Backproj
# * @brief Callback to Trackbar
# */

