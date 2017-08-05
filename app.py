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


import os, argparse, logging, atexit, json, time, signal, re

from flask import Flask
from datetime import datetime

import view.admin as admin

root_dir = '.'
data_dir = os.path.join(root_dir, 'data')
mdl_dir = os.path.join(root_dir, 'mdl')

logger = logging.getLogger(__name__)
# TODO:
# Initial ML model class
hospital = 'NTU_example_31_14_20170715'
hm = HospitalManager()
# update model
hm.updateModel()

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

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/admin')
def route_admin():
	# return 'hello admin'
	return admin.hello()

# Usgae:
# /feature?hospital=NTU&filename=example_31_14
@app.route('/feature')
def getFeature():
	# TODO:
	# return the data of features in JSON format according to different hospital
	if 'hospital' in request.args and 'filename' in request.args:
		hospital = str(request.args['hospital'])
		filename = str(request.args['filename'])
		features = hm.getInputFeature(hospital, filename)
	else:
		features = {}
	return json.dumps(features, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)