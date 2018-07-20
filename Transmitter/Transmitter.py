#Transmitter.py
"""This class is initiated through the LinkLayerInterface.py file.  It initializes a RGBmatrix object and takes in network
packets that are to be transmitted.  Then it converts those packets to the QOTR protocol and dispays them
on the LED matrix to initiate an optical link."""

import EncodeFrame
import QR_DICTIONARIES
from time import sleep
from time import time
from rgbmatrix import Adafruit_RGBmatrix

class Transmitter:

    def __init__(self, version, qrECC, linkID, duration, speed):
        """Contructor"""
        self.linkID = linkID
        self.matrix = Adafruit_RGBmatrix(32,1)
        self.currentID = 0
        self.version = version
        self.versionLength = QR_DICTIONARIES.VERSION_SIZE[version]
        self.qrECC = qrECC
        self.qrSize = self.__selectDict__(qrECC)
        self.speed = speed
        self.startTime = time()
        self.duration = duration
        self.packetsSent = 0
        self.bytesSent = 0
        self.qrsSent = 0

##        self.__startTransmitter__()

    def __startTransmitter__(self, queue):
        """Initializes the LED matrix with a basic pattern to assist receiver in
        adjusting to glare."""
        print("Transmitter Started")
        self.homeScreen(6)
        self.__transmit__(queue)
        sleep(.2)
        self.homeScreen(3)

    def __transmit__(self, queue):
        """Transmits network packets that are contained in the share memory queue."""
        self.homeScreen(0)
        print("Transmitting")
        cont = self.checkTime() #used for testing.  sets total transmit time of trial
        while cont == True:
            cont = self.checkTime()
            try:
                packet = queue.pop(0)
                print("Transmitting: ",packet)
##                self.matrix.Clear()
                prep = EncodeFrame.EncodeFrame(packet, self.version, self.qrECC, self.qrSize, self.currentID, self.linkID, self.matrix, self.speed)
                self.packetsSent += 1
                self.bytesSent += (len(packet)/2)
                self.qrsSent += prep.sendPacket()
                self.__incrementID__() #gets new PID for next packet
                if len(queue) == 0:                    
                    self.homeScreen(0)
                

            except:
                self.homeScreen(0)
        print("Finished Transmission")
        print(str(self.packetsSent) + " packets sent (" + str(self.bytesSent) + " bytes) in " + str(self.duration) + " seconds.")
        rate = self.bytesSent / self.duration
        print(str(rate) + " Bps")
        print(str(self.qrsSent) + " Frames Sent")
        
    def checkTime(self):
        """used for testing.  limits trial transmit time to a defined length to prevent overheading
        of RPi."""
        now = time()
        if self.duration > (now - self.startTime):
            return True
        else:
            return False
    

    def __incrementID__(self):
        """Increments packet ID."""
        if self.currentID >= 255:
            self.currentID = 0
        else:
            self.currentID += 1
 
    def __selectDict__(self, qrECC):
        """Determines capacity dictionary to use for error correction level."""


        if qrECC == "L":
            return QR_DICTIONARIES.QR_DICT_L[self.versionLength]
        elif qrECC == "M":
            return QR_DICTIONARIES.QR_DICT_M[self.versionLength]
        elif qrECC == "Q":
            return QR_DICTIONARIES.QR_DICT_Q[self.versionLength]
        elif qrECC == "H":
            return QR_DICTIONARIES.QR_DICT_H[self.versionLength]
        else:
            print("Error: Invalid Error Correction Level selected.")
            pass
        

    def homeScreen(self, duration):
        """Displays alternating on/off LED pattern to be used at the beginning of transmission
        and when no packets are in the shared queue."""
        print("Home Screen")
        for i in range(31):
            if i%2 == 1:
                
                for j in range(31):
                    if j%2 == 1:
                        self.matrix.SetPixel(i, j,0, 0, 150)
                    else:
                        self.matrix.SetPixel(i, j, 0, 0, 0)
            else:
                for j in range(31):
                    if j%2 == 0:
                        self.matrix.SetPixel(i, j,0, 0, 150)
                    else:
                        self.matrix.SetPixel(i, j, 0, 0, 0)
        if duration != 0:
            sleep(duration)
##            self.matrix.Clear()
                

##queue = ["53 70 6f 74 55 64 70 30 84 fe b2 49 f5 e8 b7 59 00 01 00 04 48 95 c2 03 96 f7 b9 90 47 1e bb 92 4c c2 93 25 66 da 85 d6 93 b0 74 88"
##]
##transmitter = Transmitter(3, "H", 1)
##transmitter.__startTransmitter__(queue)
        
            
