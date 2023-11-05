from flask import Blueprint, request, jsonify

import cx_Oracle
import hashlib

register = Blueprint('register', __name__)

@register.route('/register', methods=["POST"])
def register_user():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        data = {
            'cedule': request.form.get("cedule"),
            'password': hashlib.md5(request.form.get('password').encode()).hexdigest(),
            'email': request.form.get("email"),
            'username': request.form.get("username"),
            'rol': request.form.get('rol') if request.form.get('rol') is not None else 1
        }
        
        print(data)
        
        cursor.execute("INSERT INTO AVI_USERS (CEDULE, PASSWORD, EMAIL, USERNAME, ROL) VALUES (:cedule, :password, :email, :username, :rol)", data)
        connection.commit()
        
        cursor.execute("INSERT INTO AVI_PROFILES (CEDULE, USER_PROFILE) VALUES (:cedule, :cedule)", data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'message': 'Usuario creado exitosamente correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
