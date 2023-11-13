from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from helpers.send_email import send_email
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle
import hashlib
import os

drivers = Blueprint('drivers', __name__)

@drivers.route("/drivers")
def get_drivers():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_DRIVERS")
        drivers_db = cursor.fetchall()
        
        result = format_fields(drivers_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@drivers.route('/create-driver', methods=["POST"])
def create_driver():
    try:
        connection, cursor = connection_db()
        
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
            'password': hashlib.md5(request.form.get('password').encode()).hexdigest(),
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
        connection, cursor = connection_db()
        
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
        connection, cursor = connection_db()
        
        cedule = request.form.get('cedule')
        destination = request.form.get('destination')
        body = request.form.get("body")
        subject = request.form.get("subject")
        verified_documents = request.form.get("verified_documents")
        
        send_email(destination, body, subject)
        
        cursor.execute(f"UPDATE AVI_DRIVERS SET VERIFIED_DOCUMENTS = {verified_documents} WHERE CEDULE = {cedule}")
        connection.commit()
        
        cursor.close()
        connection.close()
            
        return jsonify({ 'error': False, 'message': 'Mensaje enviado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
