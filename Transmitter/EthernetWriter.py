from __future__ import print_function
from scapy.all import *
import multiprocessing
import time

class EthernetWriter:

	def __init__(self):
		print("Ethernet Writer Started")
		self.localInterface = 'eth0'

	def sendPacket(self, packet):
		sendp(Ether()/packet, iface=self.localInterface)
		

	def checkForPacket(self, packetBuffer):
		while True:
			try:				
				nextPacket = packetBuffer.pop(0)
				# print("Writer: ", nextPacket)
				self.sendPacket(nextPacket)
				# time.sleep(1)

			except:
				pass

##writer = EthernetWriter()
##writer.sendPacket("53706f745564703084feb249f5e8b75900010004482396f7b990471ebb92")
        
