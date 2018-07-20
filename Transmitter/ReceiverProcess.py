import QRCodeScanner
import time

TB = 0
LID = 1
FID = 2
SID = 3

class Receiver:
    def __init__(self, linkID):
        self.linkID = linkID
        self.scanner = QRCodeScanner.QRCodeScanner()
        self.scanner.start()
        self.currentID = None
        self.currentPacket = ''
        self.terminalFlag = False
        self.lastSeg = ''
        self.timeStart = 0
        self.timeEnd = 0
        self.nextSegNum = 0

    def receive(self):
        while True:
            try:
                segment = self.scanner.getCurrentSegment()

                if (segment != None):  ##prevent frames with no QR from being processed
                    print("Recevier: ", segment)
                    if (segment != self.lastSeg):  ##prevent duplicate QRs from being processed
                        self.lastSeg = segment

                        headerMetrics = self.processHeader(segment)
                        tB = headerMetrics[TB]
                        lID = headerMetrics[LID]
                        fID = headerMetrics[FID]
                        sID = headerMetrics[SID]

                        if lID != self.linkID:
                            pass

                        else:
                            validFrame = self.checkFrame(fID, sID, tB)
                            if validFrame == True:
                                self.currentID = fID
                                self.currentFrame += segment[2:].strip('Z')

                                if self.checkTerminal(tB) == True:
                                    self.serialForward()
                                    break

                                self.nextSegNum += 1

            except:
                pass

            time.sleep(.08)

    def serialForward(self):
        print("Packet Received: ", self.currentFrame)
        self.timeEnd = time.time()
        self.calcSpeed()
        self.flagFinish = True

    def calcSpeed(self):
        time = self.timeEnd - self.timeStart
        print(time)
        speed = len(self.currentFrame) / 2
        print("Transmit Speed (Bps): ", speed)

    def newFrame(self):

        self.currentFrame = ''
        self.nextSeg = 0
        self.lastSeg = ''
        self.timeStart = time.time()

    def processHeader(self, segment):
        header = segment[:6]
        linkByte = header[:2]
        frameByte = header[2:4]
        segByte = header[4:]
        (terminalBit, linkNum) = self.processLinkByte(linkByte)

        frameNum = int(frameByte,16)
        segNum = int(segByte,16)
        return (terminalBit, linkNum, frameNum, segNum)


    def processLinkByte(self, linkByte):
        binary = bin(int(linkByte,16))[2:]
        terminalBit = binary[0]
        linkBin = binary[1:]
        linkNum = int(linkBin,2)
        return (terminalBit, linkNum)


    def checkFrame(self, frameID, segID):
        if self.terminalFlag == True:
            self.newFrame()

        if (frameID == self.currentFrame) or (self.currentFrame == None):
            if self.nextSegNum == segID:
                return True
            else:
                return False
        else:
            return False

    def checkTerminal(self, terminalBit):
        if terminalBit == '1':
            self.terminalFlag == True
            return True
        elif terminalBit == '0':
            return False





receiver = Receiver()
receiver.receive()


