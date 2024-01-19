from flask import Blueprint, send_file, jsonify
from helpers.format import format_fields_with_clob
from db.connection import connection_db

import cx_Oracle

featured_destinations = Blueprint('featured_destinations', __name__)

@featured_destinations.route("/featured-destinations")
def get_security_alerts():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_FEATURED_DESTINATIONS")
        available_times_db = cursor.fetchall()
        
        result = format_fields_with_clob(available_times_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@featured_destinations.route('/featured-destinations/image/<name>')
def get_image_car(name):
    try:
        image_path = f"./assets/featured_destinations/{name}"
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({ 'error': True, 'message': str(e) })
