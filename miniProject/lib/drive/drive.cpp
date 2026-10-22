#include <Arduino.h>
#include <stdlib.h>
#include <string.h>
#define A1A 1
#define A1B 2
#define B1A 3
#define B1B 4
int Motor_1[] = {0,0};
int Motor_2[] = {0,0};
int receivedData[2] = {0,0};
void parseReceivedData(char* data) {
    char* token = strtok(data, ",");
    int index = 0;
    while (token != NULL && index < 2) {
        receivedData[index] = atoi(token);
        token = strtok(NULL, ",");
        index++;
    }
}
void initMotors() {
    pinMode(A1A, OUTPUT);
    pinMode(A1B, OUTPUT);
    pinMode(B1A, OUTPUT);
    pinMode(B1B, OUTPUT);
}
void driveMotors(char* receivedData) {
    parseReceivedData((char*)receivedData);
    if(receivedData[0] > 0 && receivedData[1] > 0) {
        analogWrite(A1A, receivedData[0]);
        analogWrite(A1B, 0);
        analogWrite(B1A, receivedData[1]);
        analogWrite(B1B, 0);
    } else if(receivedData[0] < 0 && receivedData[1] < 0) {
        analogWrite(A1A, 0);
        analogWrite(A1B, -receivedData[0]);
        analogWrite(B1A, 0);
        analogWrite(B1B, -receivedData[1]);
    } else if(receivedData[0] > 0 && receivedData[1] < 0) {
        analogWrite(A1A, receivedData[0]);
        analogWrite(A1B, 0);
        analogWrite(B1A, 0);
        analogWrite(B1B, -receivedData[1]);
    } else if(receivedData[0] < 0 && receivedData[1] > 0) {
        analogWrite(A1A, 0);
        analogWrite(A1B, -receivedData[0]);
        analogWrite(B1A, receivedData[1]);
        analogWrite(B1B, 0);
    } else {
        analogWrite(A1A, 0);
        analogWrite(A1B, 0);
        analogWrite(B1A, 0);
        analogWrite(B1B, 0);
    }
}