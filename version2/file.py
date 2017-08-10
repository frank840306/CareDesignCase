from utils import *
# from logManager import setupLogger
import logging, time, re

class File:
	def __init__(
		self,
		hospitalName,
		filename,
		data_dir=default_path['DATA_DIR'],
		modelNumPerFile=default_config['MODEL_NUM_PER_FILE'],
		):
		self.logger = logging.getLogger(__name__)
		self.hospitalName = hospitalName
		self.filename = filename
		self.data_dir = data_dir
		self.modelNumPerFile = modelNumPerFile
		self.modelNameList = []
		self.modelClassDict = {}
		self.xlsxFile = '%s.xlsx' % (self.filename)
		self.csvFile = '%s.csv' % (self.filename)
		self.inputFeature = {}
		self.outputFeature = []
		self.loadData()
	
	def getInputFeature(self):
		csv_header = open(os.path.join(self.data_dir, self.csvFile)).readline()[:-1].split(',')
		inputFeature = [val for val in csv_header if 'IN' in val]
		boolFeature = []
		floatFeature = []

		for idx in range(len(inputFeature)):
			inputFeature[idx] = re.sub(r'IN\d+', '', inputFeature[idx])
			if 'Bool' in inputFeature[idx]:
				inputFeature[idx] = re.sub(r'Bool', '', inputFeature[idx])
				boolFeature.append(inputFeature[idx])
			elif 'Float' in inputFeature[idx]:
				inputFeature[idx] = re.sub(r'Float', '', inputFeature[idx])
				floatFeature.append(inputFeature[idx])
		
		return {'bool': boolFeature, 'float': floatFeature}

	def getOutputFeature(self):
		csv_header = open(os.path.join(self.data_dir, self.csvFile)).readline()[:-1].split(',')
		outputFeature = [val for val in csv_header if 'OUT' in val]
		for idx in range(len(outputFeature)):
			outputFeature[idx] = re.sub(r'OUT\d+', '', outputFeature[idx])	

		return outputFeature
	def getModelList(self):
		return self.modelNameList
		
	def prepareCSVFile(self):
		if self.csvFile not in os.listdir(self.data_dir):
			if self.xlsxFile not in os.listdir(self.data_dir):
				self.logger.info('Please upload CSV/XLSX formated file in [ %s ]' % (self.data_dir))
				return False	
			else:
				XLSX2CSV(os.path.join(self.data_dir, self.xlsxFile))
				self.logger.info('Convert file format: XLSX --> CSV')
				return True
		else:
			self.logger.info('CSV exists --> do nothing')
			return True

	def loadData(self):
		self.lastLoadDate = time.strftime('%Y%m%d') 
		self.lastLoadTime = time.strftime('%H%M%S')

		saveData = readObject(object_type['file'], '%s_%s' % (self.hospitalName, self.filename))
		if saveData != None:
			# load data from file
			self.logger.info('Loading file object [ %5s --> %15s ]' % (
				self.hospitalName,
				self.filename,
			))
			self.modelNameList = saveData['modelNameList']
			self.inputFeature = saveData['inputFeature']
			self.outputFeature = saveData['outputFeature']
			self.addDate = saveData['addDate']
			self.addTime = saveData['addTime']
		else:
			# first time create the object
			# make sure the csv/xlsx file exists
			if not self.prepareCSVFile():
				# no csv file ready
				return
			# get input and output features
			self.inputFeature = self.getInputFeature()
			self.outputFeature = self.getOutputFeature()
			self.addDate = self.lastLoadDate
			self.addTime = self.lastLoadTime
		return

	def dumpData(self):
		self.logger.info('Dumping file object [ %5s --> %15s ]' % (
			self.hospitalName,
			self.filename
		))
		saveData = {
			'modelNameList'	: self.modelNameList,
			'inputFeature'	: self.inputFeature,
			'outputFeature'	: self.outputFeature,
			'addDate'		: self.addDate,
			'addTime'		: self.addTime,
		}
		writeObject(object_type['file'], '%s_%s' % (self.hospitalName, self.filename), saveData)
		# TODO:
		# call every model object to dumpData
		return
	
	def showInfo(self):
		self.logger.info('[ FILE ] --> name: %20s, addTime: %s %s, lastLoadTime: %s %s' % (
			'%s_%s' % (self.hospitalName, self.filename),
			self.addDate,
			self.addTime,
			self.lastLoadDate,
			self.lastLoadTime
		))
		# TODO:
		# call showInfo of every model
		return

# setupLogger()

# fileA = File('NTU', 'example_37_14')
# fileA.dumpData()
# fileA.showInfo()

# time.sleep(2)
# fileB = File('NTU', 'example_37_14')
# fileB.showInfo()