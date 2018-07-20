from __future__ import print_function
from scapy.all import *
import multiprocessing



class EthernetReader:

	def __init__(self):
		
		# multiprocessing.Process.__init__(self)
		# self.buffer = systemBuffer
		self.localMAC = "08:00:27:0b:96:7c"
		self.localIP = "10.0.0.129"
		self.localInterface = 'eth0'
		# self.read()

	def read(self, queue):
                print("Ethernet Reader Started")
		while True:
		# for i in range(5):	
			p = sniff(iface=self.localInterface, count=1)
			frame = p[0]
##			print("Read: ",str(frame[ARP]).encode("HEX"))
			check = self.__filter__(frame)
##			if check == True:
                        print(frame.summary())
                        packet = self.stripHeader(frame)
                        print(packet)
                        queue.append(packet)
				# print(str(ip).encode("HEX"))
		

	def __filter__(self, frame):
		if (frame.dst == self.localMAC) and (frame[IP].dst != self.localIP):
			return True
		return False

	def stripHeader(self, frame):
                try:
##                        packet = IP(str(frame[IP])[0:frame[IP].len])
                        packet = str(frame[IP]).encode("HEX")
                        return packet
                except:
                        try:
                                packet = str(frame[ARP]).encode("HEX")
                                return packet
                        except:
                                pass
##                        packet = ARP(str(frame[ARP])[0:frame[ARP].len])
##                        packet = str(packet).encode("HEX")
##                        return packet
                
##queue = []
##e = EthernetReader()
##e.read(queue)
