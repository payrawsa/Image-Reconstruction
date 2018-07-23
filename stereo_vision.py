import cv2
import numpy as np
import argparse

image_one = cv2.imread('view1.png', 0)  #read it as a grayscale image
image_two= cv2.imread('view5.png', 0)
disp1= cv2.imread('disp1.png',0)
disp2= cv2.imread('disp5.png',0)
parser = argparse.ArgumentParser()
parser.add_argument('integers', metavar='N', type=int, nargs=1, help='input window horizontal length')
args = parser.parse_args()
np.set_printoptions(threshold='nan')
window_size = args.integers[0]

#this will calculate the disparity for any two images and any window_size. Automatically looks through
def calculate_disparity(image_one, image_two):

	#pad_amt is how many values around the center value. So if pad_amt=1 it means look at 1 value around the center in all directions.
	pad_amt= (window_size-1)/2
	#pad the images with the pad_amt amount
	img1= cv2.copyMakeBorder(image_one,pad_amt,pad_amt,pad_amt,pad_amt,cv2.BORDER_CONSTANT,value=0)
	img2= cv2.copyMakeBorder(image_two,pad_amt,pad_amt,pad_amt,pad_amt,cv2.BORDER_CONSTANT,value=0)
	numcols= img1.shape[1]
	numrows=img1.shape[0]
	#create disparity matrix
	dist= np.zeros((image_one.shape[0],image_one.shape[1]))
	#populate disparity matrix
	for row in range (pad_amt, numrows-pad_amt):
		for img1_col in range (pad_amt, numcols-pad_amt):
			#select the pixel in the first image
			current_pixel=img1[row,img1_col]
			best = 10000000;
			temp1= np.array(img1[row-pad_amt:row+pad_amt, img1_col-pad_amt:img1_col+pad_amt],dtype=np.int16)
			y_value=0;
			for img2_col in range(pad_amt,numcols-pad_amt):

						temp2=np.array(img2[row-pad_amt:row+pad_amt, img2_col-pad_amt:img2_col+pad_amt],dtype=np.int16)
						distance=np.sum(np.absolute(temp1-temp2))
						if (best > distance):
							best=distance;
							y_value=img2_col;

			dist[row-pad_amt,img1_col-pad_amt]=img1_col-y_value
	return dist

def MSE(disp_calc, ground_truth,x,y):
	return np.sum((disp_calc-ground_truth)**2)/(x*y)

def consistency_check(one, two):

	for i in range (0,one.shape[0]):
		for j in range(0,one.shape[1]):
			disparity1_value=one[i][j]
			disparity2_value=two[i][j-disparity1]
			if disparity1 != disparity2:
				 one[i][j]=0
				 two[i][j-disparity1]=0
	print "The consistency check for disparity 1 is: ", one
	print "The consistency check for disparity 2 is: ", two

disparity1= calculate_disparity(image_one, image_two)
disparity2= calculate_disparity(image_two, image_one)

print "disparity for image one"
print disparity1

print "disparity for image two"
print disparity2

print "MSE value for disp1 is: ", MSE(disparity1, disp1, disparity1.shape[0],disparity1.shape[1])
print "MSE value for disp1 is: ", MSE(disparity2, disp2, disparity2.shape[0], disparity2.shape[1])

consistency_check(disparity1,disparity2)
