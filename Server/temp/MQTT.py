'''
import paho.mqtt.client as mqtt
import json
import config
from flask import Flask, request, jsonify

app = Flask(__name__)

# 创建客户端
client = mqtt.Client(client_id=MQTT["client_id"])

# 建立连接
client.connect(MQTT["host"],
               MQTT["port"],
               MQTT["keeplive"])

client.loop_start()

@app.route('/')
def main_page():
    return "There is API!!!!!!!!!!!"

@app.route('/api')
def api_page():
    api_id_out = request.args.get('id_out')
    api_set = request.args.get('set')
    if not api_id_out or not api_set:
        return jsonify({"error": "Topic or Message is missing"}), 400
    api_data = {"id_out": api_id_out, "set": api_set}
    api_data_json = json.dumps(api_data)
    client.publish("smfl/contorl", api_data_json)
    print(api_data_json)
    return jsonify({"success": True})
    #return f'id_out: {api_id_out}, set: {api_set}'

if __name__ == '__main__':
    app.run(debug=True)
'''
MQTT = {
    "host":"192.168.31.193",
    "port":1883,
    "keeplive":60,
    "client_id":"Py_server"
}

import MySQL
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import threading


# 设备在线状态解码
def DeMQTT(in_topic, in_message):
    MQTT_data = json.loads(in_message)

    if "clean_start" in MQTT_data:
        out_status = "online"
    else :
        out_status = "offline"
    
    print(MQTT_data["clientid"] + " " + out_status)
    #MySQL.write_status("shebei_in", MQTT_data["clientid"], out_status)
    #MySQL.print_db("shebei_in") # debug
    
# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    client.subscribe("$SYS/brokers/+/clients/#") # 设备在线状态
    client.subscribe("smfl/back") # 设备控制

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    MQTT_message = str(msg.payload.decode('utf-8'))
    MQTT_topic = str(msg.topic)
    if MQTT_topic == "smfl/back": # 设备返回
        back_data = json.loads(MQTT_message)
        #automation.auto_in(back_data)
    else: # 设备在线状态
        print(MQTT_topic + " " + MQTT_message)
        DeMQTT(MQTT_topic, MQTT_message)

# 创建客户端
client = mqtt.Client(client_id=MQTT["client_id"])

# 回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立MQTT连接
client.connect(MQTT["host"],
               MQTT["port"],
               MQTT["keeplive"])

if __name__ == '__main__':
    client.loop_forever()
    # 退出
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")
