#EncodeFrame.py
"""Takes in a network packet in HEX and Link Packet ID along with QR Link characteristics.
Outputs string segments for QR encoding.  Provides functions for building and sending QR Codes
over MIMO optical link."""


import QRGenerator
from time import sleep
from rgbmatrix import Adafruit_RGBmatrix


class EncodeFrame(object):

    def __init__(self, frame, version, qrECC, qrSize, packetID, linkID, matrix, speed):
        """Constructor"""

        self.packetID = '{0:08b}'.format(packetID)
        self.linkID = '{0:07b}'.format(linkID)
        self.version = version
        self.qrECC = qrECC
        self.qrSize = qrSize
        self.frame = self.__prepFrame__(frame)
        self.segArray = []
        self.matrix = matrix
        self.speed = speed

        self.__prepareQRMessages__()

    def __prepFrame__(self, frame):
        """Converts raw network packet hex string to appropriate Alphanumeric format."""

        frame = frame.upper()
        return frame.replace(" ", "")


    def __prepareQRMessages__(self):
        """Segments packet into appropriately sized stings for QR encoding.  First byte
        (first 2 Alphanumeric/hex characters) of the string are used for segment identification data.
        First bit is 0 if there are more segments in packet, 1 if it is the last packet.  The following
        7 bits are used as a semi unique identifier (between 0 and 127) for the packet the segment
        belongs to."""

        self.segLen = self.qrSize - 6  #total length of bytes in frame is the capacity of the qr code minus 6 bytes for the frame header
    
        data = self.frame
        padding = ""
        frameID = 0

        #7/18/2018 - The packets sent via the QR code are also saved to a text file which can be used to compare to what is received
        while True:
            if len(data) <= self.segLen:
                header = self.buildSegHeader(self.linkID, self.packetID, frameID, '1')  
                for i in range(self.segLen - len(data)):
                    padding += "Z"  #"Z" is used to fill empty space in a QOTR frame 
                data = header + data + padding
                #The packets sent via the QR code are also saved to a text file
                with open('test7.txt', 'a') as test_file:
                    test_file.write(data + '\n')
                self.segArray.append(data)
                break

            header = self.buildSegHeader(self.linkID, self.packetID, frameID, '0')  #gets hex header
            seg = header + data[:self.segLen]
            data = data[self.segLen:]

            with open('test7.txt', 'a') as test_file:
                test_file.write(seg + '\n')

            self.segArray.append(seg)
            frameID += 1
            
        print(self.segArray)

        test_file.close()


    def sendPacket(self):
        """Uses the QRCode class to send all prepared packet segments."""
        qrCount = 0
        for seg in self.segArray:
##            print(seg)
            QR = QRGenerator.QRCode(seg, self.version, self.qrECC, self.matrix, self.speed)
            QR.drawQR()
            qrCount += 1
##            del QR
        sleep(self.speed)
        return qrCount

    def buildSegHeader(self, linkID, packetID, frameID, terminalBit):
        """Creates proper  header for Frame"""
        header = ''
        linkBin = terminalBit + linkID[:3] + ' ' + linkID[3:]  #converts decimal linkID to binary
        packetBin = ' ' + packetID[:4] + ' ' + packetID[4:]  #converts decimal packetID to binary
        frameBin = '{0:08b}'.format(frameID)
        frameBin = ' ' + frameBin[:4] + ' ' + frameBin[4:]
        headerBin = linkBin + packetBin + frameBin  #builds binary header
        for part in headerBin.split(' '):   #converts header to hex
            header += hex(int(part, 2))[2:].upper()
##        print(header)
        return header











######MAIN#####

##packet = "53 70 6f 74 55 64 70 30 84 fe b2 49 f5 e8 b7 59 00 01 00 04 48 95 c2 03 96 f7 b9 90 47 1e bb 92 4c c2 93 25 66 da 85 d6 93 b0 74 88"
##prep = EncodePacket(packet, 3,"H", 100)
##prep.sendPacket()
##packet = "FF 70 6f 74 55 64 70 30 84 fe b2 49 f5 e8 b7 59 00 01 00 04 48 95 c2 03 96 f7 b9 90 47 1e bb 92 4c c2 93 25 66 da 85 d6 93 b0 74 88"
##prep = EncodePacket(packet, 3,"H", 10)
##prep.sendPacket()

##packet = "FF 70 6f 74 55 64 70 30 84 fe b2 49 f5 e8 b7 59 00 01 00 04 48 95 c2 03 96 f7 b9 90 47 1e bb 92 4c c2 93 25 66 da 85 d6 93 b0 74 88"
##prep = EncodeFrame(packet, 3,"H", 29, 1, 1, 0)
