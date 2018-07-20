from __future__ import print_function
from scapy.all import * # used to capture network traffic in Python
import multiprocessing

"""

"""

class EthernetReader:

	def __init__(self):
		
		# multiprocessing.Process.__init__(self)
		# self.buffer = systemBuffer
		self.localMAC = "08:00:27:0b:96:7c" # maybe not used
		self.localIP = "10.0.0.129" # maybe not used
		# will not get pushed the to transmitter ^
		self.localInterface = 'eth0' # used to know what local ethernet port is being read from
		# self.read()

	def read(self, queue):
                print("Ethernet Reader Started")
		while True:
		# for i in range(5):	
			p = sniff(iface=self.localInterface, count=1)
			# count - the number of frames being sniffed
			frame = p[0] #just want the frame itself
##			print("Read: ",str(frame[ARP]).encode("HEX"))
			check = self.__filter__(frame) # traffic that is destined for another device
##			if check == True:
                        print(frame.summary())
                        packet = self.stripHeader(frame) # to get hex packet that the transmitter is going to deal
                        print(packet)
                        queue.append(packet) # then head packet to management keep
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
