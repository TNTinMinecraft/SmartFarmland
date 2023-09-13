import pymysql

db = pymysql.connect(host='',
                    port=8883,
                    user='smartfarmland',
                    password='smartfarmland',
                    db='smartfarmland',
                    charset="utf8")

# 遍历打完整库
def print_db():
    cursor = db.cursor()
    query = ("SELECT * FROM shebei_in")
    cursor.execute(query)

    for row in cursor.fetchall():
        print(row)
    return

# 注册设备
def db_write(clint_st):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM shebei_in ORDER BY number DESC LIMIT 1")
        last_number = cursor.fetchone()[0]
        #print(last_number)

        cursor.execute("INSERT INTO shebei_in (number, id_in, name_in, status) VALUES (%s, %s, %s, %s)",
                        (last_number + 1, clint_st[0], clint_st[1], clint_st[2]))
        db.commit()
        return
    
    except:
        print ("Error!")

# 查询设备行数
def get_MAC(found_MAC):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM shebei_in WHERE id_in = %s",
                        (found_MAC))
        MAC_num = cursor.fetchall()[0][0]
        return MAC_num

    except:
        print ("Error!")

# 修改设备状态
def switch_status(found_MAC, in_status):
    if in_status == 1:
        write_status = "online"
    elif in_status == 0:
        write_status = "offline"
    cursor = db.cursor()

    try:
        cursor.execute("UPDATE shebei_in SET status = %s WHERE id_in = %s",
                        (write_status, found_MAC))
        db.commit()
        return
    
    except:
        print ("Error!")