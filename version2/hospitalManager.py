from utils import *
from trainingManager import TrainingManager
from hospital import Hospital
from file import File
from logManager import setupLogger

import logging, time, shutil

class HospitalManager:
	def __init__(
		self,
		mdl_dir=default_path['MDL_DIR'],
		# data_dir=default_path['DATA_DIR'],
		fileNumPerHospital=default_config['FILE_NUM_PER_HOSPITAL'],
		modelNumPerFile=default_config['MODEL_NUM_PER_FILE'],
		trainingMethod=default_config['TRAINING_METHOD']
		):
		self.logger = logging.getLogger(__name__)
		self.mdl_dir = mdl_dir
		# self.data_dir = data_dir
		self.fileNumPerHospital = fileNumPerHospital
		self.modelNumPerFile = modelNumPerFile
		self.trainingMethod = trainingMethod
		self.hospitalNameList = []
		self.hospitalClassDict = {}
		self.tm = TrainingManager()
		self.loadData()

	def getInputFeature(self, hospitalName, filename):
		if hospitalName not in self.hospitalNameList:
			# ERROR
			feature = {}
			self.logger.info('Hospital [ %5s ]  does not exist' % (hospitalName)) 
		else:
			if hospitalName not in self.hospitalClassDict:
				self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			feature = self.hospitalClassDict[hospitalName].getInputFeature(filename)
			self.logger.info(feature)
		return feature

	def getOutputFeature(self, hospitalName, filename):
		if hospitalName not in self.hospitalNameList:
			feature = []
			self.logger.info('Hospital [ %5s ]  does not exist' % (hospitalName)) 
		else:
			if hospitalName not in self.hospitalClassDict:
				self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			feature = self.hospitalClassDict[hospitalName].getOutputFeature(filename)
			self.logger.info(feature)
		return feature

	def getHospitalList(self):
		return self.hospitalNameList

	def getFileList(self, hospitalName):
		if hospitalName not in self.hospitalNameList:
			fileList = []
			self.logger.info('Hospital [ %5s ]  does not exist' % (hospitalName))
		else:
			if hospitalName not in self.hospitalClassDict:
				self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			fileList = self.hospitalClassDict[hospitalName].getFileList()
			self.logger.info(fileList)
		return fileList

	def getModelList(self, hospitalName, filename):
		if hospitalName not in self.hospitalNameList:
			modelList = []
			self.logger.info('Hospital [ %5s ]  does not exist' % (hospitalName))
		else:
			if hospitalName not in self.hospitalClassDict:
				self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			modelList = self.hospitalClassDict[hospitalName].getModelList(filename)
			self.logger.info(modelList)
		return modelList

	def predictFocus(self, hospitalName, filename):
		return []
	def trainModel(self):
		return
	def updateModel(self):
		return
	def addHospital(self, hospitalName):
		if hospitalName not in self.hospitalNameList:
			self.hospitalNameList.append(hospitalName)
			self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			if not os.path.exists(os.path.join(self.mdl_dir, hospitalName)):
				os.makedirs(os.path.join(self.mdl_dir, hospitalName))
			msg = 'Add new hospital [ %5s ]' % (hospitalName)
		else:
			msg	= 'Hospital [ %5s ] in the list' % (hospitalName)

		self.logger.info(msg)
		return msg

	def removeHospital(self, hospitalName):
		return
	def addFile(self, hospitalName, filename):
		if hospitalName not in self.hospitalNameList:
			# ERROR
			msg = 'Hospital [ %5s ]  does not exist' % (hospitalName)
		else:
			if hospitalName not in self.hospitalClassDict:
				self.hospitalClassDict[hospitalName] = Hospital(hospitalName)
			msg = self.hospitalClassDict[hospitalName].addFile(filename)
			# add to training manager
			self.tm.addTask()
		self.logger.info(msg)	
		return msg

	def removeFile(self, hospitalName, filename): 
		return
	def addModel(self, hospitalName, filename, date):
		return
	def loadData(self):
		saveData = readObject(object_type['hm'], 'hospitalManager')
		if saveData != None:
			self.logger.info('Loading hospital manager')
			self.hospitalNameList = saveData['hospitalNameList']

		return 
	def dumpData(self):
		self.logger.info('Dumping hospital manager')
		saveData = {
			'hospitalNameList' : self.hospitalNameList, 
		}
		writeObject(object_type['hm'], 'hospitalManager', saveData)
		# dump training manager
		self.tm.dumpData()
		# call every hospital object to dumpData
		for hospitalName in self.hospitalClassDict:
			self.hospitalClassDict[hospitalName].dumpData()
		return
	def showInfo(self):
		self.logger.info('=================================== SHOW INFO ===================================')
		self.logger.info('[ HOSPITAL MANAGER ] -->  hospital number: %2d, file limit: %2d, model limit: %2s, training method: %5s' % (
			len(self.hospitalNameList),
			self.fileNumPerHospital,
			self.modelNumPerFile,
			self.trainingMethod
		))
		self.logger.info('Hospital List: ' + ', '.join(self.hospitalNameList))
		for hospitalName in self.hospitalClassDict:
			self.hospitalClassDict[hospitalName].showInfo()		

setupLogger()



hm = HospitalManager()
hm.addHospital('NTU')
hm.addFile('NTU', 'example_37_14')
hm.showInfo()
hm.getInputFeature('NTU', 'example_37_14')
hm.getOutputFeature('NTU', 'example_37_14')
hm.dumpData()
time.sleep(2)

print('\n\n\n')
hm = HospitalManager()
hm.addFile('NTU', 'example_37_14')
hm.addFile('NTU', 'example_37_14_2')
hm.getInputFeature('NTU', 'example_37_14')
hm.getOutputFeature('NTU', 'example_37_14')
# fileA = File('NTU', 'example_37_14')
# fileA.showInfo()

# hospitalA = Hospital('NTU')
# hospitalA.showInfo()

# hospitalA.filenameList.append('example_37_14')
# hospitalA.fileClassDict['example_37_14'] = fileA

# hm = HospitalManager()
# hm.hospitalNameList.append('NTU')
# hm.hospitalClassDict['NTU'] = hospitalA

# hm.dumpData()

