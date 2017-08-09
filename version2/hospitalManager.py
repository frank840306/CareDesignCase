from utils import *
import logging, time, shutil

class HospitalManager:
    def __init__(
        self,
        mdl_dir=default_path['MDL_DIR'],
        fileNumPerHospital=default_config['FILE_NUM_PER_HOSPITAL',
        modelNumPerFile=default_config['MODEL_NUM_PER_FILE'],
        trainingMethod=default_config['TRAINING_METHOD']
        ):
        self.logger = logging.getLogget(__name__)
        self.mdl_dir = mdl_dir
    def getInputFeature(self, hospitalName, filename):
        return {}
    def getOutputFeature(self, hospitalName, filename):
        return {}
    def getHospitalList(self):
        return []
    def getFileList(self, hospitalName):
        return []
    def getModelList(self, hospitalName, filename):
        return []
    def predictFocut(self, hospitalName, filename):
        return []
    def trainModel(self, 
    def loadData(self):
        return 
    def dumpData(self):
        return
