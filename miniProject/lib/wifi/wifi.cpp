#include <stdlib.h>
#include <string.h>
#include <WiFi.h>
#include <WiFiUdp.h>
const char* ssid = "router";
const char* password = "123456789";
const int UDP_PORT = 4210;
IPAddress local_IP(192, 168, 1, 200);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);
WiFiUDP udp;
char packet[256];
int initWifi(){
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS)) {
        Serial.println("Static IP configuration failed!");
        return -1;
    }
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to WiFi");
    udp.begin(UDP_PORT);
    return 0;
}
char* receiveUdpPacket() {
    int packetSize = udp.parsePacket();
    if (packetSize) {
        int len = udp.read(packet, sizeof(packet) - 1);
        if (len > 0) {
            packet[len] = '\0';
        }
        return packet;
    }
    return NULL;
}
int checkWifiConnection() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection lost. Attempting to reconnect...");
        WiFi.disconnect();
        WiFi.begin(ssid, password);
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 10) {
            delay(500);
            Serial.print(".");
            attempts++;
        }
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("Reconnected to WiFi");
            return 0;
        } else {
            Serial.println("Failed to reconnect to WiFi");
            return -1;
        }
    }
    return 0;
}
void restartUdp() {
    udp.stop();
    udp.begin(UDP_PORT);
    Serial.println("UDP server restarted");
}
int checkPacketSize() {
    int packetSize = udp.parsePacket();
    if (packetSize > 0) {
        return packetSize;
    }
    return 0;
}