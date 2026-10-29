#include <Arduino.h>
#include <stdlib.h>
#include <string.h>

#define A1A 1
#define A1B 2
#define B1A 3
#define B1B 4
#define C1A 5
#define C1B 6
#define D1A 7
#define D1B 8

int receivedData[4] = {0, 0, 0, 0};

void parseReceivedData(char* data) {
    char* token = strtok(data, ",");
    int index = 0;

    while (token != NULL && index < 4) {
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
    pinMode(C1A, OUTPUT);
    pinMode(C1B, OUTPUT);
    pinMode(D1A, OUTPUT);
    pinMode(D1B, OUTPUT);
}

void driveMotor(int pinA, int pinB, int speed) {
    speed = constrain(speed, -255, 255);

    if (speed > 0) {
        analogWrite(pinA, speed);
        analogWrite(pinB, 0);
    }
    else if (speed < 0) {
        analogWrite(pinA, 0);
        analogWrite(pinB, -speed);
    }
    else {
        analogWrite(pinA, 0);
        analogWrite(pinB, 0);
    }
}

void driveMotors(char* data, int distance) {
    parseReceivedData(data);
    if (distance < 2) {
        receivedData[0] = constrain(receivedData[0], -255, 10);
        receivedData[1] = constrain(receivedData[1], -255, 10);
        receivedData[2] = constrain(receivedData[2], -255, 10);
        receivedData[3] = constrain(receivedData[3], -255, 10);
        return;
    }
    // up-right, up-left, down-right, down-left
    driveMotor(A1A, A1B, receivedData[0]);
    driveMotor(B1A, B1B, receivedData[1]);
    driveMotor(C1A, C1B, receivedData[2]);
    driveMotor(D1A, D1B, receivedData[3]);
}