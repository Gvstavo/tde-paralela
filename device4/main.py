import network
import time
from umqtt.simple import MQTTClient
import machine

trigger_pin = machine.Pin(27, machine.Pin.OUT)
echo_pin = machine.Pin(26, machine.Pin.IN)

SSID = "Wokwi-GUEST"
PASSWORD = ""

MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "7c152066-c618-427e-b137-e5f3331c6e24" 
DIST_TOPIC = "meu_iot/garagem1/distancia_cm"  

print("--- Monitor Serial Pronto. Iniciando Setup ---")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Conectando ao WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("Conectado!", wlan.ifconfig())

try:
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()
    print("Conectado ao MQTT Broker!")
except OSError as e:
    print(f"Erro ao conectar ao MQTT: {e}")
    import machine
    machine.reset()

def get_distance_cm():
    trigger_pin.value(0)
    time.sleep_us(2)

    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    try:
        duration_us = machine.time_pulse_us(echo_pin, 1, 30000)
    except OSError as e:
        print(f"Erro no time_pulse_us: {e}")
        duration_us = 0

    distance_cm = duration_us / 58.0
    
    return round(distance_cm, 2)

while True:
    try:
        distance_cm = get_distance_cm()
        
        
        if distance_cm >= 10:
            print(f"Publicando em {DIST_TOPIC}: {distance_cm} cm")
            client.publish(DIST_TOPIC, str(distance_cm))
        else:
            print(f"Valor detectado: {distance_cm} cm. Muito perto (< 10cm). Não publicando.")

    except Exception as e:
        print(f"Erro no loop principal: {e}")

    time.sleep(2) 