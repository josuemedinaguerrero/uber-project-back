from flask import Blueprint, jsonify, request
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle
import random

cancellation_route = Blueprint('cancellation_route', __name__)
    
@cancellation_route.route("/cancellation-route", methods=["POST"])
def create_available_time():
    try:
        connection, cursor = connection_db()
        
        id = int(''.join([str(random.randint(0, 9)) for _ in range(15)]))
        
        data = {
            'id': id,
            'id_route': request.form.get('id_route'),
            'comment_cancellation': request.form.get('comment_cancellation'),
        }
        
        cursor.execute(f"UPDATE AVI_ROUTES SET STATUS = 0 WHERE ID = {request.form.get('id_route')}")
        cursor.execute("INSERT INTO AVI_CANCELLATIONS (ID, COMMENT_CANCELLATION, ROUTE) VALUES (:id, :comment_cancellation, :id_route)", data)
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False, 'message': 'Ruta cancelada correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
