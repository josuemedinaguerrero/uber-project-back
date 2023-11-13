def format_fields(data, cursor):
    column_names = [desc[0] for desc in cursor.description]
    
    result = []
    
    for row in data:
            row_dict = {}
            for i in range(len(row)):
                row_dict[column_names[i]] = row[i]
            result.append(row_dict)

    return result
