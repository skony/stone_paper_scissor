import cv2
import numpy as np

class Contour:
	''' Provides detailed parameter informations about a contour

		Create a Contour instant as follows: c = Contour(src_img, contour)
				where src_img should be grayscale image.

		Attributes:

		c.area -- gives the area of the region
		c.perimeter -- gives the perimeter of the region
		c.moments -- gives all values of moments as a dict
		c.centroid -- gives the centroid of the region as a tuple (x,y)
		c.bounding_box -- gives the bounding box parameters as a tuple => (x,y,width,height)
		c.bx,c.by,c.bw,c.bh -- corresponds to (x,y,width,height) of the bounding box
		c.aspect_ratio -- aspect ratio is the ratio of width to height
		c.equi_diameter -- equivalent diameter of the circle with same as area as that of region
		c.extent -- extent = contour area/bounding box area
		c.convex_hull -- gives the convex hull of the region
		c.convex_area -- gives the area of the convex hull
		c.solidity -- solidity = contour area / convex hull area
		c.center -- gives the center of the ellipse
		c.majoraxis_length -- gives the length of major axis
		c.minoraxis_length -- gives the length of minor axis
		c.orientation -- gives the orientation of ellipse
		c.eccentricity -- gives the eccentricity of ellipse
		c.filledImage -- returns the image where region is white and others are black
		c.filledArea -- finds the number of white pixels in filledImage
		c.convexImage -- returns the image where convex hull region is white and others are black
		c.pixelList -- array of indices of on-pixels in filledImage
		c.maxval -- corresponds to max intensity in the contour region
		c.maxloc -- location of max.intensity pixel location
		c.minval -- corresponds to min intensity in the contour region
		c.minloc -- corresponds to min.intensity pixel location
		c.meanval -- finds mean intensity in the contour region
		c.leftmost -- leftmost point of the contour
		c.rightmost -- rightmost point of the contour
		c.topmost -- topmost point of the contour
		c.bottommost -- bottommost point of the contour
		c.distance_image((x,y)) -- return the distance (x,y) from the contour.
		c.distance_image() -- return the distance image where distance to all points on image are calculated
		'''
	def __init__(self,img,cnt):
		self.img = img
		self.cnt = cnt
		self.size = len(cnt)

		# MAIN PARAMETERS

		#Contour.area - Area bounded by the contour region'''
		self.area = cv2.contourArea(self.cnt)

		# contour perimeter
		self.perimeter = cv2.arcLength(cnt,True)

		# centroid
		self.moments = cv2.moments(cnt)
		if self.moments['m00'] != 0.0:
			self.cx = self.moments['m10']/self.moments['m00']
			self.cy = self.moments['m01']/self.moments['m00']
			self.centroid = (self.cx,self.cy)
		else:
			self.centroid = "Region has zero area"

		# bounding box
		self.bounding_box=cv2.boundingRect(cnt)
		(self.bx,self.by,self.bw,self.bh) = self.bounding_box

		# aspect ratio
		self.aspect_ratio = self.bw/float(self.bh)

		# equivalent diameter
		self.equi_diameter = np.sqrt(4*self.area/np.pi)

		# extent = contour area/boundingrect area
		self.extent = self.area/(self.bw*self.bh)


		### CONVEX HULL ###

		# convex hull
		self.convex_hull = cv2.convexHull(cnt)

		# convex hull area
		self.convex_area = cv2.contourArea(self.convex_hull)

		# solidity = contour area / convex hull area
		self.solidity = self.area/float(self.convex_area)


		### ELLIPSE  ###

		self.ellipse = cv2.fitEllipse(cnt)

		# center, axis_length and orientation of ellipse
		(self.center,self.axes,self.orientation) = self.ellipse

		# length of MAJOR and minor axis
		self.majoraxis_length = max(self.axes)
		self.minoraxis_length = min(self.axes)

		# eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
		self.eccentricity = np.sqrt(1-(self.minoraxis_length/self.majoraxis_length)**2)


		### CONTOUR APPROXIMATION ###

		self.approx = cv2.approxPolyDP(cnt,0.02*self.perimeter,True)


		### EXTRA IMAGES ###

		# filled image :- binary image with contour region white and others black
		self.filledImage = np.zeros(self.img.shape[0:2],np.uint8)
		cv2.drawContours(self.filledImage,[self.cnt],0,255,-1)

		# area of filled image
		filledArea = cv2.countNonZero(self.filledImage)

		# pixelList - array of indices of contour region
		self.pixelList = np.transpose(np.nonzero(self.filledImage))

		# convex image :- binary image with convex hull region white and others black
		self.convexImage = np.zeros(self.img.shape[0:2],np.uint8)
		cv2.drawContours(self.convexImage,[self.convex_hull],0,255,-1)


		### PIXEL PARAMETERS
	  
		# mean value, minvalue, maxvalue
		self.minval,self.maxval,self.minloc,self.maxloc = cv2.minMaxLoc(self.img,mask = self.filledImage)
		self.meanval = cv2.mean(self.img,mask = self.filledImage)


		### EXTREME POINTS ###

		# Finds the leftmost, rightmost, topmost and bottommost points
		self.leftmost = tuple(self.cnt[self.cnt[:,:,0].argmin()][0])
		self.rightmost = tuple(self.cnt[self.cnt[:,:,0].argmax()][0])
		self.topmost = tuple(self.cnt[self.cnt[:,:,1].argmin()][0])
		self.bottommost = tuple(self.cnt[self.cnt[:,:,1].argmax()][0])
		self.extreme = (self.leftmost,self.rightmost,self.topmost,self.bottommost)

	### STONE PAPER SCISSORS CHECKER

	def sps_check(self):
		if (self.aspect_ratio < 1.7) and (self.eccentricity < 1.75):
			self.result = "stone"
			return self.result
		elif (self.solidity > 0.9):
			self.result = "paper"
			return self.result
		else:
			self.result = "scissors"
			return self.result 

	

#### DEMO ######
if __name__=='__main__':

	im = cv2.imread('test/3b.jpg')
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	#thresh = cv2.adaptiveThreshold(imgray,255, cv2.ADAPTIVE_THRESH_MEAN_C,1,11,2)
	thresh = 100	
	edges = cv2.Canny(imgray, thresh, thresh*3)
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im, contours,-1,(0,255,0),1)
	cv2.imshow('fotka', im)
	if cv2.waitKey(0) == 27:
		cv2.destroyAllWindows()
	#for cnt in contours:
	c = Contour(imgray, contours[0])
	print('ratio (w/h): ')
	print(c.aspect_ratio)
	
	print('circle diameter: ')
	print(c.equi_diameter)
	
	print('extent (con area/bounding box area): ')
	print(c.extent)
	
	print('solidity (con area/conver hull area): ')
	print(c.solidity)
	
	print('area/perimeter: ')
	print(c.area/c.perimeter)
	
	print('elipse eccentricities: ')
	print(c.eccentricity)
	print('ellipse majoraxis/el minor')
	print(c.majoraxis_length/c.minoraxis_length)
	print('result: ')
	print(c.sps_check())
	cv2.drawContours(im, c.approx,-1,(0,255,0),1)
	cv2.imshow('fotka', im)
	if cv2.waitKey(0) == 27:
		cv2.destroyAllWindows()
	
