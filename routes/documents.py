from flask import Blueprint, send_from_directory, request, jsonify
from werkzeug.utils import secure_filename
from db.connection import connection_db

import cx_Oracle
import os

documents = Blueprint('documents', __name__)

@documents.route("/driver-documents", methods=["PUT"])
def upload_documents():
    try:
        connection, cursor = connection_db()
        
        cedule_file = request.files.get('cedule')
        registration_file = request.files.get('registration')
        license_file = request.files.get('license')
        cedule = request.form.get("cedule")
            
        print(cedule)        
       
        if not cedule_file or not registration_file or not license_file:
            return jsonify({ 'error': True, 'message': 'Todos los archivos son requeridos' })
    
        cedule_filename = secure_filename(f"{cedule}_cedule.pdf")
        registration_filename = secure_filename(f"{cedule}_registration.pdf")
        license_filename = secure_filename(f"{cedule}_license.pdf")
        
        cedule_file.save(os.path.join('documents', cedule_filename))
        registration_file.save(os.path.join('documents', registration_filename))
        license_file.save(os.path.join('documents', license_filename))
        
        cursor.execute(f"UPDATE AVI_DRIVERS SET STATE_DOCUMENTS = 3 WHERE CEDULE = {cedule}")
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'message': 'Documentos ingresados correctamente. Le notificaremos a uno de nuestros administradores para que los verifique.' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@documents.route("/documents/cedule/<cedule>")
def get_documents_cedule(cedule):
    try:
        document_folder = 'documents'
        return send_from_directory(document_folder, f'{cedule}_cedule.pdf')
    except Exception as e:
        print("ERROR: ", str(e))
        return jsonify({ 'error': True, 'message': str(e) })

@documents.route("/documents/registration/<cedule>")
def get_documents_registration(cedule):
    try:
        document_folder = 'documents'
        return send_from_directory(document_folder, f'{cedule}_registration.pdf')
    except Exception as e:
        print("ERROR: ", str(e))
        return jsonify({ 'error': True, 'message': str(e) })

@documents.route("/documents/license/<cedule>")
def get_documents_license(cedule):
    try:
        document_folder = 'documents'
        return send_from_directory(document_folder, f'{cedule}_license.pdf')
    except Exception as e:
        print("ERROR: ", str(e))
        return jsonify({ 'error': True, 'message': str(e) })
