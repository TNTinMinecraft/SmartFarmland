import config
import paho.mqtt.client as mqtt
import threading
from flask import Flask, request, jsonify
import json
import MySQL
import time
import automation

# Flask app init
app = Flask(__name__)
# 设定客户端ID
client = mqtt.Client(config.MQTT["client_id"])
mqtt_done = "MAC" # 等待返回
mqtt_get = {"mac": "-1", "data": ""} # 传感器度数

# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    client.subscribe("smfl/status") # 设备状态
    client.subscribe("smfl/callback") # 设备返回
    client.subscribe("smfl/chuangan") # 传感器度数

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    global mqtt_done
    global mqtt_get

    # 解码MQTT消息
    MQTT_topic = str(msg.topic)
    try:
        MQTT_message = json.loads(str(msg.payload.decode('utf-8')))
    except Exception as e:
        print("Error! MQTT_message", e)
        return

    print(MQTT_message) # debug

    # 设备状态
    if MQTT_topic == "smfl/status":
        if MQTT_message["mode"] == "in":
            MySQL.update_status("chuanganqi", MQTT_message["mac"], MQTT_message["status"], MQTT_message["leixing"])
            print(f"chuanganqi {MQTT_message['mac']} {MQTT_message['status']} {MQTT_message['leixing']}") # debug
        elif MQTT_message["mode"] == "out":
            MySQL.update_status("xiaoyingqi", MQTT_message["mac"], MQTT_message["status"], MQTT_message["leixing"])
            print(f"xiaoyingqi {MQTT_message['mac']} {MQTT_message['status']} {MQTT_message['leixing']}") # debug
        else:
            print("Error! not define mode in status_json", MQTT_message)
    
    # 自动化返回
    elif MQTT_topic == "smfl/chuangan":
        try:
            if MQTT_message["data"] != "":
                mqtt_get["mac"] = MQTT_message["mac"]
                mqtt_get["data"] = MQTT_message["data"]
        except Exception as e:
            print("Error! MQTT_message", e)
            return

    # 设备返回
    elif MQTT_topic == "smfl/callback":
        try:
            if MQTT_message["success"]:
                mqtt_done = MQTT_message["mac"]
        except Exception as e:
            print("Error! MQTT_message", e)
            return
    
    # 未定义topic
    else:
        print("Error! not define topic", MQTT_topic)

# 写入传感器度数
def MQTT_get():
    global mqtt_get
    mqtt_get["mac"] = "-1"

    while True:
        print("MQTT_get start")
        sql_data = MySQL.get_all_db("chuanganqi")
        sql_row = MySQL.get_row("chuanganqi")
        while sql_row >= 0:
            client.publish("smfl/chuangan", json.dumps({"id": sql_data[sql_row][0], "data": "get"})) # 请求数据
            start_time = time.time()
            while mqtt_get["mac"] != sql_data[sql_row][0]:
                print("Waiting for MQTT...", sql_data[sql_row][0])
                if time.time() - start_time > 0.5:
                    MySQL.switch_status("chuanganqi", sql_data[sql_row][0], "offline", "-1")
                    MySQL.db_debug("chuanganqi") # debug
                    print("Error! MQTT timeout", sql_data[sql_row][0])
                    return "Error! MQTT timeout"
                time.sleep(0.1)
            MySQL.switch_status("chuanganqi", sql_data[sql_row][0], "online", mqtt_get["data"]) # 修改状态
            MySQL.write_data("chuanganqi", sql_data[sql_row][0], time.time(), mqtt_get["data"]) # 写入数值
            # 选择主传感器
            if sql_data[sql_row][0] == config.main_define["wendu"]:
                MySQL.write_data("chuanganqi", "wendu", time.time(), mqtt_get["data"]) # 主温度传感器
            elif sql_data[sql_row][0] == config.main_define["shidu"]:
                MySQL.write_data("chuanganqi", "shidu", time.time(), mqtt_get["data"]) # 主湿度传感器
            # 存入自动化
            automation.auto_in({"mac": sql_data[sql_row][0], "data": mqtt_get["data"]})
            
            print(f"chuanganqi {sql_data[sql_row][0]} {mqtt_get['data']}") # debug
        print("MQTT_get end")
        time.sleep(10) # 更新间隔，默认3600秒（1小时）

# 根路由
@app.route('/')
def main_page():
    return "This is SmartFarmland Server, please use GET method to send data."

# API路由
@app.route('/api', methods=['GET'])
def conturl_api():
    global mqtt_done
    mqtt_done = "MAC"
    # 获取GET参数
    api_mac_out = request.args.get('mac_out')
    api_set = request.args.get('set')

    if api_mac_out == None or api_set == None:
        return "Error! your GET method is wrong"
    else:
        api_data_json = json.dumps({"id_out": api_mac_out, "set": api_set})
        client.publish("smfl/control", api_data_json)
        # 等待执行成功
        start_time = time.time()
        while mqtt_done != api_mac_out:
            print("Waiting for MQTT...", api_mac_out)
            if time.time() - start_time > 1: # 超时1S
                MySQL.switch_status("xiaoyingqi", api_mac_out, "offline", "off")
                MySQL.db_debug("xiaoyingqi") # debug
                print("Error! MQTT timeout", api_mac_out)
                return "Error! MQTT timeout"
            time.sleep(0.1)
        MySQL.switch_status("xiaoyingqi", api_mac_out, "online", api_set)
        return f"ID: {api_mac_out} SET: {api_set}"

# MQTT线程
def MQTT_loop():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.MQTT["host"],
                   config.MQTT["port"],
                   config.MQTT["keeplive"]) # 建立MQTT连接
    
    client.loop_forever() # 主循环

# Flask线程
def flask_loop():
    app.run(host=config.api_server["host"], port=config.api_server["port"], debug=False)

# 自动化线程
def auto_loop():
    automation.auto()

if __name__ == "__main__":
    # 创建线程
    mqtt_thread = threading.Thread(target=MQTT_loop)
    flask_thread = threading.Thread(target=flask_loop)
    auto_thread = threading.Thread(target=auto_loop)

    # 设定守护线程
    mqtt_thread.setDaemon(True)
    flask_thread.setDaemon(True)
    auto_thread.setDaemon(True)

    # 启动线程
    #mqtt_thread.start()
    print("MQTT_thread start")
    flask_thread.start()
    print("Flask_thread start")
    #auto_thread.start()
    print("Auto_thread start")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit()  # 退出程序