#QRCodeTextToLEDDisplay.py
"""Takes in a string and QR code parameters and produces a QR Code of data.  Provides functions
to display a QR code on a 32x32 Adafruit LED board."""

import pyqrcode
from time import sleep
from rgbmatrix import Adafruit_RGBmatrix

class QRCode:
    def __init__(self, data, version, qrECC, matrix, speed):
        """Constructor"""

        self.version = version
        self.qrECC = qrECC
        self.data = data
        self.__processQR__(self.data)
        self.matrix = matrix
        self.speed = speed

    def __del__(self):
        pass
        

        
    def __processQR__(self, data):
        """Encodes data into specified type of QR Code and then prepares QR Code data to be
        sent to LED Board."""

        qr = pyqrcode.create(data, error= self.qrECC, version=self.version, mode='alphanumeric')
        qrText = qr.text()
        #print qrText
        self.dimension = qrText.index('\n') - 6
        qrArray = qrText.split('\n')
        ledData = []

        for y in range(self.dimension):
            line = qrArray[y +3]
            row = []

            for x in range(self.dimension):
                bit = line[x+ 3]
                row.append(str(bit))


            ledData.append(row)

        self.ledData = ledData


            
    def drawQR(self):
        """Draws single qr code on the RGBmatrix."""
        print("sent")
        counter = 0
        
        for y in range(self.dimension):
            for x in range(self.dimension):
                counter = counter + 1
                bit = self.ledData[y][x]
                #print bit
                if bit == "0":
                    """
                    if counter < 310:
                        self.matrix.SetPixel(x, y, 200, 0, 0)
                    elif counter >= 310 and counter < 620:
                        self.matrix.SetPixel(x, y, 0, 200, 0)
                    else:
                    """
                    self.matrix.SetPixel(x, y, 0, 0, 200)
                elif bit == "1":
                    self.matrix.SetPixel(x, y, 0, 0, 0)
                else:
                    print( "Error: invalid bit value.")
                    break
        sleep(self.speed)


    

                




# myQR.drawQR()
