from utils import *
import logging
class TrainingManager():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.trainingQueue = []
		self.loadData()

	def addTask(self):
		
	def createProcess(self):	

	def loadData(self):
		saveData = readObject(object_type['tm'], 'trainingManager')
		if saveData != None:
			self.logger.info('Loading training manager')
			self.trainingQueue = saveData['trainingQueue']
		return

	def dumpData(self):
		self.logger.info('Dumping training manager')
		saveData = {
			'trainingQueue' : self.trainingQueue
		}
		writeObject(object_type['tm'], 'trainingManager', saveData)
		return