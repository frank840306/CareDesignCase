# -*- coding: utf-8 -*-
from logManager import setupLogger

from flask import Flask
from flask_appconfig import AppConfig

import os, argparse, logging

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

def create_app(configfile=None):
	
	logger = logging.getLogger(__name__)

	logger.info('Initial Flask app')
	app = Flask(__name__)
	AppConfig(app, configfile)
	app.config['SECRET_KEY'] = 'devkey'
	app.config['RECAPTCHA_PUBLIC_KEY'] = '6Mfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

	@app.route('/feature')
	def getFeature():
		return 'features:'

	@app.route('/predict')
	def predict():
		return 'predict'

	return app
if __name__ == '__main__':
	setupLogger()
	logger = logging.getLogger(__name__)
	logger.info('Initial logger')
	if args.mode == 'debug':
		logger.info('Running server as [ %s ] mode on [ %s : %d ]' % (args.mode, args.host, args.port))
		create_app().run(debug=False, host=args.host, port=args.port)
		