from src.server import *
from view.view import *
from flask import Flask

setupLogger()
logger = logging.getLogger(__name__)
logger.info('Initial logger')

app = create_app()
create_view_route(app)



# for test only view, no ML model

# from view.view import *
# from flask import Flask
# from flask import Flask, request
# app = Flask(__name__)
# create_view_route(app)