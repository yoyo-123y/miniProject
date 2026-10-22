#ifndef WIFI_H
#define WIFI_H

#include <Arduino.h>

int initWifi();
char* receiveUdpPacket();
int checkWifiConnection();
void restartUdp();
int checkPacketSize();

#endif