from flask import Blueprint, jsonify, request
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle

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
        
        cursor.execute(f"UPDATE AVI_RATE_DRIVERS SET RATE = {new_rate} WHERE DRIVER = '{cedule}'")
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False, 'message': 'Tiempos disponibles añadidos correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
