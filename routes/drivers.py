from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from helpers.send_email import send_email

import cx_Oracle
import os

drivers = Blueprint('drivers', __name__)

@drivers.route("/drivers")
def get_drivers():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM AVI_DRIVERS")
        drivers_db = cursor.fetchall()
        
        column_names = [desc[0] for desc in cursor.description]
        
        cursor.close()
        connection.close()

        result = []
        for row in drivers_db:
            row_dict = {}
            for i in range(len(row)):
                row_dict[column_names[i]] = row[i]
            result.append(row_dict)

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@drivers.route('/create-driver', methods=["POST"])
def create_driver():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        image = request.files['image']
        if image:
            image.save(f"./assets/images/profile_{request.form.get('cedule')}.png")
            
        birthdate = datetime.fromisoformat(request.form.get('birthdate'))
        
        data = {
            'cedule': request.form.get("cedule"),
            'address': request.form.get("address"),
            'names': request.form.get("names"),
            'surnames': request.form.get("surnames"),
            'city': request.form.get("city"),
            'email': request.form.get("email"),
            'phone': request.form.get("phone"),
            'password': birthdate.strftime("%Y-%m-%d"),
            'birthdate': birthdate,
        }
        
        print(data)
        
        cursor.execute("""
            INSERT INTO AVI_DRIVERS (CEDULE, ADDRESS, NAMES, SURNAMES, CITY, EMAIL, PHONE, PASSWORD, BIRTHDATE)
            VALUES (:cedule, :address, :names, :surnames, :city, :email, :phone, :password, :birthdate)
        """, data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'message': 'Conductor creado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
    
@drivers.route("/driver-documents", methods=["PUT"])
def upload_documents():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cedule_file = request.files.get('cedule')
        registration_file = request.files.get('registration')
        license_file = request.files.get('license')
        cedule = request.form.get("cedule")
       
        if not cedule_file or not registration_file or not license_file:
            return jsonify({ 'error': True, 'message': 'Todos los archivos son requeridos' })
    
        cedule_filename = secure_filename(f"{cedule}_cedule.pdf")
        registration_filename = secure_filename(f"{cedule}_registration.pdf")
        license_filename = secure_filename(f"{cedule}_license.pdf")
        
        cedule_file.save(os.path.join('documents', cedule_filename))
        registration_file.save(os.path.join('documents', registration_filename))
        license_file.save(os.path.join('documents', license_filename))
        
        cursor = connection.cursor()
        
        cursor.execute(f"UPDATE AVI_DRIVERS SET DOCUMENTS = 1 WHERE CEDULE = {cedule}")
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'message': 'Documentos ingresados correctamente. Le notificaremos a uno de nuestros administradores para que los verifique.' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@drivers.route('/verificate-documents', methods=["PUT"])
def verificate_documents_driver():
    try:
        connection = cx_Oracle.connect(
            user='system',
            password='123456',
            dsn='localhost:1521/XEPDB1',
            encoding='UTF-8'
        )
        
        cursor = connection.cursor()
        
        cedule = request.form.get('cedule')
        destination = request.form.get('destination')
        body = request.form.get("body")
        subject = request.form.get("subject")
        verified_documents = request.form.get("verified_documents")
        
        send_email(destination, body, subject)
        
        if verified_documents == 'true':
            cursor.execute(f"UPDATE AVI_DRIVERS SET VERIFIED_DOCUMENTS = 1 WHERE CEDULE = {cedule}")
            connection.commit()
        
            cursor.close()
            connection.close()
            
            return jsonify({ 'error': False, 'message': 'Conductor verificado correctamente' })
        else:
            return jsonify({ 'error': False, 'message': '' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
