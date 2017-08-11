from flask import render_template
from flask import Flask, request, redirect, url_for, flash

import os

# def hello():

#     return "Hello World! Admin"

def hello(name=None):
	# return "Hello World! Admin"
	return render_template('hello.html', name='Admin')

