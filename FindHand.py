import cv2
import cv
import numpy as np
import sys

if __name__ == '__main__':
	bins = 25

	#read image & transform to hsv
	img = cv2.imread( "img.jpg" )
	hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
	
	#use only hue value
	hue = np.zeros( hsv.shape, np.uint8 ) #not sure if correct
	ch = [0, 0]
	cv2.mixChannels(hsv, hue, ch)

	#Create Trackbar to enter the number of bins
	window_image = "Source image"
	cv2.namedWindow( window_image, cv2.CV_WINDOW_AUTOSIZE )
	
		
