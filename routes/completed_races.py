from flask import Blueprint, jsonify, request
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle

completed_races = Blueprint('completed_races', __name__)

@completed_races.route("/completed-races/<cedule>")
def get_completed_races(cedule):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT * FROM AVI_COMPLETED_RACES WHERE DRIVER = {cedule}")
        completed_races_db = cursor.fetchone()
        
        cursor.close()
        connection.close()

        return jsonify({ 'data': completed_races_db[1] })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
    
@completed_races.route("/completed-races/<cedule>", methods=["PUT"])
def update_rate_driver(cedule):
    try:
        connection, cursor = connection_db()
         
        cursor.execute(f"SELECT r.quantity FROM AVI_COMPLETED_RACES r WHERE DRIVER = {cedule}")
        rate_driver_db = cursor.fetchone()
        
        if not rate_driver_db:
            cursor.execute(f"INSERT INTO AVI_COMPLETED_RACES (DRIVER, QUANTITY) VALUES ('{cedule}', 1)")
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({ 'error': False })
        
        cursor.execute(f"UPDATE AVI_COMPLETED_RACES SET QUANTITY = {int(int(rate_driver_db[0])) + 1} WHERE DRIVER = '{cedule}'")
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
