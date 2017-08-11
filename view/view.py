from datetime import datetime
from flask import render_template

from flask import Flask, request, redirect, url_for, flash
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename

import view.admin as admin
import os

basedir = os.path.abspath(".")
UPLOAD_FOLDER = os.path.join(basedir, "data")

def create_view_route(app):
	@app.route('/')
	def mainPageView():
		the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
		# return """
	 #    <h1>Hello Cared Design</h1>
	 #    <p>It is currently {time}.</p>
	 #    <p>AddHospital: http://127.0.0.1:5000/addHospital?hospital=NTU1</p>
	 #    """.format(time=the_time)
		return render_template('main.html', time=the_time)

	@app.route('/admin')   
	def adminView():
		return admin.hello()

	ALLOWED_EXTENSIONS = set(['csv'])
	def allowed_file(filename):
	    return '.' in filename and \
	           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
