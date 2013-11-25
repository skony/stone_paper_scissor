import cv2
import numpy as np

def main():
	
	img = cv2.imread('Webcam/2013-11-23-144142.jpg')
	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	drawing = np.zeros(img.shape,np.uint8)
	for cnt in contours:
		color = np.random.randint(0,255,(3)).tolist()
		cv2.drawContours(drawing,[cnt],0,color,2)	
		cv2.imshow('output',drawing)


if __name__ == '__main__':
	main()
