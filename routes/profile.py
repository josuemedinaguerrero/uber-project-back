from flask import Blueprint, request, jsonify

import cx_Oracle

profile = Blueprint('profile', __name__)

@profile.route('/create-profile', methods=["POST"])
def create_profile():
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
            'user_profile': request.form.get("user_profile"),
        }
        
        print(data)
        
        cursor.execute("INSERT INTO AVI_PROFILES (CEDULE, USER_PROFILE) VALUES (:cedule, :user_profile)", data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'message': 'Perfil creado exitosamente!' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@profile.route('/update-profile', methods=["PUT"])
def update_profile():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        data = {
            'cedule': request.form.get('cedule'),
            'payment_method': request.form.get('payment_method')
        }
        
        cursor.execute("UPDATE AVI_PROFILES SET payment_method = :payment_method WHERE cedule = :cedule", data)
        connection.commit()
        
        # cursor.execute("SELECT * FROM AVI_PROFILES WHERE CEDULE = :cedule", data)
        # updated_profile = cursor.findone()
        
        # print(updated_profile)
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'message': 'Metodo de pago actualizado correctamente!!!' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
