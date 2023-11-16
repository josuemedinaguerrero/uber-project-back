from flask import Blueprint, jsonify, request
from db.connection import connection_db

import cx_Oracle
import random

rate_drivers = Blueprint('rate_drivers', __name__)

@rate_drivers.route("/rate-drivers/<cedule>")
def get_rate_drivers(cedule):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT * FROM AVI_RATE_DRIVERS WHERE DRIVER = {cedule}")
        available_times_db = cursor.fetchone()
        
        cursor.close()
        connection.close()

        return jsonify({ 'data': available_times_db[0] })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
    
@rate_drivers.route("/rate-driver/<cedule>", methods=["PUT"])
def update_rate_driver(cedule):
    try:
        connection, cursor = connection_db()
         
        cursor.execute(f"SELECT r.rate FROM AVI_RATE_DRIVERS r WHERE DRIVER = {cedule}")
        rate_driver_db = cursor.fetchone()
        
        new_rate = int((int(rate_driver_db[0]) + int(request.form.get('rate'))) / 2)
        
        data_review = {
            'id': int(''.join([str(random.randint(0, 9)) for _ in range(15)])),
            'comment_review': request.form.get('comment_review'),
            'route_id': request.form.get('route_id')
        }
        
        cursor.execute(f"UPDATE AVI_ROUTES SET CALIFICATION = {request.form.get('rate')} WHERE ID = {request.form.get('route_id')}")
        cursor.execute(f"UPDATE AVI_RATE_DRIVERS SET RATE = {new_rate} WHERE DRIVER = '{cedule}'")
        cursor.execute("INSERT INTO AVI_REVIEWS (ID, COMMENT_REVIEW, ROUTE) VALUES (:id, :comment_review, :route_id)", data_review)
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
