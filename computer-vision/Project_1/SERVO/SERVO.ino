#include <WiFi.h>
#include <WiFiClient.h>
#include <ESP32Servo.h>

const char* ssid = "IphoneE";
const char* password = "fredo242001";
WiFiServer server(80);  // Puerto en el que el servidor escucha los comandos
Servo servo;

void setup() {
  Serial.begin(9600);
  delay(100);


  Serial.println("Conectando a WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  Serial.println("Conectado a WiFi");
  Serial.println(WiFi.localIP());
  server.begin();
  servo.setPeriodHertz(50); // Establecer el período del servo a 50 Hz
  servo.attach(12, 500, 2400);  // Conectar el servo al pin 2 con límites de pulso de 500-2400
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        Serial.print("SISISI");
        String comando = client.readStringUntil('\n');
        int index = comando.indexOf(',');
        String tipo_moneda = comando.substring(0, index);
        int grados = comando.substring(index + 1).toInt();

        if (tipo_moneda == "1000") {
          servo.write(0);
          delay(00);
          servo.write(0);
        } else if (tipo_moneda == "200") {
          servo.write(15);
          delay(2000);
          servo.write(0);  // Mover la moneda de $200 a 45 grados
        } else if (tipo_moneda == "500") {
          servo.write(25);
          delay(2000);
          servo.write(0);  // Mover la moneda de $500 a 60 grados
        } else if (tipo_moneda == "100") {
          servo.write(35);
          delay(2000);
          servo.write(0);  // Mover la moneda de $100 a 75 grados
        } else if (tipo_moneda == "50") {
          servo.write(50);
          delay(2000);
          servo.write(0);  // Mover la moneda de 50 centavos a 90 grados
        }
      else {   
        Serial.print("listo");
        }
      }
    }
  }
}
