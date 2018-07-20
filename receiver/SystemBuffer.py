
import multiprocessing

class SystemBuffer:

	def __init__(self, size):
		print("Packet Buffer Created")

		self.manager = multiprocessing.Manager()
		self.size = self.manager.Value('i', size)
		self.occupancy = self.manager.Value('i', 0)
		self.queue = self.manager.list([])



	def addPacket(self, raw):
		packetSize = len(raw)/2 
		newOccunpancy = self.occupancy + packetSize
		if newOccunpancy <= self.size:
			with self.manager.get_lock():
				self.occupancy = newOccunpancy
				self.queue.append(raw)

	def getPacket(self):
		packetSize = len(self.queue[0])
		self.size -= packetSize
		return self.queue.pop(0)
