from flask import Flask
from flask_cors import CORS

from routes.register import register
from routes.login import login
from routes.drivers import drivers
from routes.payment_methods import payment_methods
from routes.profile import profile 
from routes.documents import documents 
from routes.users import users 
from routes.security_alerts import security_alerts
from routes.rate_drivers import rate_drivers
from routes.completed_races import completed_races
from routes.available_times import available_times
from routes.routes import routes
from routes.cancellation_route import cancellation_route
from routes.reviews import reviews
from routes.featured_destinations import featured_destinations
from routes.cars import cars

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
app.register_blueprint(users)
app.register_blueprint(security_alerts)
app.register_blueprint(rate_drivers)
app.register_blueprint(completed_races)
app.register_blueprint(available_times)
app.register_blueprint(routes)
app.register_blueprint(cancellation_route)
app.register_blueprint(reviews)
app.register_blueprint(cars)
app.register_blueprint(featured_destinations)
