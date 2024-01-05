import MySQL
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import threading
import config

import automation

app = Flask(__name__)

'''
# 设备在线状态解码
def DeMQTT(in_message):
    try:
        MQTT_data = json.loads(in_message)
    except:
        print("Error! MQTT_data")
        return

    if "clean_start" in MQTT_data:
        out_status = "online"
    else :
        out_status = "offline"
    
    print(MQTT_data["clientid"] + " " + out_status)
    MySQL.write_status("shebei_in", MQTT_data["clientid"], out_status)
'''

# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    #client.subscribe("$SYS/brokers/+/clients/#") # 设备在线状态
    client.subscribe("smfl/status") # 设备状态
    client.subscribe("smfl/back") # 设备控制

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    MQTT_message = str(msg.payload.decode('utf-8'))
    MQTT_topic = str(msg.topic)

    if MQTT_topic == "smfl/back": # 设备返回
        try:
            back_data = json.loads(MQTT_message)
            print(back_data)
            #automation.auto_in(back_data)
        except:
            print("Error! back_data")

    elif MQTT_topic == "smfl/status": # 设备状态
            status_data = json.loads(MQTT_message)
            print(status_data)
            if status_data["mode"] == "out":
                MySQL.write_status("shebei_out", status_data["id"], status_data["status"])
                MySQL.print_db("shebei_out") # debug
            elif status_data["mode"] == "in":
                MySQL.write_status("shebei_in",  status_data["id"], status_data["status"])
                MySQL.print_db("shebei_in") # debug
            else:
                print("Error! status_data")
                

    else: # 设备在线状态
        print(MQTT_topic + " " + MQTT_message)
        #DeMQTT(MQTT_message)

# 创建客户端
client = mqtt.Client(client_id=config.MQTT["client_id"])

# 回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立MQTT连接
client.connect(config.MQTT["host"],
               config.MQTT["port"],
               config.MQTT["keeplive"])

# 根路由
@app.route('/')
def main_page():
    return "This is API!!!!!!!!!!!"

# /api路由
@app.route('/api')
def api_page():
    api_id_out = request.args.get('id_out')
    api_set = request.args.get('set')
    if not api_id_out or not api_set:
        return jsonify({"error": "Topic or Message is missing"}), 400
    api_data = {"id_out": api_id_out, "set": api_set}
    api_data_json = json.dumps(api_data)
    client.publish("smfl/contorl", api_data_json)
    return jsonify({"success": True})
    #return f'id_out: {api_id_out}, set: {api_set}' # debug

# MQTT callback
def run_mqtt_loop():
    client.loop_forever()

#automation
def run_automation():
    automation.main()

# api server
def run_flask_api():
    app.run(port=8166)

if __name__ == '__main__':
    # 创建线程
    mqtt_thread = threading.Thread(target=run_mqtt_loop)
    auto_thread = threading.Thread(target=run_automation)
    flask_thread = threading.Thread(target=run_flask_api)
    
    # 设置为守护线程
    mqtt_thread.daemon = True
    auto_thread.daemon = True
    flask_thread.daemon =True

    # 启动线程
    mqtt_thread.start()
    print("MQTT thread started")
    auto_thread.start()
    print("Automation thread started")
    flask_thread.start()
    print("Flask thread started")
    
    # 退出
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")