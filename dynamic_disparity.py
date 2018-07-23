import cv2
import numpy as np

left_img = cv2.imread('view1.png', 0)  #read it as a grayscale image
right_img = cv2.imread('view5.png', 0)

numcols= left_img.shape[1]
numrows=left_img.shape[0]
OcclusionCost = 20 #(You can adjust this, depending on how much threshold you want to give for noise)
s= (numcols,numcols)


DMatrix1= np.zeros((numrows,numcols))
DMatrix2= np.zeros((numrows,numcols))
CostMatrix = np.zeros(s)

for i in range (1, numcols):
      CostMatrix[i,0] = i*OcclusionCost
      CostMatrix[0,i] = i*OcclusionCost

# Now, its time to populate the whole Cost Matrix and DirectionMatrix

# Use the pseudocode from "A Maximum likelihood Stereo Algorithm" paper given as reference

for row in range(1,numrows):
	temp = np.zeros(s)

	for i in range (1, numcols):
	      for j in range (1, numcols):
			min1= CostMatrix[i-1,j-1] + np.abs(left_img[row,i]-right_img[row,j])
			min2= CostMatrix[i-1,j] + OcclusionCost
			min3= CostMatrix[i,j-1] + OcclusionCost
			cmin= min(min1, min2, min3)
			if (min1==cmin): temp[i,j]=1
			if (min2==cmin): temp[i,j]=2
			if (min3==cmin): temp[i,j]=3
	p=numcols-1
	q=numcols-1

	while (p!=0 and q!= 0):

		if (temp[p][q] == 1):
	                p -= 1; q -= 1;
	                DMatrix1[row][p] = np.absolute(p-q)
	                DMatrix2[row][q] = np.absolute(p-q)
		elif (temp[p][q] == 2):
	                p -= 1
	                DMatrix1[row][p] = np.absolute(p-q)
		elif (temp[p][q] == 3):
	                q -= 1
	                DMatrix2[row][q] = np.absolute(p-q)

#print dmap1
print "Disparity Matrix 1 using Dynamic Programming is: ", DMatrix1
print "Disparity Matrix 2 using Dynamic Programming is: ", DMatrix2
