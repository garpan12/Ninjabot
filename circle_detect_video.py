import cv2.cv as cv
import cv2
import sys
import numpy as np

capture = cv.CaptureFromCAM(0)

# some random colors to draw circles and their center points with
d_red = cv.RGB(150, 55, 65)
l_red = cv.RGB(250, 200, 200)

def autocalibrate(orig, storage):
    
    circles = np.asarray(storage)
    #print 'drawing: ' + str(len(circles)) + ' circles'

    min_value = 255
    max_value = 0
    s = []
    for circle in circles:
        Radius, x, y = int(circle[0][2]), int(circle[0][0]), int(circle[0][1])
        processed =  cv.CreateImage(cv.GetSize(orig),8,3)
        cv.CvtColor(orig,processed, cv.CV_BGR2HSV)
        s.append(cv.Get2D(processed,y,x))

    return s
        
    #cropped  = cv.CreateImage((Radius/2,Radius/2),8,3)
    #sub = cv.GetSubRect(orig,(x,y,Radius/2,Radius/2))
    #cv.Copy(sub,cropped)
    #cv.ShowImage('cropped',cropped)
    #hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
    """cv.CalcHist(cropped,hist)
    (min_tmp,max_tmp, _, _) = cv.GetMinMaxHistValue(hist)
    if min_tmp <= min_value:
        min_value = min_tmp
    if max_tmp >= max_value:
        max_value = max_tmp"""
    #return cropped


def colorFilter(img, color, calibrate):

    imgHSV = cv.CreateImage(cv.GetSize(img),8,3)
    cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)

    if color == "yellow":
        minColor = cv.Scalar(20, 70, 70)
        maxColor = cv.Scalar(60, 255, 255)
    elif color == "blue":
        minColor = cv.Scalar(100,100,100)
        maxColor = cv.Scalar(120,255,255)
    elif color == "calibrate":
         minColor = cv.Scalar(calibrate[0],calibrate[1],calibrate[2])
         maxColor = minColor

    imgFiltered = cv.CreateImage(cv.GetSize(img),8,1)

    cv.InRangeS(imgHSV, minColor, maxColor, imgFiltered)

    return imgFiltered

def colorFilterCombine(img, color1, color2, s):
    imgFiltered = cv.CreateImage(cv.GetSize(img),8,1)
    imgColor1 = cv.CreateImage(cv.GetSize(img),8,1)
    imgColor2 = cv.CreateImage(cv.GetSize(img),8,1)  
    imgCalibrate = cv.CreateImage(cv.GetSize(img),8,1)   
    
    imgColor1 = colorFilter(img, color1 ,s)
    imgColor2 = colorFilter(img, color2 ,s)

    cv.Add(imgColor1, imgColor2, imgFiltered)

    if s != []:
        for value in s:
            imgCalibrate = colorFilter(img, "calibrate" , value)
            cv.Add(imgFiltered, imgCalibrate, imgFiltered)
            print value[0],value[1],value[2], "added"

    return imgFiltered 

'''def channel_processing(channel):
    pass
    cv.AdaptiveThreshold(channel, channel, 255, adaptive_method=cv.CV_ADAPTIVE_THRESH_MEAN_C, thresholdType=cv.CV_THRESH_BINARY, blockSize=55, param1=7)
    #mop up the dirt
    cv.Dilate(channel, channel, None, 1)
    cv.Erode(channel, channel, None, 1)'''

def find_circles(processed, storage, LOW):
    print "Finding circles" 

    # Use Hough Circles algorithm to find circles
    # Parameters:
    # @ image is the 8-bit single channel image you want to search for circles in. 
    # @ circle_storage is where the function puts its results. You can pass a CvMemoryStorage structure here.
    # @ method is always CV_HOUGH_GRADIENT
    # @ dp lets you set the resolution of the accumulator. dp is a kind of scaling down factor. 
    #       The greater its value, the lower the resolution of the accumulator. dp must always be more than or equal to 1.
    # @ min_dist is the minimum distance between circle to be considered different circles.
    # @ param1 is used for the (internally called) canny edge detector. The first parameter of the canny is set to param1, and the second is set to param1/2.
    # @ param2 sets the minimum number of votes that an accumulator cell needs to qualify as a possible circle.
    # @ min_radius and max_radius do exactly what to mean. They set the minimum and maximum radii the function searches for.
    
    try:
        cv.HoughCircles(processed, storage, cv.CV_HOUGH_GRADIENT, 2, 30.0, 70, 70, 25, 70) #great to add circle constraint sizes.
    except:
        pass

    if storage.rows == 0:
        print "no circles found"

    return storage

def draw_circles(storage, output):
    # if there are more than 30 circles something went wrong, don't draw anything
    if storage.rows <= 0:
        return

    if storage.rows >= 30:
        return

    circles = np.asarray(storage)
    print 'drawing: ' + str(len(circles)) + ' circles'

    for circle in circles:
        Radius, x, y = int(circle[0][2]), int(circle[0][0]), int(circle[0][1])
        cv.Circle(output, (x, y), 1, l_red, -1, 8, 0)
        cv.Circle(output, (x, y), Radius, d_red, 3, 8, 0)

        


orig = cv.QueryFrame(capture)
processed = cv.CreateImage((orig.width,orig.height), cv.IPL_DEPTH_8U, 1)
storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
s = []

while True:
    orig = cv.QueryFrame(capture)
    #cv.Normalize(orig)
    # filter for all yellow and blue - everything else is black
    processed = colorFilterCombine(orig, "yellow", "blue" ,s)
    
    # Some processing and smoothing for easier circle detection
    cv.Canny(processed, processed, 5, 70, 3)
    cv.Smooth(processed, processed, cv.CV_GAUSSIAN, 7, 7)
    
    cv.ShowImage('processed2', processed)
    
    # Find&Draw circles
    find_circles(processed, storage, 100)

    #if it is in the range of 1 to 9, we can try and recalibrate our filter
    if 1 <= storage.rows < 10:
        s = autocalibrate(orig, storage)
        


    draw_circles(storage, orig)

    # Delete and recreate the storage so it has the correct width
    del(storage)
    storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
    
    cv.ShowImage('output', orig)

    if cv.WaitKey(10) == 27:
        break
