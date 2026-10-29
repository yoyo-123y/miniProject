import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto(
        "1,0,0,0,123".encode('utf-8'),
        ("127.0.0.1", 4220)
    )
    time.sleep(0.05)