# -*- coding: utf-8 -*-
from utils import *
from logManager import setupLogger
from casemodel import kerasModel 
from rfModel import RandomForestModel
# TODO:
# create hospitalManager to maintain model from different hospital
from hospitalManager import HospitalManager
from flask import Flask, request
from flask_appconfig import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import os, argparse, logging, time, atexit, json, time, signal, re

parser = argparse.ArgumentParser(
	prog='PROG',
	formatter_class=argparse.RawDescriptionHelpFormatter, 
	description='''
		Care Design Server
		--------------------------

	'''
	)
parser.add_argument('-m', '--mode', help='debug or deploy', default='debug')
parser.add_argument('-n', '--host', help='host name', default='127.0.0.1')
parser.add_argument('-p', '--port', help='port number', type=int, default=5000)
args = parser.parse_args()

def trainModel(filename):
	print ('XDDD : ' + filename)
	return

def create_app(configfile=None):
	root_dir = '.'
	data_dir = os.path.join(root_dir, 'data')
	mdl_dir = os.path.join(root_dir, 'mdl')

	logger = logging.getLogger(__name__)
	# TODO:
	# Initial ML model class
	hospital = 'example_31_14'
	date = time.strftime('%Y%m%d')
	modelName = hospital + '_' + date

	# xlsxFile = 'example_31_14.xlsx'
	xlsxFile = hospital + '.xlsx'
	csvFile = hospital + '.csv'
	# modelName = xlsxFile.split('.', 1)[0]
	km = kerasModel(hospital)
	rfm = RandomForestModel(hospital)
	hm = HospitalManager()
	# update model
	hm.updateModel()
	# TODO:
	# add constraint
	# if (no model), then train a new model
	# else load existing one
	# convert xlsx to csv
	rfm.trainModel(os.path.join(data_dir, hospital + '.csv'), 37, 14)
		
	if hospital + '_model.h5' not in os.listdir(mdl_dir):
		logger.info('Model does not exist --> train a new one')
		if hospital + '.csv' not in os.listdir(data_dir):
			# convert xlsx to csv
			logger.info('CSV formated file does not exist --> create CSV')
			XLSX2CSV(os.path.join(data_dir, xlsxFile))
		else:
			# do nothing
			logger.info('CSV exists --> do nothing')
			pass
		# train model
		logger.info('Training Keras model named [ %s ]' % (hospital + '.csv'))
		km.trainModel(os.path.join(data_dir, hospital + '.csv'), 37, 14)
		
	else:
		# use current model
		logger.info('Model exists --> do nothing')
		pass
	features = open(os.path.join(data_dir, hospital + '.csv')).readline()[:-1].split(',')[:37]
	for idx in range(len(features)):
		features[idx] = re.sub(r'IN\d+', '', features[idx])
	results = open(os.path.join(data_dir, hospital + '.csv')).readline()[:-1].split(',')[37:]
	for idx in range(len(results)):
		results[idx] = re.sub(r'OUT\d+', '', results[idx])
		# print(results[idx])
	# logger.info(features)
	# logger.info(results)

	# ref: https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python
	# TODO:
	# Every hospital should maintain their own data and model

	# Register training funtion executed once every day
	# TODO: 
	# change interval and filename
	# scheduler = BackgroundScheduler()
	# scheduler.start()
	# scheduler.add_job(
	# 	func=lambda: trainModel('input.csv'),
	# 	trigger=IntervalTrigger(days=1),
	# 	id='training_model',
	# 	name='training model every day',
	# 	replace_existing=True)
	# atexit.register(lambda: scheduler.shutdown())


	logger.info('Initial Flask app')
	app = Flask(__name__)
	AppConfig(app, configfile)
	app.config['SECRET_KEY'] = 'devkey'
	app.config['RECAPTCHA_PUBLIC_KEY'] = '6Mfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

	@app.route('/feature')
	def getFeature():
		# TODO:
		# return the data of features in JSON format according to different hospital
		return json.dumps(features, indent=4, ensure_ascii=False)

	@app.route('/predict')
	def predict():
		logger.info	(request.args)
		# TODO:
		# 1. check current hospital
		cur_hospital = str(request.args['hospital'])
		cur_features = [0] * 37
		for args in request.args:
			if args != 'hospital':
				cur_features[int(args[1:])] = 1
		logger.info('Features from client:')
		logger.info([cur_features])
		# 2. parse the feature clicked by user
		# 3. feed the feature to the model and predict answer
		pred_idx = km.predictFocus([cur_features])
		# pred_idx = rfm.predictFocus(cur_features)
		
		logger.info('Predict result idx:')
		logger.info(pred_idx)
		pred = [results[val] for val in pred_idx]
		return json.dumps(pred, indent=4, ensure_ascii=False)
	@app.route('/update')
	def update():
		# TODO:
		# update the csv file with current record
		return 'update'

	# signal.signal(signal.SIGINT, hm.shutdown)

	return app
if __name__ == '__main__':
	setupLogger()
	logger = logging.getLogger(__name__)
	logger.info('Initial logger')
	if args.mode == 'debug':
		logger.info('Running server as [ %s ] mode on [ %s : %d ]' % (args.mode, args.host, args.port))
		create_app().run(debug=True, host=args.host, port=args.port)
		