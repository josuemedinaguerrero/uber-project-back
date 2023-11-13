import cx_Oracle

def connection_db():
    connection = cx_Oracle.connect(
                user='system',
                password='123456',
                dsn='localhost:1521/XEPDB1',
                encoding='UTF-8'
            )

    cursor = connection.cursor()
    return connection, cursor
