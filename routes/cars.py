from flask import Blueprint, request, send_file, jsonify
from helpers.format import format_obj
from db.connection import connection_db

import cx_Oracle
import os

cars = Blueprint('cars', __name__)

@cars.route('/car/image/<cedule>')
def get_image_car(cedule):
    try:
        image_path = f"./assets/cars/{cedule}.png"
        if not os.path.exists(image_path):
            return send_file(f"./assets/cars/default.png", mimetype='image/png')
        
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({ 'error': True, 'message': str(e) })
    
@cars.route('/car/<driver>')
def get_car(driver):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT * FROM AVI_CARS WHERE DRIVER = {driver}")
        car_exist = cursor.fetchone()
        
        
        if car_exist:
            result = format_obj(car_exist, cursor)
            
            cursor.close()
            connection.close()
            
            return jsonify({ 'error': False, 'data': result })
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'data': {} })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@cars.route('/upload-car', methods=["POST"])
def upload_car():
    try:
        connection, cursor = connection_db()
        
        image = request.files['image']
        if image:
            image.save(f"./assets/cars/{request.form.get('cedule')}.png")
            
        data = {
            'plate': request.form.get("plate"),
            'color': request.form.get("color"),
            'cedule': request.form.get("cedule"),
        }
        
        cursor.execute("INSERT INTO AVI_CARS (PLATE, COLOR, DRIVER) VALUES (:plate, :color, :cedule)", data)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'message': 'Vehículo guardado exitosamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
