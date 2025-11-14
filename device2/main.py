import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, ADC
import random
import math  

SSID = "Wokwi-GUEST"
PASSWORD = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "4751671b-edb7-4b56-a46d-5dd4f93da0e0"
LIGHT_TOPIC = "meu_iot/sala1/luz_lux" 

print("--- Monitor Serial Pronto. Iniciando Setup ---")

ldr_pin = ADC(Pin(35))
ldr_pin.atten(ADC.ATTN_11DB) 
ldr_pin.width(ADC.WIDTH_10BIT) 


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


GAMMA = 0.7 
RL10 = 50.0  

V_IN = 3.3          
R_FIXO = 10000.0  

def converter_analog_para_lux(valor_analog):
    try:
        if valor_analog >= 1023:
            return 0.0 

        voltage = (float(valor_analog) / 1023.0) * V_IN
        
        if V_IN == voltage:
            return 0.0 
            
        resistance = (R_FIXO * voltage) / (V_IN - voltage)

        rl10_ohms = RL10 * 1000.0
        pow_10_gamma = math.pow(10, GAMMA)
        
        base = (rl10_ohms * pow_10_gamma) / resistance
        lux = math.pow(base, (1.0 / GAMMA))
        
        return lux

    except Exception as e:
        print(f"Erro no cálculo de Lux: {e}")
        return -1.0


loop_counter = 0 

while True:
    loop_counter += 1
    valor_publicar_str = "" 
    
    valor_ldr = ldr_pin.read()
    lux = converter_analog_para_lux(valor_ldr)
        
    lux_formatado = round(lux, 2)
    valor_publicar_str = str(lux_formatado)
        
    print(f"{valor_ldr} -> Convertido (Lux): {lux_formatado} -> Publicando...")
    
    client.publish(LIGHT_TOPIC, valor_publicar_str)
    time.sleep(3)