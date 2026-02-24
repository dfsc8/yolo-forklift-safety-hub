"""
MQTT 订阅客户端 - 整合版
功能：订阅叉车告警主题，更新数据库并通过SocketIO推送数据
"""

import paho.mqtt.client as mqtt
import json
import db
from logger import log_event
from datetime import datetime

# MQTT 核心配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/forklift/+/alarm"

# 全局 SocketIO 实例引用（用于WebSocket推送）
socketio_inst = None

def set_socketio(sio):
    """
    设置 SocketIO 实例，用于推送消息到前端
    :param sio: SocketIO 实例对象
    """
    global socketio_inst
    socketio_inst = sio

def on_connect(client, userdata, flags, rc):
    """
    MQTT连接成功/失败回调函数
    :param client: MQTT客户端实例
    :param userdata: 用户自定义数据
    :param flags: 连接标志
    :param rc: 连接返回码（0=成功）
    """
    if rc == 0:
        log_event("INFO", "mqtt.client.connected", "ops", "mqtt", 
                  "Connected to MQTT broker successfully", topic=MQTT_TOPIC)
        client.subscribe(MQTT_TOPIC)
        log_event("INFO", "mqtt.topic.subscribed", "ops", "mqtt", 
                  "Subscribed to target MQTT topic", topic=MQTT_TOPIC)
    else:
        log_event("ERROR", "mqtt.client.connect_failed", "ops", "mqtt", 
                  f"Failed to connect to MQTT broker, return code {rc}", 
                  topic=MQTT_TOPIC, error=rc)

def on_message(client, userdata, msg):
    """
    MQTT收到消息回调函数（核心业务逻辑）
    :param client: MQTT客户端实例
    :param userdata: 用户自定义数据
    :param msg: 收到的MQTT消息对象（包含topic和payload）
    """
    try:
        # 记录原始消息接收日志
        log_event("DEBUG", "mqtt.message.received", "ops", "mqtt", 
                  "MQTT message received", 
                  topic=msg.topic, extra={"payload_size": len(msg.payload)})
        
        # 解析消息体
        payload = json.loads(msg.payload.decode())
        
        # 优先从Topic解析device_id（更可靠），兜底用payload中的值
        topic_parts = msg.topic.split('/')
        device_id = (
            topic_parts[2] if len(topic_parts) >= 3 
            else payload.get("device_id", "unknown")
        )
        alarm = payload.get("alarm", 0)
        
        # 更新数据库
        changed = db.update_device_data(device_id=device_id, alarm=alarm)
        log_event("INFO", "mqtt.message.processed", "biz", "mqtt", 
                  "MQTT message processed and DB updated", 
                  device_id=device_id, topic=msg.topic, changed=changed)

        # 通过SocketIO推送数据到前端（如果实例已初始化）
        if socketio_inst:
            full_data = db.get_latest_data_with_stats()
            socketio_inst.emit('device_update', full_data)
            log_event("DEBUG", "socketio.data.pushed", "biz", "socketio", 
                      "Pushed device data to frontend via SocketIO", 
                      device_id=device_id)
        
    except Exception as e:
        log_event("ERROR", "mqtt.message.parse_failed", "ops", "mqtt", 
                  "Failed to process MQTT message", 
                  topic=msg.topic, error=str(e))

def start_mqtt():
    """
    初始化并启动MQTT客户端（非阻塞模式）
    :return: 成功返回MQTT客户端实例，失败返回None
    """
    # 创建MQTT客户端实例
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # 连接Broker并启动循环（后台线程）
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        log_event("INFO", "mqtt.client.started", "ops", "mqtt", 
                  "MQTT client started successfully", 
                  broker=MQTT_BROKER, port=MQTT_PORT)
        return client
    except Exception as e:
        log_event("CRITICAL", "mqtt.client.start_failed", "ops", "mqtt", 
                  "MQTT client failed to start", 
                  broker=MQTT_BROKER, port=MQTT_PORT, error=str(e))
        return None
