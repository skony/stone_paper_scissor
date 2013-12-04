import cv2
import numpy as np
from contours import contour_thingy, winner 

if __name__ == '__main__':
	
	s1, s2 = 0, 0
	cam=cv2.VideoCapture(0)
	cam.open
	ret,frame = cam.read()
	tick = 10
	T, t1, t2 = 0, 0, 0
	r,h,c,w = 240,240,0,240
	track_window = (c,r,w,h)
	y2,h2,x2,w2 = 240,240,400,240

	while(1):
		ret ,frame = cam.read()

		if ret == True:
 			x,y,w,h = track_window

			if T > 1 and tick==0:
				handL = frame[y:y+h,x:x+w]
				handR = frame[y2:y2+h2,x2:x2+w2]
				#cv2.imwrite("handL.jpg",handL)
				#cv2.imwrite("handR.jpg",handR)
				p1 = contour_thingy(handL)
				p2 = contour_thingy(handR)
				s1, s2 = winner(p1, s1, p2, s2)
				print s1, s2
				tick = 10
				T = 0
			elif T > 1:
				t1 = cv2.getTickCount()
				cv2.putText(frame, str(tick), (280,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255) )
				tick = tick-1
				T = 0

			img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
			img3 = cv2.rectangle(frame, (x2,y2), (x2+w2,y2+h2), (0,255),2)
			cv2.putText(frame, str(s1), (10,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255) )
			cv2.putText(frame, str(s1), (480,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255) )
			cv2.imshow('img2', frame)
			k = cv2.waitKey(60) & 0xff

			if k == 27:
				break
			else:
				cv2.imwrite(chr(k)+".jpg",img3)

		else:
			break
		t2 = cv2.getTickCount()
		T += (t2 - t1)/cv2.getTickFrequency()

	cv2.destroyAllWindows()
	cam.release() 

	 
