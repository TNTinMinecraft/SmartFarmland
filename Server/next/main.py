import config
import paho.mqtt.client as mqtt
import threading
from flask import Flask, request, jsonify
import json

# Flask app init
app = Flask(__name__)
# 设定客户端ID
client = mqtt.Client(config.MQTT["client_id"])

# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    client.subscribe("smfl/status") # 设备状态
    client.subscribe("smfl/back") # 设备控制

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    print("") 

# 根路由
@app.route('/')
def main_page():
    return "This is SmartFarmland Server, please use GET method to send data."

@app.route('/api', methods=['GET'])
def conturl_api():
    api_id_out = request.args.get('id_out')
    api_set = request.args.get('set')
    if api_id_out == None or api_set == None:
        return "Error! Please use GET method to send data."
    else:
        api_data_json = json.dumps({"id_out": api_id_out, "set": api_set})
        client.publish("smfl/control", api_data_json)
        return f"ID: {api_id_out} SET: {api_set}"

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