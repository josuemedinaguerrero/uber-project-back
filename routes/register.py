from flask import Blueprint, request, jsonify
from db.connection import connection_db

import cx_Oracle
import hashlib

register = Blueprint('register', __name__)

@register.route('/register', methods=["POST"])
def register_user():
    try:
        connection, cursor = connection_db()
        
        cedule = request.form.get("cedule")
        
        data = {
            'cedule': cedule,
            'password': hashlib.md5(request.form.get('password').encode()).hexdigest(),
            'email': request.form.get("email"),
            'username': request.form.get("username"),
            'rol': request.form.get('rol') if request.form.get('rol') is not None else 1
        }
        
        cursor.execute("INSERT INTO AVI_USERS (CEDULE, PASSWORD, EMAIL, USERNAME, ROL) VALUES (:cedule, :password, :email, :username, :rol)", data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'message': 'Usuario creado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(error.message)
        return jsonify({ 'error': True, 'message': error.message })
