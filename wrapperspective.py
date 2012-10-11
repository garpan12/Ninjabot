#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy as np
"""
cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
img=cv.LoadImage('testmap2.png', cv.CV_LOAD_IMAGE_COLOR) #Load the image
gray = cv.CreateImage((img.width,img.height), cv.IPL_DEPTH_8U, 1)

cv.CvtColor(img, gray ,cv.CV_BGR2GRAY)

mask = np.zeros((gray.width,gray.height),np.uint8)
#cv.getStructuringElement(kernel1 ,cv.MORPH_ELLIPSE,(11,11))

#close = cv.MorphologyEx(gray,cv.MORPH_CLOSE,kernel1)
#div = np.float32(gray)
res = np.uint8(gray)
#cv.CvtColor(res,res2, cv.CV_GRAY2BGR)
#storage = cv.GetMat(dst)

#thresh = cv.AdaptiveThreshold(storage,255,0,1,19,2)
mask = np.zeros((src.width,src.height),np.uint8)


contour,hier = cv.FindContours(dst, cv.CreateMemStorage() ,cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)


max_area = 0
best_cnt = None
for cnt in contour:
    area = cv.ContourArea(cnt)
    if area > 1000:
        if area > max_area:
            max_area = area
            best_cnt = cnt


cv.DrawContours(mask,[best_cnt],0,255,-1)
cv.DrawContours(mask,[best_cnt],0,0,2)

res = cv.Bitwise_and(dst,mask)

#cv.WarpPerspective(src, dst, storage)
cv.ShowImage('a_window', res)
"""
#img = cv2.imread('testmap2.png')
#img = cv2.GaussianBlur(img,(5,5),0)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#cornermap = cv.CreateMat(gray.height, gray.width, cv.CV_32FC1)


"""
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
div = np.float32(gray)/(close)
res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
res2 = cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)


thresh = cv2.adaptiveThreshold(res,255,0,1,19,2)
contour,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
best_cnt = None
for cnt in contour:
    area = cv2.contourArea(cnt)
    if area > 1000:
        if area > max_area:
            max_area = area
            best_cnt = cnt

cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)

res = cv2.bitwise_and(res,mask)
"""
#output = np.zeros((450,450,3),np.float32)

#src = bm[ri:ri+2, ci:ci+2 , :].reshape((4,2))
#dst = np.array( [ [ci*50,ri*50],[(ci+1)*50-1,ri*50],[ci*50,(ri+1)*50-1],[(ci+1)*50-1,(ri+1)*50-1] ], np.float32)
"""

img = cv2.imread('testmap2.png')
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cornermap = np.zeros((gray.shape),np.uint8)
cornermap = cv2.cornerHarris(gray,3,1,1)

src = np.array([[25,25],[100,100],[70,120],[120,70]],np.float32)
dst = np.array([[0,0],[450,450],[0,450],[450,0]],np.float32)

retval = cv2.getPerspectiveTransform(src,dst)
warp = cv2.warpPerspective(src,retval,(450,450))

h, w = img.shape[:2]

for y in range(0, h):
 for x in range(0, w):
  harris = cv2.et2D(cornermap, y, x) # get the x,y value
  # check the corner detector response
  if harris[0] > 10e-06:
   # draw a small circle on the original image
   cv.Circle(imcolor,(x,y),2,cv.RGB(155, 0, 25))
print cornermap[:2]


cv2.imshow('a_window2', img)

cv2.imshow('a_window', warp)





#cv.ShowImage('a_window', src)

#cv.ShowImage('a_window', warp)

while True:
    if cv.WaitKey(10) == 27:
        break
        """
imcolor = cv.LoadImage('field3.jpg ')
image = cv.LoadImage('field3.jpg ',cv.CV_LOAD_IMAGE_GRAYSCALE)


img = cv2.imread('field3.jpg')
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cornermap = np.zeros((image.height,image.width),np.uint8)
#cv.Canny(image, image, 5, 70, 3)
#gray = cv.CreateImage(cv.GetSize(image),8,1)
eig_image = cv.CreateImage(cv.GetSize(image),8,1)
temp_image= cv.CreateImage(cv.GetSize(image),8,1)
#cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
#cv.Smooth(image, image, cv.CV_GAUSSIAN, 7, 7)
cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
# OpenCV corner detection
#cv.CornerHarris(image,cornerMap,3)
#cornermap = cv2.goodFeaturesToTrack(gray, 4,0.04,1)
cornerMap =cv.GoodFeaturesToTrack(image, eig_image, temp_image, 4, 0.04, 1, useHarris = True)
#s= []

#src = np.array([[257,95],[692,320],[162,320],[618,86]],np.float32)
src = np.array([[114,56],[885,292],[0,292],[751,74]],np.float32)
print src
dst = np.array([[0,0],[image.width,image.height],[0,image.height],[image.width,0]],np.float32)
print dst
retval = cv2.getPerspectiveTransform(src,dst)
warp = cv2.warpPerspective(gray,retval,(image.width,image.height))


"""
for y in range(0, image.height):
 for x in range(0, image.width):
  harris = cv.Get2D(cornerMap, y, x) # get the x,y value
  # check the corner detector response
  #if harris[0] > 10e-10:
   # draw a small circle on the original image
  cv.Circle(image,(x,y),5,cv.RGB(155, 0, 25))
   #s +=[x,y]
for points in cornerMap:
    (x,y) = points
    cv.Circle(image,(int(x),int(y)),5,cv.RGB(155, 0, 25))"""

#print cornermap
cv2.imshow('a_window', warp)

#cv.NamedWindow('Harris', cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage('image', image) # show the image
#cv.ShowImage('warp', warp)
#cv.SaveImage('harris.jpg', imcsolor)
cv.WaitKey()