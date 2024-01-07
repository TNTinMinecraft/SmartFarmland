import time
import MySQL
import config
import json

def auto_in(in_data):
    sql_data = MySQL.get_from_MAC("zidonghua", in_data["id"])
    if sql_data != -1:
        raw_data = f'{in_data["data"]} {sql_data[1]} {sql_data[2]}'
        if eval(raw_data):
            print("OK") # 成立
        else:
            MySQL.update_timer("zidonghua", in_data["id"], "-1") # 不成立

def auto():
    while True:
        sql_data = MySQL.get_all_db("zidonghua")
        sql_row = MySQL.get_row("zidonghua")
        while sql_row >= 0:
            if sql_data[sql_row][6] != "-1":
                MySQL.update_timer("zidonghua", sql_data[sql_row][0], sql_data[sql_row][6] + 1) # 自增timer
                print(f"{sql_data[sql_row][0]} {sql_data[sql_row][6]}") # debug
            
            if sql_data[sql_row][6] >= sql_data[sql_row][3]:
                print(f"ON ID: {sql_data[sql_row][4]} DATA: {sql_data[sql_row][5]}")
                MySQL.update_timer("zidonghua", sql_data[sql_row][0], "-1") # 清零tinmer
            elif sql_data[sql_row][6] == "-1":
                print(f"OFF ID: {sql_data[sql_row][4]} DATA: {sql_data[sql_row][5]}")

            time.sleep(1)
            sql_row -= 1 # 自减

if __name__ == "__main__":
    MySQL.db_debug("zidonghua")
    auto()