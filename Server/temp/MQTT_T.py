import paho.mqtt.client as mqtt
import json
import config
    
# 回调函数：当建立连接时
def on_connect(client, userdata, flags, rc):
    print(rc)
    #client.subscribe("smfl/contorl")

# 回调函数：当收到消息时
def on_message(client, userdata, msg):
    MQTT_message = str(msg.payload.decode('utf-8'))
    MQTT_topic = str(msg.topic)
    print(MQTT_topic + " " + MQTT_message)

# 创建客户端
client = mqtt.Client(client_id=config.MQTT["client_id"])

# 回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立连接
client.connect(config.MQTT["host"],
               config.MQTT["port"],
               config.MQTT["keeplive"])

# MQTT LOOP
client.loop_forever()