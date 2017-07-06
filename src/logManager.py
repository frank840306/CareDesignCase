import logging, logging.config, os
from utils import *

def setupLogger(
	default_path='config/logging.json', 
	default_level=logging.INFO
	):
	if os.path.exists(default_path):
		config = readJson(default_path)
		logging.config.dictConfig(config)
	else:
		logging.basicConfig(level=default_level)	