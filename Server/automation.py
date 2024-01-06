import time
import MySQL
import threading
import config
import json

in_json = json.loads('{"AA:BB:A1": "30", "AA:BB:B1": "20"}')

'''
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
    if in_data["mode"] == "chuagan":
        print(in_data["data"])
    elif in_data["mode"] == "kongzhi":
        print(in_data["data"])
    else:
        print("Error! NOT Defined mode " + in_data["mode"] + " from " + in_data["id"]) # debug
'''
def auto_in(in_data):
    sql_data = MySQL.get_MAC("zidonghua", in_data["id"])
    if sql_data != -1:
        raw_data = f'{in_data["data"]} {sql_data[1]} {sql_data[2]}'
        if eval(raw_data):
            print("OK") # 成立
        else:
            MySQL.update_timer("zidonghua", in_data["id"], "-1") # 不成立

def auto():
    while True:
        sql_data = MySQL.get_db("zidonghua")
        sql_row = MySQL.get_row("zidonghua")
        while sql_row >= 0:
            if sql_data[sql_row][6] != "-1":
                MySQL.update_timer("zidonghua", sql_data[sql_row][0], sql_data[sql_row][6] + 1) # 自增time
                print(f"{sql_data[sql_row][0]} {sql_data[sql_row][6]}") # debug
            
            if sql_data[sql_row][6] >= sql_data[sql_row][3]:
                print(f"ON ID: {sql_data[sql_row][4]} DATA: {sql_data[sql_row][5]}") # debug
            elif sql_data[sql_row][6] == "-1":
                print(f"OFF ID: {sql_data[sql_row][4]} DATA: {sql_data[sql_row][5]}")
            
            time.sleep(1)
            sql_row -= 1


def main():
    while True:
        time.sleep(1)
        #print("OK")

if __name__ == '__main__':
    MySQL.print_db("zidonghua")