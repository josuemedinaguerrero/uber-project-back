from flask import Blueprint, jsonify
from db.connection import connection_db

import cx_Oracle

payment_methods = Blueprint('payment_methods', __name__)

@payment_methods.route('/payment-methods')
def register_user():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_PAYMENT_METHODS")
        payment_methods = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify([{ 'id': row[0], 'name': row[1] } for row in payment_methods])
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
