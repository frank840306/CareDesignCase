from utils import *
from casemodel import kerasModel		# ML model from Kevin
from rfModel import RandomForestModel	# ML model from Andy
from trainingManager import TrainingManager
import logging, time, shutil

class HospitalManager:
	def __init__(
		self, 
		data_dir=default_path['DATA_DIR'],
		mdl_dir=default_path['MDL_DIR'],
		hospitalJsonFile=default_path['HOSPITALJSON'],
		hospital2modelJsonFile=default_path['HOSPITAL2MODELJSON'],
		fileNumPerHospital=default_config['FILE_NUM_PER_HOSPITAL'],
		modelNumPerFile=default_config['MODEL_NUM_PER_FILE'],
		trainingQueueFile=default_path['TRAININGQUEUEJSON'],
		method=default_config['TRAINING_METHOD'],
		):
		self.logger = logging.getLogger(__name__)
		self.data_dir = data_dir
		self.mdl_dir = mdl_dir
		self.hospitalJsonFile = hospitalJsonFile
		self.hospital2modelJsonFile = hospital2modelJsonFile
		self.hospitalList, self.hospital2model = self.loadData()
		self.fileNumPerHospital = fileNumPerHospital
		self.modelNumPerFile = modelNumPerFile
		self.method = method
		self.tm = TrainingManager(jsonFile=trainingQueueFile)
		self.tm.train()

	def loadData(self):
		self.logger.info('Loading data from [ %s ] and [ %s ]' % (self.hospitalJsonFile, self.hospital2modelJsonFile))
		if os.path.exists(self.hospitalJsonFile):
			hospitalListJson = readJson(self.hospitalJsonFile)
			hospitalList = json.loads(hospitalListJson)
		else:
			hospitalList = []
		self.logger.info(hospitalList)
		if os.path.exists(self.hospital2modelJsonFile):
			hospital2modelJson = readJson(self.hospital2modelJsonFile)
			hospital2model = json.loads(hospital2modelJson)
		else:
			hospital2model = {}
		self.logger.info(hospital2model)
		return hospitalList, hospital2model
			
	def dumpData(self):
		self.logger.info('Dumping data to [ %s ] and [ %s ]' % (self.hospitalJsonFile, self.hospital2modelJsonFile))
		if len(self.hospitalList) == 0:
			if os.path.exists(self.hospitalJsonFile):
				os.remove(self.hospitalJsonFile)
				# open(self.hospitalJsonFile, 'w').truncate()
		else:
			hospitalListJson = json.dumps(self.hospitalList)
			writeJson(hospitalListJson, self.hospitalJsonFile)
			self.logger.info(hospitalListJson)
		if len(self.hospital2model) == 0:
			if os.path.exists(self.hospital2modelJsonFile):
				os.remove(self.hospital2modelJsonFile)
				# open(self.hospital2modelJsonFile, 'w').truncate()
		else:
			hospital2modelJson = json.dumps(self.hospital2model)
			writeJson(hospital2modelJson, self.hospital2modelJsonFile)
			self.logger.info(hospital2modelJson)
		return

	def getCurrentModel(self, hospital):
		pass
	def getInputFeature(self, hospital, filename):
		features = {'Bool': [], 'Float': []}
		if hospital in self.hospitalList:
			if filename in self.hospital2model[hospital]:
				task = self.tm.getTask(hospital, filename, self.hospital2model[hospital][filename][-1])
				# features['Bool'] = {'Bool' : task['BoolFeature'], 'Float' : task['FloatFeature']}
				# TODO:
				# features['Float']	## 2017.7.18 bigyo modify this
				features = {'Bool' : task['BoolFeature'], 'Float' : task['FloatFeature']}
				msg = 'Success get features from CSV file [ %s ] in [ %s ]' % (filename, hospital)	 
			else:
				msg = 'Current hospital [ %s ] doesn\'t have  CSV file [ %s ]' % (hospital, filename)
		else:
			msg = 'No hospital named [ %s ]' % (hospital)
		self.logger.info(msg)
		return features

	def getOutputFeature(self, hospital, filename):
		features = []
		if hospital in self.hospitalList:
			if filename in self.hospital2model[hospital]:
				task = self.tm.getTask(hospital, filename, self.hospital2model[hospital][filename][-1])
				features = task['outputFeature']
				# TODO:
				# features['Float']
				msg = 'Success get features from CSV file [ %s ] in [ %s ]' % (filename, hospital)	 
			else:
				msg = 'Current hospital [ %s ] doesn\'t have  CSV file [ %s ]' % (hospital, filename)
		else:
			msg = 'No hospital named [ %s ]' % (hospital)
		self.logger.info(msg)
		return features

	def predictFocus(self, data, hospital, filename, time=-1):
		pred = None
		focus = self.getOutputFeature(hospital, filename)
		if len(focus) == 0:
			# hospital does not have the CSV file
			msg = 'Current hospital [ %s ] does not have CSV file [ %s ]' % (hospital, filename)
		else:
			task = self.tm.getTask(hospital, filename, self.hospital2model[hospital][filename][time])
			if task == -1:
				msg = 'Could not get specified task [ %s, %s, %s]' % (hospital, filename, self.hospital2model[hospital][filename][time])
			else:
				self.logger.info(data)
				# model = readPickle(task['modelClassFile'])
				if task['method'] == 'keras':
					model = kerasModel(task['modelName'], task['hospital'])
				elif task['method'] == 'rf':
					model = RandomForestModel(task['modelName'], task['hospital'])
				else:
					model = None
				if model == None:
					msg = 'Model [ %s, %s ] does not exists, with mothod [ %s     ]' % (task['modelName'], task['hospital'], task['method'])
				else:
					pred_idx = model.predictFocus(data)
					pred = [focus[idx] for idx in pred_idx]
					msg = 'Success predict result from model'

				# model = readPickle(task['modelClassFile'])
				# pred_idx = model.predictFocus(data)
				# pred = [focus[idx] for idx in pred_idx]
				# msg = 'Success predict result from model class[ %s ]' % (task['modelClassFile'])
				
		self.logger.info(msg)
		return pred

	def updateModel(self):
		for hospital in self.hospitalList:
			modelUsed = hospital + '_' + time.strftime('%Y%m%d')
			# if len(self.hospital2model[hospital]) == 0 or self.hospital2model[hospital][-1]:
				# 
				# pass
		pass
	

	def addHospital(self, hospital):
		if hospital not in self.hospitalList:
			# Success to add a new hospital
			self.logger.info('Adding a new hospital [ %s ] to list' % (hospital))
			self.hospitalList.append(hospital)
			self.hospital2model[hospital] = {}
			# create their own directory
			hospital_dir = os.path.join(self.mdl_dir, hospital)
			if not os.path.exists(hospital_dir):
				os.makedirs(hospital_dir)
			msg = 'Add a new hospital named [ %s ]' % (hospital)
		else:
			# Fail
			msg = 'Hospital named [ %s ] has already in the list' % (hospital)
		self.logger.info(msg)
		return msg

	def removeHospital(self, hospital):
		if hospital in self.hospitalList:
			self.logger.info('Remove a hospital [ %s ] from list' % (hospital))
			self.hospitalList.remove(hospital)
			del self.hospital2model[hospital] 
			# remove model file from the directory
			hospital_dir = os.path.join(self.mdl_dir, hospital)
			if os.path.exists(hospital_dir):
				shutil.rmtree(hospital_dir)
			msg = 'Remove a hospital named [ %s ]' % (hospital)
		else:
			msg = 'No hospital named [ %s ] to be removed' % (hospital)

		self.logger.info(msg)
		return msg

	def addFile(self, hospital, filename, method=None):
		if hospital in self.hospitalList:
			if filename not in self.hospital2model[hospital]:
				if len(self.hospital2model[hospital]) >= self.fileNumPerHospital:
					msg = 'Current hospital cannot maintain more than [ %d ] CSV file' % (self.fileNumPerHospital)
				else:
					self.hospital2model[hospital][filename] = []
					# TODO:
					# add into training queue
					self.tm.addTask(hospital, filename, time.strftime('%Y%m%d'), method)
					# self.hospital2model[hospital][filename].append('%s_%s_%s' % (hospital, filename, time.strftime('%Y%m%d')))
					self.hospital2model[hospital][filename].append(time.strftime('%Y%m%d'))
					msg = 'Add a new CSV file named [ %s ] in hospital [ %s ]' % (filename, hospital)
			else:
				msg = 'CSV file named [ %s ] has already in the hospital [ %s ]' % (filename, hospital)
		else:
			# cannot add model becaues no this hospital
			msg = 'Cannot add file because current hospital [ %s ] does not exist' % (hospital)
		self.logger.info(msg)
		return msg

	def removeFile(self, hospital, filename):
		if hospital in self.hospitalList:
			if filename in self.hospital2model[hospital]:
				# TODO:
				# check training queue
				# self.tm.setTaskStatus(hospital, filename, time.strftime('%Y%m%d'))
				self.tm.removeTask(hospital, filename, time.strftime('%Y%m%d'))
				del self.hospital2model[hospital][filename]
				msg = 'Remove a CSV file named [ %s ] in hospital [ %s ]' % (filename, hospital)
			else:
				msg = 'No CSV file named [ %s ] in hospital [ %s ] to be removed' % (filename, hospital)
		else:
			msg = 'No hospital named [ %s ] to be removed' % (hospital)
		self.logger.info(msg)
		return msg

	def shutdown(self, signal, frame):
		# before closing server

		self.tm.shutdown()
		self.dumpData()
		exit(0)
