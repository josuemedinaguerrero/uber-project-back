from flask import Blueprint, request, jsonify
from db.connection import connection_db

import cx_Oracle
import hashlib

login = Blueprint('login', __name__)

@login.route('/login', methods=["POST"])
def register_user():
    try:
        connection, cursor = connection_db()
        
        data = {
            'password': hashlib.md5(request.form.get('password').encode()).hexdigest(),
            'cedule': request.form.get("cedule"),
        }
        
        cursor.execute(f"SELECT * FROM AVI_DRIVERS WHERE cedule = {request.form.get("cedule")}")
        
        driver_data = cursor.fetchone()
        
        result = None
        
        if driver_data:
            cursor.execute("SELECT * FROM AVI_DRIVERS WHERE cedule = :cedule AND password = :password", data)
            driver_db = cursor.fetchone()
            
            if driver_db:
                column_names = [desc[0] for desc in cursor.description]

                result = {}
                for i in range(len(column_names)):
                    if column_names[i] != 'PASSWORD':
                        result[column_names[i]] = driver_db[i]

                result['ROL'] = 'DRIVER'

                cursor.close()
                connection.close()
                
                return jsonify({ 'error': False, 'message': 'Inicio de sesión exitoso!', 'data': result })
            else:
                return jsonify({ 'error': True, 'message': 'Usuario o contraseña incorrecto!' })
        else:
            cursor.execute("""
                SELECT u.cedule, u.email, u.username, r.id, r.type
                FROM AVI_USERS u
                LEFT JOIN AVI_ROLES r
                ON u.rol = r.id 
                WHERE u.cedule = :cedule AND u.password = :password
            """, data)
            result = cursor.fetchone()
        
            cursor.close()
            connection.close()
            
            if result:
                data = {
                    'CEDULE': result[0],
                    'EMAIL': result[1],
                    'USERNAME': result[2],
                    'ROL_ID': result[3],
                    'ROL': result[4].strip()
                }
                return jsonify({ 'message': 'Inicio de sesión exitoso!', 'data': data })
            else:
                return jsonify({ 'error': True, 'message': 'Usuario o contraseña incorrecto!' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
