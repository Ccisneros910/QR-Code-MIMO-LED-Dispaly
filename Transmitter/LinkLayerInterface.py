#LinkLayerInterface.py
"""This file contains the main class for the QOTR/LED system.  Call from command line."""

from __future__ import print_function
import ethernetReader
import time
import EthernetWriter
import multiprocessing
import sys
from Transmitter import Transmitter
import random


class LinkLayerInterface:

	def __init__(self, linkID, qrVersion, qrECC, duration, speed):
                """Constructor"""
		self.linkID = linkID
		self.speed = self.speedValue(speed)
		self.qrVersion = qrVersion
		self.qrECC = qrECC
		self.duration = duration
##		self.matrix = Adafruit_RGBmatrix(32,1)

		

		print("QOTR System Booting: \nQR Verion %d ECC %s \nLink ID %d \n" % (self.qrVersion,self.qrECC, self.linkID))

		self.manager = multiprocessing.Manager()
		self.queue = self.manager.list([])

                self.buildQueue()

                #Uncomment these lines to support full duplex link
##                trans = multiprocessing.Process(target=Transmitter.__startTransmitter__, args=(self.transmitter, self.queue))
##                trans.start()
                
##		self.EthernetReader = ethernetReader.EthernetReader()
##		self.EthernetWriter = EthernetWriter.EthernetWriter()

##		reader = multiprocessing.Process(target=ethernetReader.EthernetReader.read, args=(self.EthernetReader, self.queue))
##		writer = multiprocessing.Process(target=EthernetWriter.EthernetWriter.checkForPacket, args=(self.EthernetWriter, self.queue))

##		reader.start()
##		writer.start()

                self.transmitter = Transmitter(self.qrVersion, self.qrECC, self.linkID, self.duration, self.speed)
                self.transmitter.__startTransmitter__(self.queue)

                reader.terminate()

                
		# self.EthernetReader.read()
		# self.EthernetWriter.checkForPacket()	

		try:
			while True:
				pass
		except KeyboardInterrupt:
			reader.terminate()
##			writer.terminate()
			sys.exit()
		except:
			pass
	def speedValue(self, speed):
                # allow user to input lower and upper case letters
                if speed.upper() == "S":
                        return .1
                elif speed.upper() == "M":
                        return .05
                elif speed.upper() =="F":
                        return 0
                #if invalid, warn user
                else:
                        print("Invalid speed setting. Options are S, M, or F.\n");

        def buildQueue(self):
                """For testing purposes, instead of using the ethernetRead.py this version reads packets from a PCAP.  To create variation
                it randomizes which packets from the file are used."""
                packets = open("parsedPackets.txt","r")
                thresh = 1000
                count = 0
                for line in packets:
                        if thresh <= count:
                                break
                        if len(line) < 40:
                                pass
                        elif "(" in line:
                                pass
                        else:
                                packet = line.strip("\n")
                                self.queue.append(packet)
                                count += 1
                random.shuffle(self.queue)
                self.queue = self.queue[0:50]
                print( "Test Queue Built")
                
                

LinkLayerInterface(69, 3, "H", 300, "M")
