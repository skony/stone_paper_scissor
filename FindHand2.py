import cv2
import numpy as np

if __name__ == '__main__': 
	roi = cv2.imread('hope.jpg')
	hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
	 
	target = cv2.imread('img3.jpg')
	hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

	#mix Channels
	hue = np.empty(hsv.shape, np.float32)
	cv2.mixChannels(hsv.astype('float32'),hue, [0, 0])	
	 
	# calculating object histogram
	roihist = cv2.calcHist([hue],[0, 0], None, [180, 256], [0, 180, 0, 256] )
	 
	# normalize histogram and apply backprojection
	cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
	dst = cv2.calcBackProject([hsvt],[0,0],roihist,[0,180,0,256],1)

	#a minsziftem
	term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
	ret, track_window = cv2.meanShift(dst, track_window, term_crit)

	# Draw it on image
	x,y,w,h = track_window
	img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	cv2.imshow('img2',img2)
	 
	# Now convolute with circular disc
	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	cv2.filter2D(dst,-1,disc,dst)
	 
	# threshold and binary AND
	#ret,thresh = cv2.threshold(dst,0,255,0)
	thresh = cv2.merge((thresh,thresh,thresh))
	res = cv2.bitwise_and(target,thresh)
	 
	res = np.vstack((target,thresh,res))
	cv2.imwrite("res.jpg",res)
