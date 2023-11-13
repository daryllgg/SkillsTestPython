from mysql.connector import connect

db = connect(
    host = '127.0.0.1',
    user = 'root',
    password = '',
    database = 'skills'
)

#1. ADD DATA
def add_data(table: str, **kwargs)->int:
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join(['%s'] * len(kwargs))
    values = tuple(kwargs.values())

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()

    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected

#2. EDIT DATA
def update_data(table: str, **kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())

    #FOR SET
    set_clause = ", ".join([f"`{key}` = %s" for key in keys[1:]])
    #FOR WHERE
    where_condition = f"`{keys[0]}` = %s"

    sql : str = f"UPDATE {table} SET {set_clause} WHERE {where_condition}"
    values = values[1: ] + [values[0]]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    cursor.close()

    rows_affected = cursor.rowcount
    return rows_affected

#3. DELETE DATA
def delete_data(table: str, **kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())

    sql = f"DELETE FROM {table} WHERE `{keys[0]}` = '{values[0]}'"
    cursor : object = db.cursor(dictionary=True)
    cursor.execute(sql)
    db.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


#4. GET DATA
def get_data(table: str, **kwargs)->dict:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())

    
    
    sql : str = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
    cursor : object = db.cursor(dictionary=True)
    cursor.execute(sql)
    data : list = cursor.fetchone()
    return data


#5. GET ALL DATA
def get_all_data(table: str)->list:
    sql : str = f"SELECT * FROM {table}"
    cursor : object = db.cursor(dictionary=True)
    cursor.execute(sql)
    data : list = cursor.fetchall()
    return data

#6. CHECK EXISTS
def exists(key: str, value: str)->bool:

    data = get_all_data('student')
    for datum in data:
        if str(datum[key]) == value:
            return True
    return False
        

