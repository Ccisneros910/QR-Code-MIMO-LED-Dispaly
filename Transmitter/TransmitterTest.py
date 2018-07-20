import EncodeFrame
import QR_DICTIONARIES
from time import sleep
from time import time
from rgbmatrix import Adafruit_RGBmatrix

class Transmitter:

    def __init__(self, version, qrECC, linkID,duration):
        self.linkID = linkID
        self.matrix = Adafruit_RGBmatrix(32,1)
        self.currentID = 0
        self.version = version
        self.qrECC = qrECC
        self.qrSize = int(QR_DICTIONARIES.VERSION_SIZE[version])
        self.dict = self.__selectDict__(qrECC)
        self.startTime = time()
        self.duration = duration

##        self.__startTransmitter__()

    def __startTransmitter__(self, queue):
        print("Transmitter Started")
        self.homeScreen(3)
        self.__transmit__(queue)
        sleep(.2)
        self.homeScreen(3)

    def __transmit__(self, queue):
        self.homeScreen(0)
        cont = self.checkTime()
        while cont == True:
            cont = self.checkTime()
            try:
                packet = queue.pop(0)
                print("Transmitting: ",packet)
                self.matrix.Clear()
                prep = EncodeFrame.EncodeFrame(packet, self.version, self.qrECC, self.qrSize, self.currentID, self.linkID, self.matrix)
                prep.sendPacket()
                self.__incrementID__()
                self.homeScreen(0)
                

            except:
                pass

    def checkTime(self):
        now = time()
        if self.duration > (now - self.startTime):
            return True
        else:
            return False


    def __incrementID__(self):
        if self.currentID >= 255:
            self.currentID = 0
        else:
            self.currentID += 1
 
    def __selectDict__(self, qrECC):
        """Determines capacity dictionary to use for error correction level."""


        if qrECC == "L":
            self.dict = QR_DICTIONARIES.QR_DICT_L
        elif qrECC == "M":
            self.dict = QR_DICTIONARIES.QR_DICT_M
        elif qrECC == "Q":
            self.dict = QR_DICTIONARIES.QR_DICT_Q
        elif qrECC == "H":
            self.dict = QR_DICTIONARIES.QR_DICT_H
        else:
            print("Error: Invalid Error Correction Level selected.")
            pass
        return self.dict

    def homeScreen(self, duration):

        for i in range(32):
            if i%2 == 1:
                
                for j in range(32):
                    if j%2 == 1:
                        self.matrix.SetPixel(i, j,0, 0, 200)
                    else:
                        self.matrix.SetPixel(i, j, 0, 0, 0)
            else:
                for j in range(32):
                    if j%2 == 0:
                        self.matrix.SetPixel(i, j,0, 0, 200)
                    else:
                        self.matrix.SetPixel(i, j, 0, 0, 0)
        if duration != 0:
            sleep(duration)
            self.matrix.Clear()
                

queue = ["53 70 6f 74 55 64 70 30 84 fe b2 49 f5 e8 b7 59 00 01 00 04 48 95 c2 03 96 f7 b9 90 47 1e bb 92 4c c2 93 25 66 da 85 d6 93 b0 74 88"
]
transmitter = Transmitter(3, "H", 1, 10)
transmitter.__startTransmitter__(queue)
        
            
