from flask import Blueprint, request, jsonify
from db.connection import connection_db
from helpers.format import format_obj, format_fields

import cx_Oracle
import random
import datetime

routes = Blueprint('routes', __name__)

@routes.route('/routes/<cedule>')
def get_routes_user(cedule):
    try:
        connection, cursor = connection_db()
        
        cursor.execute(f"""
            SELECT d.cedule, d.email, c.plate, c.color, r.id as ID_ROUTE, d.names, d.surnames, r.time as TIME_LIMIT, d.phone FROM AVI_ROUTES r
                INNER JOIN AVI_DRIVERS d
                ON r.driver = d.cedule
                INNER JOIN AVI_CARS c
                ON c.driver = d.cedule
                WHERE r.user_cedule = {cedule} AND c.status = 1 AND d.status = 1 AND r.status = 1
        """)
        routes_user = cursor.fetchall()
        
        result = format_fields(routes_user, cursor)
        
        cursor.close()
        connection.close()
        
        return jsonify({ 'error': False, 'data': result })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(error.message)
        return jsonify({ 'error': True, 'message': error.message })
    
@routes.route('/create-route', methods=["POST"])
def create_route():
    try:
        connection, cursor = connection_db()
        
        id_geolocation = int(''.join([str(random.randint(0, 9)) for _ in range(15)]))
        id_route = int(''.join([str(random.randint(0, 9)) for _ in range(15)]))
        cedule = request.form.get('cedule')
        
        cursor.execute("""
            SELECT c.color, c.plate, d.phone, d.cedule, d.email, d.names, d.surnames FROM AVI_CARS C
                INNER JOIN AVI_DRIVERS D
                ON C.DRIVER = D.CEDULE
                WHERE D.STATE_DOCUMENTS = 1 AND D.STATUS = 1
        """)
        drivers_availables = cursor.fetchall()
        
        result = {}
        
        if drivers_availables:
            selected_car = random.choice(drivers_availables)
            
            data_geo = {
                'id_geo': id_geolocation,
                'start_latitude': request.form.get('start_latitude'),
                'start_longitude': request.form.get('start_longitude'),
                'end_latitude': request.form.get('end_latitude'),
                'end_longitude': request.form.get('end_longitude'),
            }
            
            time = datetime.datetime.strptime(request.form.get('time'), '%Y-%m-%dT%H:%M:%S.%fZ')
            
            data = {
                'id_geo': id_geolocation,
                'cedule': cedule,
                'driver': selected_car[3],
                'id_route': id_route,
                'time': time
            }
            
            result = format_obj(selected_car, cursor)
            result['ID_ROUTE'] = id_route
            
            cursor.execute("INSERT INTO AVI_GEOLOCATIONS (ID, START_LATITUDE, START_LONGITUDE, END_LATITUDE, END_LONGITUDE) VALUES (:id_geo, :start_latitude, :start_longitude, :end_latitude, :end_longitude)", data_geo)
            cursor.execute("INSERT INTO AVI_ROUTES (ID, USER_CEDULE, DRIVER, TIME, GEOLOCATION) VALUES (:id_route, :cedule, :driver, :time, :id_geo)", data)
            
            connection.commit()
        
            cursor.close()
            connection.close()
        
        return jsonify({ 'error': False, 'data': result })
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({ 'error': True, 'message': error.message })
