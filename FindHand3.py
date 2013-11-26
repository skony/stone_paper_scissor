import cv2
import numpy as np

if __name__ == '__main__':
	
 
	roi = cv2.imread('hope.jpg')
	hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
	
	cam=cv2.VideoCapture(0)
	cam.open
	ret,frame = cam.read()
	
	# setup initial location of window
	r,h,c,w = 250,90,400,125  # simply hardcoded the values
	track_window = (c,r,w,h) 

	#mix Channels
	hue = np.empty(hsv.shape, np.float32)
	cv2.mixChannels(hsv.astype('float32'),hue, [0, 0])	
	 
	# calculating object histogram
	roihist = cv2.calcHist([hue],[0, 0], None, [180, 256], [0, 180, 0, 256] )
	 
	# normalize histogram and apply backprojection
	cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)

	#a minsziftem
	term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
	
	while(1):
		ret ,frame = cam.read()

		if ret == True:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			dst = cv2.calcBackProject([hsv],[0,0],roihist,[0,180,0,256],1)

			# apply meanshift to get the new location
			ret, track_window = cv2.meanShift(dst, track_window, term_crit)

 			# Draw it on image
 			x,y,w,h = track_window
			img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
			
			cv2.imshow('img2',frame)

			k = cv2.waitKey(60) & 0xff
			if k == 27:
				break
			else:
				cv2.imwrite(chr(k)+".jpg",img2)

		else:
			break

	cv2.destroyAllWindows()
	cam.release() 

	 