import pymysql
import pandas as pd

def db_test():
    # 创建数据库连接(需要修改)
    db = pymysql.connect(host='',
                        port=8883,
                        user='',
                        password='',
                        db='',
                        charset="utf8")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    in_sql = ("INSERT INTO shebei_in (id_in, name_in, status) VALUES (%s, %s, %s)")
    in_data = ('AA:BB:C2:D2:E1:FF', 'CO2', 'offline')
    cursor.execute(in_sql, in_data)
    db.commit()

    query = ("SELECT * FROM shebei_in")  # 替换为你要查询的表名
    cursor.execute(query)

    for row in cursor.fetchall():
        print(row)

    # 关闭数据库连接
    cursor.close()
    db.close()