#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy as np
imcolor = cv.LoadImage('field3.jpg ')
image = cv.LoadImage('field3.jpg ',cv.CV_LOAD_IMAGE_GRAYSCALE)


img = cv2.imread('field3.jpg')
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
eig_image = cv.CreateImage(cv.GetSize(image),8,1)
temp_image= cv.CreateImage(cv.GetSize(image),8,1)
cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
cornerMap =cv.GoodFeaturesToTrack(image, eig_image, temp_image, 4, 0.04, 1, useHarris = True)
src = np.array([[114,56],[885,292],[0,292],[751,74]],np.float32)
print src
dst = np.array([[0,0],[image.width,image.height],[0,image.height],[image.width,0]],np.float32)
print dst
retval = cv2.getPerspectiveTransform(src,dst)
warp = cv2.warpPerspective(gray,retval,(image.width,image.height))
cv2.imshow('a_window', warp)
cv.ShowImage('image', image)
cv.WaitKey()