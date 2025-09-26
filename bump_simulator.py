import time
import random
import uuid
import json
import paho.mqtt.client as mqtt
from geopy.distance import geodesic

# Simulated GPS path (lat, lon)
route = [
    (-0.4275, 36.9476),  # Start point in Nyeri
    (-0.4280, 36.9480),
    (-0.4285, 36.9485),
    (-0.4290, 36.9490),
    (-0.4295, 36.9495),
    (-0.4300, 36.9500),
]

# MQTT setup
BROKER = "localhost"  # Replace with your broker IP or domain
PORT = 1883
TOPIC = "bump/events"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Vehicle ID
vehicle_id = str(uuid.uuid4())

def simulate_bump(lat, lon):
    bump_event = {
        "type": "AUTO_BUMP",
        "vehicle_id": vehicle_id,
        "timestamp": time.time(),
        "lat": lat,
        "lon": lon,
        "severity": round(random.uniform(0.5, 1.0), 2)  # Simulated shock intensity
    }
    client.publish(TOPIC, json.dumps(bump_event))
    print(f"🚧 Bump reported at ({lat}, {lon})")

def simulate_drive():
    for i, coord in enumerate(route):
        print(f"🚗 Vehicle at {coord}")
        time.sleep(2)  # Simulate movement delay

        # Inject bump randomly or at fixed index
        if i == 2 or random.random() < 0.3:
            simulate_bump(*coord)

simulate_drive()




def manual_flag(lat, lon, flag_type="ADD"):
    flag_event = {
        "type": "MANUAL_FLAG",
        "flag": flag_type,
        "vehicle_id": vehicle_id,
        "timestamp": time.time(),
        "lat": lat,
        "lon": lon
    }
    client.publish("bump/flags", json.dumps(flag_event))





import folium
m = folium.Map(location=route[0], zoom_start=16)
for lat, lon in route:
    folium.Marker([lat, lon], popup="Vehicle").add_to(m)
m.save("map.html")
