from utils import *
from casemodel import kerasModel		# ML model from Kevin
from rfModel import RandomForestModel	# ML model from Andy
import logging, threading, os, re

class TrainingManager:
	def __init__(
		self, 
		data_dir=default_path['DATA_DIR'],
		mdl_dir=default_path['MDL_DIR'],
		jsonFile=default_path['TRAININGQUEUEJSON'],
		trainingQueueSize=default_config['TRAINING_QUEUE_SIZE'],
		trainingSkipNum=default_config['TRAINING_SKIP_NUM'],
		method=default_config['TRAINING_METHOD'],
		):
		self.logger = logging.getLogger(__name__)
		self.data_dir = data_dir
		self.mdl_dir = mdl_dir
		self.trainingQueueFile = jsonFile
		self.trainingQueue = self.loadData()
		self.trainingQueueSize = trainingQueueSize
		self.trainingSkipNum = trainingSkipNum
		self.method = method
		self.trainingThread = None
		self.threadLock = threading.Lock()
		self.showQueueInfo()

	def train(self):
		skipCnt = 0
		while True:
			curTask = None
			for task in self.trainingQueue:
				if task['status'] == status['Ongoing']:
					# remove the unfinished file
					curTask = task
					break
				elif task['status'] == status['Opened']:
					curTask = task
					break

			# check whether find a task or not
			if skipCnt > self.trainingSkipNum:
				self.logger.info('There\'s no task found after %d iteration --> close thread' % (skipCnt))
				break
			if curTask == None:
				skipCnt += 1
				break
			else:
				skipCnt = 0
				# TODO:
				# start training
				if curTask['method'] == 'keras':
					model = kerasModel(curTask['modelName'], curTask['hospital'])
					modelFile = curTask['modelName'] + '_model.h5' 
					
				elif curTask['method'] == 'rf':
					model = RandomForestModel(curTask['modelName'], curTask['hospital'])
					modelFile = curTask['modelName'] + '.pkl'
					
				else:	
					self.logger('Current method [ %s ] hasn\'t been implemented' % (curTask['method']))
					self.removeTask(curTask['hospital'], curTask['filename'], curTask['time'])
					continue
				self.logger.info('Current model: %s, model file: %s' % (model, modelFile))
				# model = kerasModel(curTask['modelName']) if curTask['method'] == 'keras' else RandomForestModel(curTask['modelName'])
				# modelFile = curTask['modelName'] + '_model.h5' if curTask['method'] == 'keras' else curTask['modelName'] + '.pkl'
				hospital_dir = os.path.join(self.mdl_dir, curTask['hospital'])
				if modelFile not in os.listdir(hospital_dir):
					if curTask['csvFile'] not in os.listdir(self.data_dir):
						if curTask['xlsxFile'] in os.listdir(self.data_dir):
							self.logger.info('Convert file format: XLSX --> CSV')
							XLSX2CSV(os.path.join(self.data_dir, curTask['xlsxFile']))
						else:
							self.logger.info('Please upload CSV/XLSX formated file in [ %s ]' % (self.data_dir))
					else:
						self.logger.info('CSV exists --> do nothing')
					csv_header = open(os.path.join(self.data_dir, curTask['csvFile'])).readline()[:-1].split(',')
					# curTask['inputFeature'] = [val for val in csv_header if 'IN' in val]
					# curTask['outputFeature'] = [val for val in csv_header if 'OUT' in val]
					# self.logger.info(curTask['input_d'])
					# self.logger.info(self.trainingQueue[0]['input_d'])
					# self.showTaskInfo(curTask)
					# self.showTaskInfo(self.trainingQueue[0])
					# input_d = len([val for val in csv_header if 'IN' in val])
					# output_d = len([val for val in csv_header if 'OUT' in val])
					self.logger.info('Start training: args = ( %s, %d, %d)' % (os.path.join(self.data_dir, curTask['csvFile']), len(curTask['inputFeature']), len(curTask['outputFeature'])))
					model.trainModel(os.path.join(self.data_dir, curTask['csvFile']), len(curTask['inputFeature']), len(curTask['outputFeature']))
					
					modelClassFile = os.path.join(hospital_dir, 'class_' + modelFile)
					writePickle(model, modelClassFile)
					curTask['modelClassFile'] = os.path.join(modelClassFile)
					curTask['status'] = status['Closed']
					# self.setTaskStatus(curTask['hospital'], curTask['filename'], curTask['time'], status['Closed'])
					self.logger.info(curTask['status'])
					self.logger.info(self.trainingQueue[0]['status'])
					
				else:
					self.logger.info('model exists --> skip training')


			

		return
	def start(self):
		# open new thread to train model
		if self.trainingThread != None and self.trainingThread.isAlive():
			self.logger.info('Training thread exists --> pass')
		else:
			self.logger.info('Training thread does not exist --> create one')
			self.trainingThread = threading.Thread(target=self.train)
			self.trainingThread.start()
			
		return
	
	def close(self):
		if self.trainingThread != None:
			self.trainingThread.join()
		return

	def addTask(self, hospital, filename, time, specifiedMethod=None):
		if len(self.trainingQueue) >= self.trainingQueueSize:
			self.logger.info('Training queue cannot afford more than [ %d ] tasks' % (self.trainingQueueSize))
		else:
			task = {
				'hospital'	: hospital,
				'filename'	: filename,
				'time'		: time,
				'modelName'	: '%s_%s_%s' % (hospital, filename, time),
				'xlsxFile'	: '%s.xlsx' % (filename),
				'csvFile'	: '%s.csv' % (filename),
				'status'	: status['Opened'],
				'method'	: self.method if specifiedMethod == None else specifiedMethod
			}
			
			csv_header = open(os.path.join(self.data_dir, task['csvFile'])).readline()[:-1].split(',')		
			task['inputFeature'] = [val for val in csv_header if 'IN' in val]
			task['BoolFeature'] = []
			task['FloatFeature'] = []
			for idx in range(len(task['inputFeature'])):
				task['inputFeature'][idx] = re.sub(r'IN\d+', '', task['inputFeature'][idx])
				if 'Bool' in task['inputFeature'][idx]:
					task['inputFeature'][idx] = re.sub(r'Bool', '', task['inputFeature'][idx])
					task['BoolFeature'].append(task['inputFeature'][idx])
				elif 'Float' in task['inputFeature'][idx]:
					task['inputFeature'][idx] = re.sub(r'Float', '', task['inputFeature'][idx])
					task['FloatFeature'].append(task['inputFeature'][idx])



				task['inputFeature'][idx] = re.sub(r'Bool\d+', '', task['inputFeature'][idx])
				task['inputFeature'][idx] = re.sub(r'Float\d+', '', task['inputFeature'][idx])
				print(task['inputFeature'][idx])
			task['outputFeature'] = [val for val in csv_header if 'OUT' in val]
			for idx in range(len(task['outputFeature'])):
				task['outputFeature'][idx] = re.sub(r'OUT\d+', '', task['outputFeature'][idx])		
			self.trainingQueue.append(task)
			self.showTaskInfo(self.trainingQueue[-1])
			# self.start()
			self.train()

	def removeTask(self, hospital, filename, time):
		for idx, task in enumerate(self.trainingQueue):
			if task['modelName'] == '%s_%s_%s' % (hospital, filename, time):
				self.logger.info('Remove task [ %s ] from training queue' % (task['modelName']))
				if task['status'] == status['Ongoing']:
					# TODO:
					# handle the ongoing training
					self.setTaskStatus(hospital, filename, time, status['Suspended'])
					# self.trainingQueue.pop(idx)
				else:
					self.setTaskStatus(hospital, filename, time, status['Suspended'])
					# self.trainingQueue.pop(idx)
				break
		return

	def loadData(self):
		self.logger.info('Loading data from [ %s ]' % (self.trainingQueueFile))
		if os.path.exists(self.trainingQueueFile):
			trainingQueueJson = readJson(self.trainingQueueFile)
			trainingQueue = json.loads(trainingQueueJson)
		else:
			trainingQueue = []
		self.logger.info(trainingQueue)
		return trainingQueue

	def dumpData(self):
		self.logger.info('Dumping data to [ %s ]' % (self.trainingQueueFile))
		if len(self.trainingQueue) == 0:
			if os.path.exists(self.trainingQueueFile):
				os.remove(self.trainingQueueFile)
		else:
			trainingQueueJson = json.dumps(self.trainingQueue)
			writeJson(trainingQueueJson, self.trainingQueueFile)
			self.logger.info(trainingQueueJson)
		return

	def setTaskStatus(self, hospital, filename, time, toStatus):
		for task in self.trainingQueue:
			if task['modelName'] == '%s_%s_%s' % (hospital, filename, time):
				self.logger.info('Set model [ %s ] from [ %s ] to [ %s ]' % (task['modelName'], task['status'], toStatus))
				task['status'] = toStatus
					
				# if task['status'] == status['Ongoing']:	
				# 	# TODO:
				# 	# terminate the training
				# 	task['status'] = status['Suspended']
				# 	# start train the next task
				# else:
				# 	task['status'] = status['Suspended']
				break
		return

	def getTaskStatus(self, hospital, filename, time):
		for task in self.trainingQueue:
			if task['modelName'] == '%s_%s_%s' % (hospital, filename, time):
				return task['status']
		return -1
	def getTask(self, hospital, filename, time):
		for task in self.trainingQueue:
			if task['modelName'] == '%s_%s_%s' % (hospital, filename, time):
				return task
		return -1
	def showTaskInfo(self, task):
		self.logger.info('-------------------- TASK INFO ---------------------')
		self.logger.info('hospital	: %s' % (task['hospital']))
		self.logger.info('CSV file	: %s' % (task['filename']))
		self.logger.info('time		: %s' % (task['time']))
		self.logger.info('model name	: %s' % (task['modelName']))
		self.logger.info('XLSX source	: %s' % (task['xlsxFile']))
		self.logger.info('CSV source	: %s' % (task['csvFile']))
		self.logger.info('task status	: %s' % (task['status']))
		self.logger.info('method	: %s' % (task['method']))
		self.logger.info('----------------------------------------------------')

	def showQueueInfo(self):
		self.logger.info('------------------- QUEUE INFO ---------------------')
		for idx, task in enumerate(self.trainingQueue):
			self.logger.info('%3d: model name: %15s, status: %10s, method: %10s' % (idx, task['modelName'], task['status'], task['method']))
		self.logger.info('----------------------------------------------------')

	def shutdown(self):

		self.showQueueInfo()
		self.close()
		self.dumpData()

