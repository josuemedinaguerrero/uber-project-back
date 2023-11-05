from flask import Blueprint, request, jsonify

import cx_Oracle

payment_methods = Blueprint('payment_methods', __name__)

@payment_methods.route('/payment_methods')
def register_user():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM AVI_PAYMENT_METHODS")
        payment_methods = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify([{ 'id': row[0], 'name': row[1] } for row in payment_methods])
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
