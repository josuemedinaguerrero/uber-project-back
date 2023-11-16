from flask import Blueprint, request, jsonify
from db.connection import connection_db

import cx_Oracle

profile = Blueprint('profile', __name__)

@profile.route('/create-profile', methods=["POST"])
def create_profile():
    try:
        connection, cursor = connection_db()
        
        cedule = request.form.get("cedule")
        
        cursor.execute(f"INSERT INTO AVI_PROFILES (CEDULE, USER_PROFILE) VALUES ('{cedule}', '{cedule}')")
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'message': 'Perfil creado exitosamente!' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@profile.route('/profile/<cedule>')
def get_profile(cedule):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT * FROM AVI_PROFILES WHERE cedule = {cedule}")
        profile_db = cursor.fetchone()
            
        if profile_db:
            column_names = [desc[0] for desc in cursor.description]

            result = {}
            for i in range(len(column_names)):
                result[column_names[i]] = profile_db[i]

            cursor.close()
            connection.close()
                
            return jsonify({ 'error': False, 'data': result })
        
        cursor.close()
        connection.close()
  
        return jsonify({ 'error': True, 'message': 'No se pudo obtener el perfil' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
