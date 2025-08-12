import paho.mqtt.client as mqtt
import time
import random

# MQTT Broker settings
broker_ip = "192.168.178.156"   # ← your VM2 IP
broker_port = 1883
username = "mqttuser"
password = "mqttpass"

# MQTT Topics
topic_moisture = "balcony/moisture"
topic_status = "balcony/pump_status"

# Moisture simulation parameters
moisture = 100
threshold = 50
pump_on = False

# Create MQTT client
client = mqtt.Client(protocol=mqtt.MQTTv311)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Assign callback
client.on_connect = on_connect

# Set MQTT credentials
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_ip, broker_port)
client.loop_start()

# Simulation loop
try:
    for t in range(0, 60, 2):  # Simulate 60 seconds (2-second steps)
        # Simulate moisture loss
        loss = random.uniform(1, 5)
        moisture = max(0, moisture - loss)
        print(f"[{t}s] Moisture: {moisture:.2f}%")
        client.publish(topic_moisture, f"{moisture:.2f}")

        if moisture < threshold and not pump_on:
            print(f"[{t}s] Pump ON")
            client.publish(topic_status, "ON")
            pump_on = True
            time.sleep(5)  # simulate pump duration
            moisture = min(100, moisture + 25)
            print(f"[{t+5}s] Pump OFF - Moisture: {moisture:.2f}%")
            client.publish(topic_status, "OFF")
            pump_on = False
        else:
            time.sleep(2)

except KeyboardInterrupt:
    print("Simulation interrupted.")

finally:
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")