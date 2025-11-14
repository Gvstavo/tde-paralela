# Projeto de Monitoramento IoT com ESP32, MQTT e Node-RED

![Node-RED](https://img.shields.io/badge/Plataforma-Node--RED-red?style=for-the-badge&logo=nodered)
![Wokwi](https://img.shields.io/badge/Simulado_em-Wokwi-40AE49?style=for-the-badge&logo=wokwi)
![MQTT](https://img.shields.io/badge/Protocolo-MQTT-660066?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Alertas-Telegram-2CA5E0?style=for-the-badge&logo=telegram)

Este repositório contém um projeto completo de monitoramento residencial (Smart Home) usando múltiplos ESP32s (simulados no Wokwi) que publicam dados de sensores via MQTT.

Uma instância central do Node-RED atua como o cérebro do sistema, consumindo os dados MQTT para:
1.  Exibir um **dashboard** em tempo real.
2.  Enviar **alertas via Telegram** com base em limites pré-definidos.

## Arquitetura do Sistema

O fluxo de dados é simples e segue um padrão clássico de IoT:



1.  **Dispositivos (ESP32):** 4 dispositivos simulados no Wokwi leem sensores do ambiente.
2.  **Comunicação (MQTT):** Cada dispositivo publica seus dados em um tópico único no broker público `broker.hivemq.com`.
3.  **Processamento (Node-RED):** O Node-RED se inscreve em todos os tópicos, recebendo os dados assim que são publicados.
4.  **Ação (Dashboard & Alertas):** Os dados são processados para alimentar gráficos e verificar regras de alerta. Se uma regra for violada, uma notificação é enviada via Telegram.

---

## 1. Dispositivos ESP32 (Simulados no Wokwi)

Quatro simulações independentes no Wokwi atuam como nossos dispositivos de hardware. Para executar o projeto, você deve abrir cada link e iniciar a simulação (clicando no botão "Play" ▶️).

### Dispositivo 1: Monitor de Clima (Quarto 1)
* **Propósito:** Mede a temperatura e a umidade do ambiente.
* **Sensor:** `DHT22`
* **Tópico MQTT:** `meu_iot/quarto1/clima`
* **Formato dos Dados:** JSON (ex: `{"temperatura": 25.5, "umidade": 60.1}`)
* **Link do Wokwi:** **[Projeto Wokwi - Clima (DHT22)](https://wokwi.com/projects/447527871040940033)**

### Dispositivo 2: Monitor de Luz (Sala 1)
* **Propósito:** Mede a intensidade da luz ambiente e a converte para a unidade Lux.
* **Sensor:** `LDR` (Resistor Dependente de Luz)
* **Tópico MQTT:** `meu_iot/sala1/luz_lux`
* **Formato dos Dados:** String (ex: `"345.20"`)
* **Link do Wokwi:** **[Projeto Wokwi - Luz (LDR)](https://wokwi.com/projects/447510363373539329)**
    

### Dispositivo 3: Detector de Fumaça (Cozinha 1)
* **Propósito:** Envia um sinal digital de alerta (0 ou 1) se fumaça for detectada.
* **Sensor:** `MQ-2` (usando a saída Digital D0)
* **Tópico MQTT:** `meu_iot/cozinha1/fumaca_pinstate`
* **Formato dos Dados:** String (`"0"` = Fumaça Detectada, `"1"` = Ar Limpo)
* **Link do Wokwi:** **[Projeto Wokwi - Fumaça (MQ-2)](https://wokwi.com/projects/447522592649990145)**

### Dispositivo 4: Sensor de Distância (Garagem 1)
* **Propósito:** Mede a distância de um objeto, simulando um sensor de estacionamento.
* **Sensor:** `HC-SR04` (Sensor Ultrassônico)
* **Tópico MQTT:** `meu_iot/garagem1/distancia_cm`
* **Formato dos Dados:** String (ex: `"50.75"`)
* **Link do Wokwi:** **[Projeto Wokwi - Distância (HC-SR04)](https://wokwi.com/projects/447545124325102593)**

---

## 2. Central de Controle (Node-RED)

O cérebro do projeto é o fluxo do Node-RED, que está no arquivo `graphs.json` deste repositório. Ele é responsável pelo dashboard e pelos alertas.

### Dashboard de Monitoramento

O fluxo cria um dashboard completo (acessível em `http://IP_DO_NODE_RED:1880/ui`) dividido em quatro grupos:



* **Quarto 1:**
    * **Medidor de Temperatura:** Exibe o valor atual em °C.
    * **Medidor de Umidade:** Exibe o valor atual em %.
    * **Gráfico de Histórico:** Mostra a variação de temperatura e umidade ao longo da última hora.

* **Sala 1:**
    * **Medidor de Luminosidade:** Exibe o valor atual em Lux.
    * **Texto de Status:** Indica se está **"Dia"** (> 50 Lux) ou **"Noite"** (< 50 Lux).
    * **Gráfico de Histórico:** Mostra a variação de Lux ao longo da última hora.

* **Cozinha 1:**
    * **Texto de Status de Fumaça:** Exibe um alerta grande e colorido: **<font color="red">FUMAÇA DETECTADA!</font>** ou **<font color="green">Ar Limpo</font>**.
    * **Gráfico de Alerta:** Um gráfico de "degrau" (stepped) que mostra o histórico de alertas (0 para Alerta, 1 para OK).

* **Garagem 1:**
    * **Texto de Status de Proximidade:** Exibe **<font color="red">ALERTA: Próximo!</font>** (se < 100cm) ou **<font color="green">OK - Distância Segura</font>**.
    * **Medidor de Distância:** Mostra a distância atual (0-400cm). As cores do medidor mudam de verde para vermelho quando um objeto está a menos de 100cm.
    * **Gráfico de Histórico:** Mostra a variação da distância ao longo da última hora.

### Alertas com Telegram

O fluxo monitora ativamente todos os dados recebidos e envia notificações de alerta para um usuário específico no Telegram.

* **Alerta de Clima:** Se a Temperatura > 30°C **OU** Umidade < 25%.
* **Alerta de Luz:** Se a Luminosidade > 1000 Lux.
* **Alerta de Fumaça:** Se o status for `"0"` (Fumaça Detectada).
* **Alerta de Distância:** Se a distância for < 100 cm.

Para evitar spam, cada tipo de alerta é controlado por um nó `delay` (atraso) configurado em modo "Rate Limit", permitindo no máximo **1 mensagem por minuto** para cada categoria de alerta.

---

## Como Executar o Projeto

### Pré-requisitos

1.  **Node-RED Instalado:** Você precisa de uma instância do Node-RED funcionando.
2.  **Paletas do Node-RED:** Instale as seguintes paletas (Menu > Manage Palette > Install):
    * `node-red-dashboard`
    * `node-red-contrib-telegrambot`
3.  **Bot do Telegram:**
    * Crie um bot falando com o `@BotFather` no Telegram e salve o **Token da API**.
    * Encontre seu **Chat ID** pessoal falando com o `@userinfobot`.
    * **Importante:** Você deve enviar uma mensagem (ex: `/start`) para o seu bot *antes* que o Node-RED possa enviar mensagens para você.

### Passo 1: Iniciar as Simulações Wokwi

1.  Abra os 4 links dos projetos Wokwi listados acima.
2.  Inicie a simulação (clique no botão "Play" ▶️) em **todas** as 4 abas.
3.  Verifique os logs seriais no Wokwi para garantir que eles se conectaram ao WiFi e estão publicando no MQTT.

### Passo 2: Configurar e Importar o Fluxo do Node-RED

#### A. Configuração de Segurança (Variáveis de Ambiente)

Para manter seu Token do Telegram e seu Chat ID seguros, **não os escreva diretamente no fluxo**. Use as variáveis de ambiente do Node-RED.

1.  No seu Node-RED, vá em **Menu > Settings > Environment**.
2.  Clique em "+add" para adicionar duas variáveis:
    * `TELEGRAM_TOKEN`: Cole seu token do bot (ex: `123:ABC...`).
    * `chat_id`: Cole seu Chat ID (ex: `1473485665`).
3.  Clique em **Deploy**.
4.  **REINICIE O NODE-RED** (o processo/serviço) para que ele carregue as novas variáveis de ambiente.

#### B. Importar o Fluxo

1.  Copie o conteúdo do arquivo `graphs.json` deste repositório.
2.  No Node-RED, vá em **Menu > Import**.
3.  Cole o JSON e clique em **Import**.

#### C. Conectar o Bot do Telegram

1.  Após importar, encontre o nó de configuração do Telegram (azul claro) chamado `Tde1-paralela`.
2.  Dê um duplo clique nele.
3.  No campo **Token**, em vez de colar seu token, escreva: `$(TELEGRAM_TOKEN)`
4.  Clique em **Update** e depois em **Deploy**.

O Node-RED irá automaticamente usar o token salvo na variável de ambiente `TELEGRAM_TOKEN`. Os nós de função de alerta (ex: "Verificar Alerta Clima") já estão configurados para usar `env.get("chat_id")`, lendo o seu ID da variável de ambiente.