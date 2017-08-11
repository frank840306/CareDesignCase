from utils import *
from file import File
# from logManager import setupLogger
import logging, time

class Hospital:
	def __init__(
		self, 
		hospitalName, 
		fileNumPerHospital=default_config['FILE_NUM_PER_HOSPITAL'],
		):
		self.logger = logging.getLogger(__name__)
		self.hospitalName = hospitalName
		self.fileNumPerHospital = fileNumPerHospital
		self.filenameList = []
		self.fileClassDict = {}
		self.loadData()

	def getInputFeature(self, filename):
		features = {}
		if filename not in self.filenameList:
			self.logger.info('Requested file [ %15s ] does not exist' % (filename))
		else:
			if filename not in self.fileClassDict:
				self.fileClassDict[filename] = File(self.hospitalName, filename)
			features = self.fileClassDict[filename].inputFeature
		return features

	def getOutputFeature(self, filename):
		features = []
		if filename not in self.filenameList:
			self.logger.info('Requested file [ %15s ] does not exist' % (filename))
		else:
			if filename not in self.fileClassDict:
				self.fileClassDict[filename] = File(self.hospitalName, filename)
			features = self.fileClassDict[filename].outputFeature
		return features		

	def getFileList(self):
		return self.filenameList

	def getModelList(self, filename):
		if filename not in self.filenameList:
			modelList = []
			self.logger.info('File [ %15s ]  does not exist' % (filename))
		else:
			if filename not in self.fileClassDict:
				self.fileClassDict[filename] = File(self.hospitalName, filename)
			modelList = self.FileClassDict[filename].getModelList()
			self.logger.info(modelList)
		return modelList

	def addFile(self, filename):
		if len(self.filenameList) < self.fileNumPerHospital:
			if filename not in self.filenameList:
				self.filenameList.append(filename)
				self.fileClassDict[filename] = File(self.hospitalName, filename)
				msg = 'Add new file [ %15s ]' % (filename)
			else:
				msg = 'File [ %15s ] in the list' % (filename)
		else:
			msg = 'File number of hospital [ %5s ] achieves limit %d' % (self.hospitalName, self.fileNumPerHospital)
		return msg 

	def loadData(self):
		self.lastLoadDate = time.strftime('%Y%m%d') 
		self.lastLoadTime = time.strftime('%H%M%S')

		saveData = readObject(object_type['hospital'], self.hospitalName)
		if saveData != None:
			# load data from file
			self.logger.info('Loading hospital object [ %5s ]' % (self.hospitalName))
		
			self.filenameList = saveData['filenameList']
			self.addDate = saveData['addDate']
			self.addTime = saveData['addTime']
		else:
			# first time create the object
			self.addDate = self.lastLoadDate
			self.addTime = self.lastLoadTime
		return

	def dumpData(self):
		self.logger.info('Dumping hospital object [ %5s ]' % (self.hospitalName))
		saveData = {
			'filenameList':self.filenameList,
			'addDate':self.addDate,
			'addTime':self.addTime,
		}
		writeObject(object_type['hospital'], self.hospitalName, saveData)
		# call every file object to dumpData
		for filename in self.fileClassDict:
			self.fileClassDict[filename].dumpData()
		return

	def showInfo(self):
		self.logger.info('[ HOSPITAL ] --> name: %5s, addTime: %s %s, lastLoadTime: %s %s' % (
			self.hospitalName, 
			self.addDate,
			self.addTime,
			self.lastLoadDate,
			self.lastLoadTime
		))
		for filename in self.fileClassDict:
			self.fileClassDict[filename].showInfo()
		return
# setupLogger()

# hospitalA = Hospital('NTU')
# hospitalA.dumpData()
# hospitalA.showInfo()
# time.sleep(2)
# hospitalB = Hospital('NTU')
# hospitalB.showInfo()


