#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "mi";
const char* password = "11111111";
const char* mqtt_server = "192.168.2.94";     // MQTT服务器IP
const char* client_id = "NULL";                    // 客户端标识，使用MAC地址
String MAC_ID = "";

int switchPin = 16;

WiFiClient espClient;
PubSubClient client(espClient);
StaticJsonDocument<200> doc;

void setup_wifi() {
  delay(10);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.macAddress());
  MAC_ID = WiFi.macAddress();
  client_id = MAC_ID.c_str();
}

void callback(char* topic, byte* payload, unsigned int length) {
  // 创建一个足够大的 StaticJsonDocument
  StaticJsonDocument<200> doc;

  // 将payload转换为字符串
  String payload_str;
  for (int i = 0; i < length; i++) {
    payload_str += (char)payload[i];
  }

  // 使用deserializeJson()函数解析JSON字符串
  DeserializationError error = deserializeJson(doc, payload_str);
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return;
  }
  
  if (doc["id_out"].as<String>() == client_id) {
    if (doc["set"].as<String>() == "on") {
      digitalWrite(switchPin, HIGH);
    } else if (doc["set"].as<String>() == "off") {
      digitalWrite(switchPin, LOW);
    }
  }

  Serial.print(doc["id_out"].as<String>());
  Serial.print(doc["set"].as<String>()); // 打印主题信息
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(client_id)) {
      Serial.println("connected");
      // client.publish("CMAC", client_id);
      client.publish("smfl/status", ("{\"status\": \"online\", \"id\": \"" + MAC_ID + "\", \"mode\": \"out\"}").c_str());
      // 连接成功时订阅主题
      client.subscribe("smfl/contorl");
      Serial.println("online");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();

  pinMode(switchPin, OUTPUT);
  digitalWrite(switchPin, LOW);
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

}