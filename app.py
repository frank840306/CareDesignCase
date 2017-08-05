from flask import Flask
from datetime import datetime
app = Flask(__name__)


import view.admin as admin

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello CareDesign Model</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/admin')
def route_admin():
	return admin.hello()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

