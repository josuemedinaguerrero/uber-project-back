import cx_Oracle

try:
    connection = cx_Oracle.connect(
        user='system',
        password='123456',
        dsn='localhost:1521/XEPDB1',
        encoding='UTF-8'
    )
except Exception as ex:
    print(ex)
finally:
    print("Conexión finalizada.")
