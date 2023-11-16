from flask import Blueprint, jsonify, request
from helpers.format import format_obj
from db.connection import connection_db

import cx_Oracle

reviews = Blueprint('reviews', __name__)

@reviews.route("/review/<id_route>")
def get_completed_races(id_route):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"SELECT r.route FROM AVI_REVIEWS r WHERE ROUTE = {id_route}")
        review = cursor.fetchone()
        
        result = {}
        if review:
            result = format_obj(review, cursor)
        
        cursor.close()
        connection.close()

        return jsonify({  'error': False, 'data': result })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
