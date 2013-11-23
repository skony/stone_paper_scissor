import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	img1 = cv2.imread('lapa.jpg')
	img2 = cv2.imread('TANK.jpg')
	img3 = cv2.imread('TANK.jpg')
	img4 = cv2.imread('TANK.jpg')

	gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	gray3 = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
	gray4 = cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
	blur1 = cv2.GaussianBlur(gray1,(5,5),0)
	blur2 = cv2.GaussianBlur(gray2,(5,5),0)
	blur3 = cv2.GaussianBlur(gray3,(5,5),0)
	blur4 = cv2.GaussianBlur(gray4,(5,5),0)
	fig = plt.figure()
	#fig.set_size_inches(10, 10)
	ax = plt.Axes(fig, [0., 0.5, 0.5, 0.5])
	ax.set_axis_off()
	fig.add_axes(ax)

	thresh = 200
	
	edges1 = cv2.Canny(blur1,thresh,thresh*2)
	edges2 = cv2.Canny(blur2,thresh,thresh*2)
	edges3 = cv2.Canny(blur3,thresh,thresh*2)
	edges4 = cv2.Canny(blur4,thresh,thresh*2)
	drawing1 = np.zeros(img1.shape,np.uint8) # Image to draw the contours
	drawing2 = np.zeros(img2.shape,np.uint8)
	drawing3 = np.zeros(img3.shape,np.uint8) # Image to draw the contours
	drawing4 = np.zeros(img4.shape,np.uint8)
	contours1,hierarchy1 = cv2.findContours(edges1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours2,hierarchy2 = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours3,hierarchy3 = cv2.findContours(edges3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours4,hierarchy4 = cv2.findContours(edges4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours1:
		cv2.drawContours(drawing1,[cnt],0,(255,255,255),2)
		plt.imshow(drawing1, aspect='normal')
	ax = plt.Axes(fig, [0., 0., 0.5, 0.5])
	fig.add_axes(ax)
	for cnt in contours2:
		cv2.drawContours(drawing2,[cnt],0,(255,255,255),2)
		plt.imshow(drawing2, aspect='normal')
	ax = plt.Axes(fig, [0.5, 0., 0.5, 0.5])
	fig.add_axes(ax)
	for cnt in contours3:
		cv2.drawContours(drawing3,[cnt],0,(255,255,255),2)
		plt.imshow(drawing3, aspect='normal')
	ax = plt.Axes(fig, [0.5, 0.5, 0.5, 0.5])
	fig.add_axes(ax)
	for cnt in contours4:
		cv2.drawContours(drawing4,[cnt],0,(255,255,255),2)
		plt.imshow(drawing4, aspect='normal')
	plt.savefig('planes.jpg',  dpi = 80)

	if cv2.waitKey(0) == 27:
		cv2.destroyAllWindows()


# 10 09 11 07 200
