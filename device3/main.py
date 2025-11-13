import network
import time
from umqtt.simple import MQTTClient
import machine 

smoke_pin = machine.Pin(27, machine.Pin.IN)


SSID = "Wokwi-GUEST"
PASSWORD = ""

MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "f0c1b45e-3f3e-4edb-924f-2daa665d7cf3"
SMOKE_TOPIC = "meu_iot/cozinha1/fumaca_pinstate"




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
    
    pin_state = smoke_pin.value()
    

    message = str(pin_state) 
        
    print(f"Publicando em {SMOKE_TOPIC}: {message}")
    client.publish(SMOKE_TOPIC, message)

    time.sleep(5) 