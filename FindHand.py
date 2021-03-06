import cv2
import cv
import numpy as np
import sys

def Hist_and_Backproj( arg1, arg2 ):
	
	histSize = max( bins, 2 )
	hue_range = [0, 180]
	#ranges = hue_range(hue, 0,

	#Get the Histogram and normalize it and apply backprojection
	hist = cv2.calcHist([hue], [0, 1], None, [180, 256], [0, 180, 0, 256])
	cv2.normalize( hist, hist, 0, 255, cv2.NORM_MINMAX )
	dst = cv2.calcBackProject([hue],[0,1],hist,[0,180,0,256],1)

	cv2.imshow("Backproj", dst) 
	
	
	return 0
	
if __name__ == '__main__':
	bins = 25
	
	img = cv2.imread( "hand2.jpg" )
	hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )

	#read image & transform to hsv
	target = cv2.imread( "img.jpg" )
	hsvt = cv2.cvtColor( target, cv2.COLOR_BGR2HSV )

	M = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
	I = cv2.calcHist([hsvt],[0, 1], None, [180, 256], [0, 180, 0, 256] )
	R = M/(I+1)

	h,s,v = cv2.split(hsvt)
	B = R[h.ravel(),s.ravel()]
	B = np.minimum(B,1)
	B = B.reshape(hsvt.shape[:2])

	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	cv2.filter2D(B,-1,disc,B)
	B = np.uint8(B)
	cv2.normalize(B,B,0,255,cv2.NORM_MINMAX)

	ret,thresh = cv2.threshold(B,50,255,0)
	#thresh = cv2.merge((thresh,thresh,thresh))
	#res = cv2.bitwise_and(target,thresh)

	#res = np.vstack((target,thresh,res))
	cv2.imshow("sru", B)
	
	#use only hue value
	#hue = np.empty(hsv.shape, np.uint8)
	#ch = [0, 0]
	#cv2.mixChannels(hsv, hue, ch)

	#Create Trackbar to enter the number of bins
	#window_image = "Source image"
	#cv2.namedWindow( window_image, cv2.CV_WINDOW_AUTOSIZE )
	#cv.CreateTrackbar( "* Hue  bins: ", "window_image", bins, 180,  Hist_and_Backproj )
	#Hist_and_Backproj(0, 0)
	
	#Show the image
	#cv2.imshow( window_image, img )

	#Wait until user exits the program
	cv2.waitKey(0)
	
