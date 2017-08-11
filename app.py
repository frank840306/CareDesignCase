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
from flask import render_template
from flask import Flask, request, redirect, url_for, flash
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename

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

# Usgae:
# /predict?hospital=NTU&filename=example_31_14 (used the newest model)
# /predict?hospital=NTU&filename=example_31_14&time=-3 (specified model)
# time: the # model counted backward, default = -1 (the newest model)
# 		ex: time = -3, means the third model counted from the end of list. 
@app.route('/predict')
def predict():
	if 'hospital' in request.args and 'filename' in request.args:
		hospital = str(request.args['hospital'])
		filename = str(request.args['filename'])
		data = [0] * (len(hm.getInputFeature(hospital, filename)['Bool']) + len(hm.getInputFeature(hospital, filename)['Float']))
		for args in request.args:
			if args != 'hospital' and args != 'filename':
				data[int(args[1:])] = float(request.args[args])
		if 'time' in request.args:
			time = int(request.args['time'])
			pred_focus = hm.predictFocus(data, hospital, filename, time)
		else:
			pred_focus = hm.predictFocus(data, hospital, filename)
	else:
		pred_focus = []
	return json.dumps(pred_focus, indent=4, ensure_ascii=False)
	
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

# Usgae:
# /addHospital?hospital=NTU
@app.route('/addHospital')
def addHospital():
	if 'hospital' in request.args:
		hospital = str(request.args['hospital'])
		return hm.addHospital(hospital)
	else:
		return 'Please give a hospital name'

# Usgae:
# /removeHospital?hospital=NTU
@app.route('/removeHospital')
def removeHospital():
	if 'hospital' in request.args:
		hospital = str(request.args['hospital'])
		return hm.removeHospital(hospital)
	else:
		return 'Please give a hospital name'

# Usgae:
# /addFile?hospital=NTU&filename=example_31_14
# /addFile?hospital=NTU&filename=example_31_14&method=rf

@app.route('/addFile')
def addFile():
	if 'hospital' in request.args and 'filename' in request.args:
		hospital = str(request.args['hospital'])
		filename = str(request.args['filename'])
		if 'method' in request.args:
			method = str(request.args['method'])
			return hm.addFile(hospital, filename, method)
		else:
			return hm.addFile(hospital, filename)	
	elif 'hospital' in request.args:
		return 'Please give a CSV file name'
	elif 'filename' in request.args:
		return 'Please give a hospital name'
	else:
		return 'Please give a CSV file and hospital name'
			
# Usage:
# removeFile?hospital=NTU&filename=example_31_14
@app.route('/removeFile')
def removeFile():
	if 'hospital' in request.args and 'filename' in request.args:
		hospital = str(request.args['hospital'])
		filename = str(request.args['filename'])
		return hm.removeFile(hospital, filename)
	elif 'hospital' in request.args:
		return 'Please give a CSV file name'
	elif 'filename' in request.args:
		return 'Please give a hospital name'
	else:
		return 'Please give a CSV file and hospital name'

@app.route('/')
def mainPageView():
	the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
	# return """
	# <h1>Hello Cared Design</h1>
	# <p>It is currently {time}.</p>
	# <p>AddHospital: http://127.0.0.1:5000/addHospital?hospital=NTU1</p>
	# """.format(time=the_time)
	return render_template('main.html', time=the_time)


@app.route('/admin')   
def adminView():
	return admin.hello()

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

basedir = os.path.abspath(".")
UPLOAD_FOLDER = os.path.join(basedir, "data")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'
@app.route('/admin/upload', methods=['GET', 'POST'])
def uploadView():
	if request.method == 'POST':
	# check if the post request has the file part
		if 'file' not in request.files:
		    flash('No file part')
		    return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
		    flash('No selected file')
		    return redirect(request.url)
		if file and allowed_file(file.filename):
		    filename = secure_filename(file.filename)
		    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		    return redirect(url_for('upload',
		                            filename=filename))
	return render_template('upload.html')		


@app.route('/uploads/<filename>')
def upload(filename):
	
	return 'file uploaded: '+str(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['UPLOAD_FOLDER']
# })

signal.signal(signal.SIGINT, hm.shutdown)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)