from flask import Blueprint, request, jsonify

import cx_Oracle

users = Blueprint('users', __name__)

@users.route('/update-user', methods=["PUT"])
def register_user():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
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
