import numpy as np
import cv2

image_one = cv2.imread('view1.png');
image_two = cv2.imread('view5.png');
disp1 = cv2.imread('disp1.png',0);
disp2 = cv2.imread('disp5.png',0);
synth_view = np.zeros(image_one.shape,dtype = np.uint8)

for i in range(0, image_one.shape[0]):
    for j in range(0, image_one.shape[1]):
        disp_value=disp1[i][j]
        synth_view[i][j-disp_value/2] = image_one[i][j]


for i in range(0, image_one.shape[0]):
        j=0
        disp_value=disp2[i][j]
        while (j+disp_value/2 < image_one.shape[1]):
            if (np.sum(synth_view[i][j+disp_value/2]) == 0):
                synth_view[i][j+disp_value/2] = image_two[i][j]
            j++
        else: break;
cv2.imshow("image",synth_view)
cv2.waitKey(0)
