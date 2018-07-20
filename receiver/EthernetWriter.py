from __future__ import print_function
from scapy.all import *
import multiprocessing # dedicates an entire piece of the computer's processing power to a task
import time

#IS NOT DONE
#is going to be trickier because it involves networking

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
        
