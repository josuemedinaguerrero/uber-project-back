from flask import Flask
from flask_cors import CORS

from routes.register import register
from routes.login import login
from routes.drivers import drivers
from routes.payment_methods import payment_methods
from routes.profile import profile 
from routes.documents import documents 

import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(app.config['UPLOAD_FOLDER'])

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(drivers)
app.register_blueprint(payment_methods)
app.register_blueprint(profile)
app.register_blueprint(documents)
