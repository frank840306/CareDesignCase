# -*- coding: utf-8 -*-
from logManager import setupLogger
# TODO:
# create hospitalManager to maintain model from different hospital
from flask import Flask, request
from flask_appconfig import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import os, argparse, logging, time, atexit

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
	
	logger = logging.getLogger(__name__)
	# TODO:
	# Initial ML model class
	# TODO:
	# convert xlsx to csv
	# ref: https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python
	# TODO:
	# Every hospital should maintain their own data and model

	# Register training funtion executed once every day
	# TODO: 
	# change interval and filename
	scheduler = BackgroundScheduler()
	scheduler.start()
	scheduler.add_job(
		func=lambda: trainModel('input.csv'),
		trigger=IntervalTrigger(days=1),
		id='training_model',
		name='training model every day',
		replace_existing=True)
	atexit.register(lambda: scheduler.shutdown())


	logger.info('Initial Flask app')
	app = Flask(__name__)
	AppConfig(app, configfile)
	app.config['SECRET_KEY'] = 'devkey'
	app.config['RECAPTCHA_PUBLIC_KEY'] = '6Mfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

	@app.route('/feature')
	def getFeature():
		# TODO:
		# return the data of features in JSON format according to different hospital
		return 'features:'

	@app.route('/predict')
	def predict():
		logger.info	(request.args)
		# TODO:
		# 1. check current hospital
		# 2. parse the feature clicked by user
		# 3. feed the feature to the model and predict answer
		return 'predict'
	@app.route('/update')
	def update():
		# TODO:
		# update the csv file with current record
		return 'update'


	return app
if __name__ == '__main__':
	setupLogger()
	logger = logging.getLogger(__name__)
	logger.info('Initial logger')
	if args.mode == 'debug':
		logger.info('Running server as [ %s ] mode on [ %s : %d ]' % (args.mode, args.host, args.port))
		create_app().run(debug=False, host=args.host, port=args.port)
		