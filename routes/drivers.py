from flask import Blueprint, request, jsonify
from datetime import datetime
from helpers.send_email import send_email
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle
import hashlib

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
        
        cursor.execute(f"UPDATE AVI_DRIVERS SET STATE_DOCUMENTS = {verified_documents} WHERE CEDULE = {cedule}")
        connection.commit()
        
        cursor.close()
        connection.close()
            
        return jsonify({ 'error': False, 'message': 'Mensaje enviado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@drivers.route('/change-status/<cedule>', methods=["PUT"])
def change_status(cedule):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT * FROM AVI_DRIVERS WHERE cedule = {cedule}")
        driver_data = cursor.fetchone()
        
        new_status = 1 if driver_data[9] == 0 else 0
        body = f"Su usuario ha sido {"bloqueado" if new_status == 0 else "desbloqueado"}"
        
        send_email(driver_data[5], body, "Estado del conductor")
        
        cursor.execute(f"UPDATE AVI_DRIVERS SET STATUS = {new_status} WHERE CEDULE = {cedule}")
        connection.commit()
        
        cursor.close()
        connection.close()
            
        return jsonify({ 'error': False, 'message': 'Estado actualizado correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
