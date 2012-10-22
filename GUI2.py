import wx
import cv2.cv as cv
import win32api 
import win32con 

#The panel containing the webcam video

import sys
import numpy as np

capture = cv.CaptureFromCAM(1)

# some random colors to draw circles and their center points with
d_red = cv.RGB(150, 55, 65)
l_red = cv.RGB(250, 200, 200)
orig = cv.QueryFrame(capture)
processed = cv.CreateImage((orig.width,orig.height), cv.IPL_DEPTH_8U, 1)
grid = cv.CreateImage((orig.width*2,orig.height), cv.IPL_DEPTH_8U, 3)
storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
s = []


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


def draw_grid(grid):
    #bg = cv.Scalar(255, 255, 255)
    #cv.Rectangle(grid,(0,0),(grid.width,grid.width),bg, cv.CV_FILLED )

    color = cv.Scalar(20, 70, 70)
    x=0;
    while x < grid.width:
        #cv.Point
        cv.Line(grid, (x,0), (x,grid.width), color, thickness=1, lineType=8, shift=0)
        x = x  + 20;

    x=0;
    while x < grid.height:
        #cv.Point
        cv.Line(grid, (0,x), (grid.width,x), color, thickness=1, lineType=8, shift=0)
        x = x  + 20;    
        #for y in range(0 , grid.height):
         #   cv.Line(grid, (x,x), (x,y), color, thickness=1, lineType=8, shift=5)
    #for
     #   Line(img, pt1, pt2, color, thickness=1, lineType=8, shift=0)        

def update_grid(storage, output, grid ):
    #grid = cv.CreateImage((orig.width*2,orig.height), cv.IPL_DEPTH_8U, 3)
    warp = perspective_transform(output)
    draw_grid(warp)
    
    #draw_circles(storage , warp)
    return warp


def perspective_transform(image_in):
    #gray = cv.CreateImage(cv.GetSize(image_in),8,1)
    #cv.CvtColor(image_in,gray, cv.CV_BGR2GRAY)
    image = np.asarray(image_in[:,:])
    #img = cv2.GaussianBlur(image,(5,5),0)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #eig_image = cv.CreateImage(cv.GetSize(image_in),8,1)
    #temp_image= cv.CreateImage(cv.GetSize(image_in),8,1)
    #cornerMap = cv.CreateMat(image_in.height, image_in.width, cv.CV_32FC1)
    #cornerMap =cv.GoodFeaturesToTrack(gray, eig_image, temp_image, 4, 0.04, 1, useHarris = True)
    #print cornerMap #[(491.0, 461.0), (203.0, 38.0), (195.0, 58.0), (201.0, 56.0)]
    src = np.array([[225,0],[545,44],[0,398],[450,480]],np.float32)
    dst = np.array([[0,0],[image_in.width,image_in.height],[0,image_in.height],[image_in.width,0]],np.float32)
    retval = cv2.getPerspectiveTransform(src,dst)
    warp = cv2.warpPerspective(image, retval, (cv.GetSize(image_in)))

    output = cv.fromarray(warp)

    return output


def run():
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
    #if 1 <= storage.rows < 10:
    #    s = autocalibrate(orig, storage)
        


    draw_circles(storage, orig)

    warp = update_grid(storage, orig, grid)


    # Delete and recreate the storage so it has the correct width
    del(storage)
    storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
    
    #cv.ShowImage('output', orig)

    return processed
    
    #cv.ShowImage('grid', warp)

    #warp = perspective_transform(orig)
    #cv.ShowImage('warped', warp)



class CvDisplayPanel(wx.Panel):
    TIMER_PLAY_ID = 101 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        """
        #magic to stop the flickering
        def SetCompositeMode(self, on=True): 
            exstyle = win32api.GetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE) 
            if on: 
                exstyle |= win32con.WS_EX_COMPOSITED 
            else: 
                exstyle &= ~win32con.WS_EX_COMPOSITED 
            win32api.SetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE, exstyle) 

        SetCompositeMode(self, True)
        """

        #self.capture = cv.CaptureFromCAM(0) # turn on the webcam
        #img = cv.QueryFrame(self.capture) # Convert the raw image data to something wxpython can handle.
        #cv.CvtColor(img, img, cv.CV_BGR2RGB) # fix color distortions
        img = run()
        self.bmp = wx.BitmapFromBuffer(img.width, img.height, img.tostring())
        sbmp = wx.StaticBitmap(self, -1, bitmap=self.bmp) # Display the resulting image

        
        self.playTimer = wx.Timer(self, self.TIMER_PLAY_ID) 
        wx.EVT_TIMER(self, self.TIMER_PLAY_ID, self.onNextFrame) 
        fps = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FPS) 

        if fps!=0: self.playTimer.Start(1000/fps) # every X ms 
        else: self.playTimer.Start(1000/15) # assuming 15 fps 


    def onNextFrame(self, evt):
        #img = cv.QueryFrame(self.capture)
        img = run()
        if img:
            #cv.CvtColor(img, img, cv.CV_BGR2RGB)
            self.bmp.CopyFromBuffer(img.tostring()) # update the bitmap to the current frame
            self.Refresh()
        evt.Skip()


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700,700))
        self.displayPanel = CvDisplayPanel(self) # display panel for video

        self.CreateStatusBar() # A Statusbar in the bottom of the window

        filemenu= wx.Menu() # Setting up the menu.

        # wx.ID_EXIT is a standard ID provided by wxWidgets.
        filemenu.AppendSeparator()
        menuExit=filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # events for the menu bar
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        menuBar = wx.MenuBar() # Creating the menubar.
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

    def OnExit(self,evt):
        self.Close(True)  # Close the frame.


draw_grid( grid )
app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = MyFrame(None, "GUI Magic") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
