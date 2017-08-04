from flask import render_template


# def hello():

#     return "Hello World! Admin"

def hello(name=None):
	return render_template('hello.html', name=name)