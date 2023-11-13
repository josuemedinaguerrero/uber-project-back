from flask import Blueprint, jsonify
from helpers.format import format_fields
from db.connection import connection_db

import cx_Oracle

security_alerts = Blueprint('security_alerts', __name__)

@security_alerts.route("/security-alerts")
def get_security_alerts():
    try:
        connection, cursor = connection_db()
        
        cursor.execute("SELECT * FROM AVI_SECURITY_ALERTS")
        security_alerts_db = cursor.fetchall()
        
        result = format_fields(security_alerts_db, cursor)
        
        cursor.close()
        connection.close()

        return jsonify(result)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
