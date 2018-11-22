import pymysql.cursors
import pandas as pd
from secret import *

connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             db=DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "SELECT `id`, `name`, `screen_name`, `description`, `location` from `user`"
        cursor.execute(sql)
        result = cursor.fetchall()
        pd.DataFrame(result).to_csv('users.csv', index=False)
finally:
    connection.close()
