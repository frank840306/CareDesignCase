from utils import *
from casemodel import kerasModel # ML model from Kevin

class HospitalManager:
	def __init__(
		self, 
		data_dir=default_path['DATA_DIR'],
		mdl_dir=default_path['MDL_DIR'],
		hospitalJsonFile=default_path['HOSPITALJSON'],
		hospital2modelJsonFile=default_path['HOSPITAL2MODELJSON']
		):
		self.data_dir = data_dir
		self.mdl_dir = mdl_dir
		self.hospitalJsonFile = hospitalJsonFile
		self.hospital2modelJsonFile = hospital2modelJsonFile
		self.hospitalList, self.hospital2model = self.loadData()

	def loadData(self):
		if os.path.exists(self.hospitalJsonFile):
			hospitalListJson = readJson(self.hospitalJsonFile)
			hospitalList = json.loads(hospitalListJson)
		else:
			hospitalList = []
		if os.path.exists(self.hospital2modelJsonFile):
			hospital2modelJson = readJson(self.hospital2modelJsonFile)
			hospital2model = json.loads(hospital2modelJson)
		else:
			hospital2model = {}
		return hospitalList, hospital2model
			
	def dumpData(self):
		if len(self.hospitalList) == 0:
			pass
		else:
			hospitalListJson = json.dumps(self.hospitalList)
			writeJson(hospitalListJson, self.hospitalJsonFile)
		if len(self.modelList) == 0:
			pass
		else:
			hospital2modelJson = json.dumps(self.hospital2model)
			writeJson(hospital2modelJson, self.hospital2modelJsonFile)
		return

	def shutdown(self):
		# before closing server

		self.dumpData()
		return

	def addHospital(self, hospital):
		if hospital not in self.hospitalList:
			


			self.hospitalList.append(hospital)

	def removeHospital(self):
		pass
	def addModel(self, hospital, model):
		
		pass
	def getCurrentModel(self):
		pass
	def updateModel(self):
		for hospital in self.hospitalList:
			modelUsed = hospital + '_' + time.strftime('%Y%m%d')
			if len(self.hospital2model) == 0 or self.hospital2model[hospital][-1]:
				# 
				pass
		pass
