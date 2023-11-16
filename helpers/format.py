import cx_Oracle

def format_fields(data, cursor):
    column_names = [desc[0] for desc in cursor.description]
    
    result = []
    
    for row in data:
            row_dict = {}
            for i in range(len(row)):
                row_dict[column_names[i]] = row[i]
            result.append(row_dict)

    return result

def format_fields_with_clob(data, cursor):
    column_names = [desc[0] for desc in cursor.description]
    
    result = []
    
    for row in data:
        row_dict = {}
        for i in range(len(row)):
            if isinstance(row[i], cx_Oracle.LOB):
                row_dict[column_names[i]] = row[i].read()
            else:
                row_dict[column_names[i]] = row[i]
        result.append(row_dict)

    return result

def format_obj(data, cursor):
    selected_columns = [col[0] for col in cursor.description]
    return dict(zip(selected_columns, data))
