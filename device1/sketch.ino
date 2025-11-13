#include <WiFi.h>
#include <PubSubClient.h>
// #include <DHT.h> // Não é mais necessário

// --- Configuração do WiFi (Wokwi-GUEST) ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// --- Configuração do MQTT ---
const char* mqtt_broker = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* client_id = "973be25e-9d20-4e7e-97ab-6f5197958bcf"; // ID ÚNICO
const char* temp_topic = "meu_iot/quarto1/temperatura";

WiFiClient espClient;
PubSubClient client(espClient);

// --- REQUISITO B: Filtro de Outlier ---
float last_temp = 25.0; // Valor inicial "seguro"

// --- Funções de Conexão (Idênticas ao exemplo anterior) ---
void connectWiFi() {
  Serial.print("Conectando ao WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println(" Conectado!");
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect(client_id)) {
      Serial.println(" Conectado!");
    } else {
      Serial.print(" falhou, rc="); Serial.print(client.state());
      Serial.println(" tentando novamente em 5s");
      delay(5000);
    }
  }
}

void publicarMQTT(const char* topic, float value) {
  char buffer[10];
  dtostrf(value, 4, 2, buffer); 
  Serial.printf("Publicando em %s: %s\n", topic, buffer);
  client.publish(topic, buffer);
}
// --- Fim das Funções de Conexão ---

void setup() {
  Serial.begin(115200);

  // Espera o monitor serial ficar pronto (crucial para Wokwi e placas reais)
  while (!Serial) {
    delay(10); 
  }
  delay(1000); // Um segundo extra de garantia
  Serial.println("\n--- Monitor Serial Pronto. Iniciando Setup ---");

  // Inicializa o gerador de números aleatórios
  randomSeed(analogRead(0)); 

  connectWiFi();
  client.setServer(mqtt_broker, mqtt_port);
}

void loop() {
  // --- AJUSTE PARA 1 EM CADA 10 ---
  // "static int" faz com que a variável mantenha seu valor
  // mesmo depois que a função 'loop' termina e recomeça.
  static int loop_counter = 0;
  
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Incrementa o contador a cada ciclo
  loop_counter++;

  float t;

  if (loop_counter == 10) { // 🎯 Na 10ª volta, é um outlier
    // Gera um outlier, ex: 80.00 a 90.00
    t = random(8000, 9001) / 100.0;
    loop_counter = 0; // Reinicia o contador
  } else { // Nas voltas 1 a 9, é um valor normal
    // Gera um valor normal entre 20.00 e 35.00
    t = random(2000, 3501) / 100.0; 
  }
  // --- FIM DO AJUSTE ---


  // --- REQUISITO B: Processamento no Dispositivo (Filtro) ---
  // O filtro agora pegará o 10º valor
  if (!isnan(t) && (abs(t - last_temp) < 15)) {
    last_temp = t; // Atualiza o último valor válido
    publicarMQTT(temp_topic, t);
  } else {
    Serial.print("Outlier de Temperatura detectado! Valor: ");
    Serial.println(t);
  }

  delay(2000); // Envia dados a cada 5 segundos
}