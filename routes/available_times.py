from flask import Blueprint, jsonify, request
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle

available_times = Blueprint('available_times', __name__)

@available_times.route("/available-times")
def get_security_alerts():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_AVAILABLE_TIMES")
        available_times_db = cursor.fetchall()
        
        result = format_fields(available_times_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
    
@available_times.route("/available-times", methods=["POST"])
def get_security_alerts():
    try:
        connection, cursor = connection_db()
        
        data = {
            'days': request.form.get('days'),
            'times': request.form.get('times'),
            'description': request.form.get('description')
        }
        
        cursor.execute("INSERT INTO AVI_AVAILABLE_TIMES (DAYS, TIMES, DESCRIPTION) VALUES (:days, :times, :description)", data)
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False, 'message': 'Tiempos disponibles añadidos correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
