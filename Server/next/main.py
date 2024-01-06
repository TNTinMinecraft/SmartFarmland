import config
import paho.mqtt.client as mqtt
import threading
from flask import Flask, request, jsonify
import json
import MySQL
import time

# Flask app init
app = Flask(__name__)
# 设定客户端ID
client = mqtt.Client(config.MQTT["client_id"])
mqtt_done = "MAC" # 等待返回

# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    client.subscribe("smfl/status") # 设备状态
    client.subscribe("smfl/back") # 设备控制

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    global mqtt_done
    MQTT_topic = str(msg.topic)
    try:
        MQTT_message = json.loads(str(msg.payload.decode('utf-8')))
    except Exception as e:
        print("Error! MQTT_message", e)
        return
    
    print(MQTT_message) # debug

    if MQTT_topic == "smfl/status": # 设备状态
        if MQTT_message["mode"] == "in":
            MySQL.update_status("chuanganqi",MQTT_message["mac"], MQTT_message["status"], MQTT_message["leixing"])
            print(f"chuanganqi {MQTT_message['mac']} {MQTT_message['status']} {MQTT_message['leixing']}") # debug
        elif MQTT_message["mode"] == "out":
            MySQL.update_status("xiaoyinqi",MQTT_message["mac"], MQTT_message["status"], MQTT_message["leixing"])
            print(f"xiaoyinqi {MQTT_message['mac']} {MQTT_message['status']} {MQTT_message['leixing']}") # debug
        else:
            print("Error! not define mode in status_json")

    elif MQTT_topic == "smfl/back": # 设备返回
        try:
            if MQTT_message["success"]:
                mqtt_done = MQTT_message["mac"]
        except Exception as e:
            print("Error! MQTT_message", e)
            return
    
    else:
        print("Error! not define topic")

# 根路由
@app.route('/')
def main_page():
    return "This is SmartFarmland Server, please use GET method to send data."

@app.route('/api', methods=['GET'])
def conturl_api():
    global mqtt_done
    mqtt_done = "MAC"
    api_mac_out = request.args.get('mac_out')
    api_set = request.args.get('set')
    if api_mac_out == None or api_set == None:
        return "Error! Please use GET method to send data."
    else:
        api_data_json = json.dumps({"id_out": api_mac_out, "set": api_set})
        client.publish("smfl/control", api_data_json)
        start_time = time.time()
        while mqtt_done != api_mac_out: # 等待执行成功
            print("Waiting for MQTT...", api_mac_out)
            if time.time() - start_time > 1:
                MySQL.switch_status("xiaoyinqi", api_mac_out, "offline", "off")
                MySQL.db_debug("xiaoyinqi")
                print("Error! MQTT timeout")
                return "Error! MQTT timeout"
            time.sleep(0.1)
        MySQL.switch_status("xiaoyinqi", api_mac_out, "online", api_set)
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
    app.run(host="0.0.0.0", port=8166)

if __name__ == "__main__":
    # 创建线程
    mqtt_thread = threading.Thread(target=MQTT_loop)
    flask_thread = threading.Thread(target=flask_loop)

    # 设定守护线程
    mqtt_thread.setDaemon(True)
    flask_thread.setDaemon(True)

    # 启动线程
    mqtt_thread.start()
    print("MQTT_thread start")
    flask_thread.start()
    print("Flask_thread start")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit()  # 退出程序