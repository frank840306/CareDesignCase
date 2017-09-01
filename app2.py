from src.server import *
from view.view import *
from flask import Flask

app = Flask(__name__)

setupLogger()
logger = logging.getLogger(__name__)
logger.info('Initial logger')

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Mfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

create_app(app)
create_view_route(app)



# for test only view, no ML model

# from view.view import *
# from flask import Flask
# from flask import Flask, request
# app = Flask(__name__)
# create_view_route(app)