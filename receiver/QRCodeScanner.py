import cv2
import cv2 as cv #computer vision library to interface with cameras
import numpy
import zbar #reads any type of barcode
import time
import threading
from PIL import Image
import zbarlight
"""
Play around with the resolution of the camera.
Less is more. Lowering the resolution will hhelp the camera recognize the QR codes
"""


class QRCodeScanner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.WINDOW_NAME = 'Camera'
        self.CV_SYSTEM_CACHE_CNT = 1 # Cv has 5-frame cache
        self.LOOP_INTERVAL_TIME = 0.01 # about how fast it scans

        cv.namedWindow(self.WINDOW_NAME, cv.WINDOW_AUTOSIZE) #the cv window (what the camera sees)
        self.cam = cv2.VideoCapture(-1) # -1 is whatever webcam a computer can find
        self.currentSegment = None 
        #self.currentSegment = queue 

    def scan(self, aframe):
        # what type of image is it? (python image PIL?)
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY) # converts images to black and white
        #raw = str(imgray.data)
        pil_img = Image.fromarray(imgray) #convert it to a python librart image
        npy_img = numpy.array(pil_img) # zbar requires the PLI to be converted to a numpy array

        scanner = zbar.Scanner()
        scanner.scan(imgray) # this might be unneccasary 

        codes = scanner.scan(npy_img) #with the zbar scanner we are checking to see if there areny QR codes in the image
        
        try:
            code = codes[0].data #take the data portion of the scanned QR code
            segment = code.decode('utf-8')
            self.currentSegment = segment
            print("Scanner: ", segment)
        except:
            self.currentSegment = None # do we need this? what is this doing?
            #self.currentSegment.insert(0, "X")

    def run(self):
        #print 'BarCodeScanner run', time.time()
        while True:
            #print time.time()
            for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                #print 'Read2Throw', time.time()
                self.cam.read()
            #print 'Read2Use', time.time()
            img = self.cam.read() # you see whatever image is the cam
            self.scan(img[1]) # then the image is scanned

            cv2.imshow(self.WINDOW_NAME, img[1])
            cv.waitKey(1)
            #print 'Sleep', time.time()
            #time.sleep(self.LOOP_INTERVAL_TIME)

        cam.release()

    def getCurrentSegment(self):
        return self.currentSegment


#scanner = QRCodeScanner()
#scanner.start()
