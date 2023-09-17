import paho.mqtt.client as mqtt
import json
import config
from flask import Flask, request, jsonify

app = Flask(__name__)

# 创建客户端
client = mqtt.Client(client_id=config.MQTT["client_id"])

# 建立连接
client.connect(config.MQTT["host"],
               config.MQTT["port"],
               config.MQTT["keeplive"])

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
