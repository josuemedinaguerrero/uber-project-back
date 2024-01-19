from flask import Blueprint, request, jsonify
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle

users = Blueprint('users', __name__)

@users.route("/users")
def get_users():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT u.CEDULE, u.EMAIL, u.USERNAME FROM AVI_USERS u WHERE ROL = 1")
        available_times_db = cursor.fetchall()
        
        result = format_fields(available_times_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@users.route('/update-user', methods=["PUT"])
def register_user():
    try:
        connection, cursor = connection_db()
        
        data_user = {
            'cedule': request.form.get('CEDULE'),
            'email': request.form.get('EMAIL'),
            'username': request.form.get('USERNAME')
        }
        
        data_profile = {
            'cedule': request.form.get('CEDULE'),
            'payment_method': request.form.get('PAYMENT_METHOD')
        }
        
        cursor.execute("UPDATE AVI_USERS SET EMAIL = :email, USERNAME = :username WHERE CEDULE = :cedule", data_user)
        cursor.execute("UPDATE AVI_PROFILES SET PAYMENT_METHOD = :payment_method WHERE CEDULE = :cedule", data_profile)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'message': 'Usuario actualizado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
