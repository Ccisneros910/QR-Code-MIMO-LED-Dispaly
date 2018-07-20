import cv2
import cv2 as cv
import numpy
import zbar
import time
import threading
from PIL import Image
import zbarlight


class QRCodeScanner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.WINDOW_NAME = 'Camera'
        self.CV_SYSTEM_CACHE_CNT = 1 # Cv has 5-frame cache
        self.LOOP_INTERVAL_TIME = 0.01

        cv.namedWindow(self.WINDOW_NAME, cv.WINDOW_AUTOSIZE)
        self.cam = cv2.VideoCapture(-1)
        self.currentSegment = None

    def scan(self, aframe):
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
        #raw = str(imgray.data)
        pil_img = Image.fromarray(imgray)
        npy_img = numpy.array(pil_img)

        scanner = zbar.Scanner()
        scanner.scan(imgray)

        codes = scanner.scan(npy_img)
        try:
            code = codes[0].data
            segment = code.decode('utf-8')
            self.currentSegment = segment
            print("Scanner: ", segment)
        except:
            self.currentSegment = None

    def run(self):
        #print 'BarCodeScanner run', time.time()
        while True:
            #print time.time()
            for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                #print 'Read2Throw', time.time()
                self.cam.read()
            #print 'Read2Use', time.time()
            img = self.cam.read()
            self.scan(img[1])

            cv2.imshow(self.WINDOW_NAME, img[1])
            cv.waitKey(1)
            #print 'Sleep', time.time()
            #time.sleep(self.LOOP_INTERVAL_TIME)

        cam.release()

    def getCurrentSegment(self):
        return self.currentSegment


#scanner = QRCodeScanner()
#scanner.start()
