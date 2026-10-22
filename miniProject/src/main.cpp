#include <Arduino.h>
#include "wifi.h"
#include "drive.h"
float lastMessageTime = 0;
void setup() {
  initWifi();
  Serial.begin(115200);
  initMotors();
}

void loop() {
  if (checkWifiConnection() != 0) {
    Serial.println("Failed to reconnect to WiFi");
  }
  char* packet = receiveUdpPacket();
  if (packet != NULL) {
    Serial.print("Received UDP packet: ");
    Serial.println(packet);
    driveMotors(packet);
  }
  if (millis() - lastMessageTime > 5000) {
    restartUdp();
    lastMessageTime = millis();
  }
  if (millis() - lastMessageTime > 20000) {
    checkWifiConnection();
    restartUdp();
    lastMessageTime = millis();
  }
}