from flask import Blueprint, jsonify, request
from helpers.format import format_fields_with_clob
from db.connection import connection_db

import cx_Oracle

security_alerts = Blueprint('security_alerts', __name__)

@security_alerts.route("/security-alerts")
def get_security_alerts():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_SECURITY_ALERTS")
        security_alerts_db = cursor.fetchall()
        
        result = format_fields_with_clob(security_alerts_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })

@security_alerts.route("/security-alerts", methods=["POST"])
def update_rate_driver():
    try:
        connection, cursor = connection_db()
         
        message = request.form.get('security_alert')
         
        cursor.execute(f"INSERT INTO AVI_SECURITY_ALERTS (ALERT_DESCRIPTION) VALUES ('{message}')")
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({ 'error': False, 'message': 'Alerta añadida correctamente' })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
