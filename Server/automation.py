import time
import MySQL
import threading
import config
import json

db = MySQL.connect(host=config.mysql_db["host"],
                     port=config.mysql_db["port"],
                     user=config.mysql_db["user"],
                     password=config.mysql_db["password"],
                     db=config.mysql_db["db"],
                     charset=config.mysql_db["charset"])

cursor = db.cursor()

in_json = json.loads('{"AA:BB:A1": "30", "AA:BB:B1": "20"}')

def auto():
    while True:
        cursor.execute(f"SELECT * FROM `zidonnghua`")

        for db_get in cursor.fetchall():
            db_data = db_get
            if in_json[db_data[0]] != '':
                raw_data = f"{in_json[db_data[0]]} {db_data[1]} {db_data[2]}"
                if eval(raw_data):
                    print("OK") # 写入time
                else:
                    if db_data[6] != "0":
                        print("--") # 自减time
            else:
                return
        
        cursor.execute(f"SELECT * FROM `zidonnghua`")

        for db_get in cursor.fetchall():
            if db_get[6] >= db_get[3]:
                print(f"{db_get[4]} {db_get[5]}") # 修改状态

# 创建线程
auto_thread = threading.Thread(target=auto)
auto_thread.daemon = True
auto_thread.start()

def auto_in(in_data):
    in_json = in_data
    print(in_data["id"])
    if in_data["mode"] == "chuangan":
        print(in_data["data"])
    elif in_data["mode"] == "kongzhi":
        print(in_data["data"])
    else:
        print("Error! NOT Defined mode " + in_data["mode"] + " from " + in_data["id"]) # debug
