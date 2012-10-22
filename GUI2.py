'''How to integrate openCV and wxpython.

This program loads an image file using openCV, converts it to a format
which wxpython can handle and displays the resulting image in a
wx.Frame.'''


import wx
import cv2.cv as cv
import cv2
import win32api 
import win32con 
import processor


#The panel containing the webcam video
class CvDisplayPanel(wx.Panel):
    TIMER_PLAY_ID = 101 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        #magic to stop the flickering
        def SetCompositeMode(self, on=True): 
            exstyle = win32api.GetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE) 
            if on: 
                exstyle |= win32con.WS_EX_COMPOSITED 
            else: 
                exstyle &= ~win32con.WS_EX_COMPOSITED 
            win32api.SetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE, exstyle) 

        SetCompositeMode(self, True)

        #self.capture = cv.CaptureFromCAM(0) # turn on the webcam
        #img = ImagePro # Convert the raw image data to something wxpython can handle.
        #cv.CvtColor(img, img, cv.CV_BGR2RGB) # fix color distortions
        storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
        ImagePro(capture,orig,processed,storage,grid)
        cv.CvtColor(orig, orig, cv.CV_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(orig.width, orig.height, orig.tostring())
        sbmp = wx.StaticBitmap(self, -1, bitmap=self.bmp) # Display the resulting image

        
        self.playTimer = wx.Timer(self, self.TIMER_PLAY_ID) 
        wx.EVT_TIMER(self, self.TIMER_PLAY_ID, self.onNextFrame) 
        fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS) 

        if fps!=0: self.playTimer.Start(1000/fps) # every X ms 
        else: self.playTimer.Start(1000/15) # assuming 15 fps 

        #del(storage)
        #storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)


    def onNextFrame(self, evt):
        storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
        ImagePro(capture,orig,processed,storage,grid)
        #img = processed
        if orig:
            cv.CvtColor(orig, orig, cv.CV_BGR2RGB)
            self.bmp.CopyFromBuffer(orig.tostring()) # update the bitmap to the current frame
            self.Refresh()
            #del(storage)
            #storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
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

#def ImageInit(camera):


def ImagePro(capture,orig,processed,storage,grid):
    orig = cv.QueryFrame(capture)
    #cv.Normalize(orig)
    # filter for all yellow and blue - everything else is black
    processed = processor.colorFilterCombine(orig, "yellow", "blue" ,s)
    
    # Some processing and smoothing for easier circle detection
    cv.Canny(processed, processed, 5, 70, 3)
    cv.Smooth(processed, processed, cv.CV_GAUSSIAN, 7, 7)
    
    #cv.ShowImage('processed2', processed)
    
    # Find&Draw circles
    processor.find_circles(processed, storage, 100)

    #if it is in the range of 1 to 9, we can try and recalibrate our filter
    #if 1 <= storage.rows < 10:
    #    s = autocalibrate(orig, storage)
        


    processor.draw_circles(storage, orig)

    #warp = processor.update_grid(storage, orig, grid)


    # Delete and recreate the storage so it has the correct width
    del(storage)
    storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
    
    #cv.ShowImage('output', orig)

    #return processed
    #cv.ShowImage('grid', warp)

    #warp = perspective_transform(orig)
    #cv.ShowImage('warped', warp)

#ImageInit(0)
capture = cv.CaptureFromCAM(0)


orig = cv.QueryFrame(capture)
processed = cv.CreateImage((orig.width,orig.height), cv.IPL_DEPTH_8U, 1)
grid = cv.CreateImage((orig.width*2,orig.height), cv.IPL_DEPTH_8U, 3)
storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
s = []

processor.draw_grid(grid)

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = MyFrame(None, "GUI Magic") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
