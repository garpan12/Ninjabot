#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy as np


#convert the image from RGB TO HSV for easier filtering
def RGBtoHSV(img):

	imgHSV = cv.CreateImage(cv.GetSize(img),8,3)

	#Convert the image to HSV (Hue, Saturation value) color model
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)

	return imgHSV

#filter the image to get everything yellow
def colorFilter(img, color):

	imgHSV = cv.CreateImage(cv.GetSize(img),8,1)
	imgHSV = RGBtoHSV(img)

	if color == "yellow":
		# the range to filter for to get the color yellow (tweak later when shade of yellow is clear)
		minColor = cv.Scalar(20, 100, 100)
		maxColor = cv.Scalar(30, 255, 255)
	elif color == "blue":
		minColor = cv.Scalar(100,100,100)
		maxColor = cv.Scalar(120,255,255)

	imgFiltered = cv.CreateImage(cv.GetSize(img),8,1)

	cv.InRangeS(imgHSV, minColor, maxColor, imgFiltered)

	return imgFiltered

cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
image=cv.LoadImage('testmap.png', cv.CV_LOAD_IMAGE_COLOR) #Load the image

''' #How to put text onto the image
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
x = 50
y = 50
cv.PutText(image,"Hello World!!!", (x,y),font, 255) #Draw the text

#combine arrays (images):
cv.Add(imgyellow,imgblue,imgthreshold)
'''

yellow = colorFilter(image, 'yellow')
blue = colorFilter(image, 'blue')
cv.ShowImage('a_window', blue)

while True:
    if cv.WaitKey(10) == 27:
        break
cv.SaveImage('image.png', image) #Saves the image