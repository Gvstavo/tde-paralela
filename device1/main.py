import network
import time
from umqtt.simple import MQTTClient
import random
import machine
import dht  
import json 

dht_pin = machine.Pin(15) 
sensor = dht.DHT22(dht_pin)

SSID = "Wokwi-GUEST"
PASSWORD = ""

MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "8440702b-4aa8-49ba-bf53-6c0fd6460490" # ID ÚNICO
DATA_TOPIC = "meu_iot/quarto1/clima"          

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


while True:
    temp = 0.0
    humid = 0.0
    
    try:
        sensor.measure() 
        temp = sensor.temperature() 
        humid = sensor.humidity() 
    except OSError as e:
        print(f"Erro ao ler o sensor DHT: {e}")
        temp = -999 
        humid = -999

    temp_valida = (temp >= 0.0 and temp <= 40.0)
    humid_valida = (humid >= 0.0 and humid <= 100.0)
    
    if temp_valida and humid_valida:
        data_dict = {
            "temperatura": temp,
            "umidade": humid
        }
        message_json = json.dumps(data_dict)
        
        print(f"Publicando em {DATA_TOPIC}: {message_json}")
        client.publish(DATA_TOPIC, message_json)
    else:
        print(f"Leitura fora da faixa: T={temp} C, H={humid} %. Não publicando.")

    time.sleep(5) 