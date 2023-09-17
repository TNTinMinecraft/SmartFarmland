import pymysql
import config

db = pymysql.connect(host=config.mysql_db["host"],
                     port=config.mysql_db["port"],
                     user=config.mysql_db["user"],
                     password=config.mysql_db["password"],
                     db=config.mysql_db["db"],
                     charset=config.mysql_db["charset"])

# 遍历打完整库
def print_db(table_name):
    cursor = db.cursor()
    #query = ("SELECT * FROM shebei_in")
    cursor.execute(f"SELECT * FROM `{table_name}`")

    for row in cursor.fetchall():
        print(row)
    return

# 查询设备行数
def get_MAC(table_name, found_MAC):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}` WHERE id_in = %s", 
                       (found_MAC,))
    db_get = cursor.fetchall()
    if len(db_get) > 0: # 判断长度大于0
        return db_get[0][0]
    else:
        return -1

    
# 注册设备
def db_write(table_name, clint_st):
    cursor = db.cursor()
    try:
        cursor.execute(f"INSERT INTO `{table_name}` (id_in, name_in, status) VALUES (%s, %s, %s)",
                        (clint_st[0], clint_st[1], clint_st[2]))
        db.commit()
        return
    
    except:
        print ("Error! db_write")

# 修改设备状态
def switch_status(table_name, found_MAC, in_status):
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE `{table_name}` SET status = %s WHERE id_in = %s",
                        (in_status, found_MAC))
        db.commit()
        return
    
    except:
        print ("Error! switch_status")

# 写入设备
def write_status(table_name, id_in, status):
    if get_MAC(table_name, id_in) == -1: # 当不存在此设备
        print("new")
        db_write(table_name, (id_in, "NULL", "offline")) # 新建键
        switch_status(table_name, id_in, status)
    else:
        switch_status(table_name, id_in, status)
        
    #print_db(table_name)