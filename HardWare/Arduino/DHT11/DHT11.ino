#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE, 15);

const char* ssid = "***";
const char* password = "***";
const char* mqtt_server = "192.168.1.163";     // MQTT服务器IP
const char* TOPIC = "dht11";                   // 订阅信息主题
const char* client_id = "";                    // 客户端标识，使用MAC地址
String MAC_ID = "";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi() {   

  delay(10);
  //连接WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  MAC_ID = WiFi.macAddress();
  client_id = MAC_ID.c_str();
}
/*
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);// 打印主题信息
  Serial.print("] ");
  Serial.println();

}
*/
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(client_id)) {
      Serial.println("connected");
      
      client.publish("CMAC", client_id);
      /*
      // 连接成功时订阅主题
      client.subscribe("inTopic");
      */
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
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  //client.setCallback(callback);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  char c[50];

  //打印数据
  Serial.print("Humidity: "); 
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: "); 
  Serial.print(t);
  Serial.println(" *C ");
  delay(2000);

  String data =String(h) +"," + String(t) ;//处理传感器数据
  strcpy(c,data.c_str());

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {//延时
    lastMsg = now;
    ++value;
    snprintf (msg, 75, c, value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(TOPIC, msg);
  }
}