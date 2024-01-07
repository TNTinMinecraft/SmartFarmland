import config
import pymysql

db = pymysql.connect(host=config.mysql_db["host"],
                     port=config.mysql_db["port"],
                     user=config.mysql_db["user"],
                     password=config.mysql_db["password"],
                     db=config.mysql_db["db"],
                     charset=config.mysql_db["charset"])

# 查找设备
def get_from_MAC(table_name, found_MAC):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}` WHERE mac = %s", 
                       (found_MAC,))
    db_get = cursor.fetchall()
    if cursor.rowcount > 0: # 判断行数大于0
        return db_get
    else:
        return -1

# 获取全表
def get_all_db(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}`")
    return cursor.fetchall()

# 获取行数
def get_row(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}`")
    return cursor.rowcount # 返回行数

# 记录度数
def write_data(table_name, mac, time, data):
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE `{table_name}` SET time = %s data = %s WHERE mac = %s", 
                       (time, data, mac))
        db.commit()
        return      
    
    except Exception as e:
        print("Error in MySQL.write_data:", e)
        db.rollback()
        return -1

# 修改设备状态
def switch_status(table_name, mac, status, zhuangtai):
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE `{table_name}` SET status = %s, zhuangtai = %s WHERE mac = %s", 
                       (status, zhuangtai, mac))
        db.commit()
        return      
    
    except Exception as e:
        print("Error in MySQL.switch_status:", e)
        db.rollback()
        return -1

# 更新设备状态
def update_status(table_name, mac, status, leixing):
    if get_from_MAC(table_name, mac) == -1:
        print("New device")

        cursor = db.cursor()
        try:
            cursor.execute(f"INSERT INTO `{table_name}` (mac, name, status, leixing, zhuangtai) VALUES (%s, %s, %s, %s, %s)",
                            (mac, mac, "offline", leixing, "0"))
            db.commit()
            switch_status(table_name, mac, status, "") # 修改状态
            return      
        
        except Exception as e:
            print("Error! MySQL.db_new_device", e)
            db.rollback()
            return -1
    else:
        switch_status(table_name, mac, status, "")

# 更新时间
def update_timer(table_name, mac, time):
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE `{table_name}` SET time = %s WHERE mac = %s", 
                       (time, mac))
        db.commit()
        return      
    
    except Exception as e:
        print("Error in MySQL.update_timer:", e)
        db.rollback()
        return -1

# debug
def db_debug(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}`")

    for row in cursor.fetchall():
        print(row)
    return