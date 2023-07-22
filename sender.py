
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 8050
MSG_SIZE = 1200
MESSAGE = bytearray(MSG_SIZE)
BANDWIDTH = 1.5e9 / 8
TOTAL_BYTES = BANDWIDTH * 5
SEND_HZ = 10
SEND_INTERVAL = 1 / SEND_HZ

# TODO bind
print(f"UDP target IP: {UDP_IP} PORT: {UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SEND_ONCE = int(BANDWIDTH / SEND_HZ // MSG_SIZE)
total_sent = 0

while total_sent < TOTAL_BYTES:
    for h in range(SEND_HZ):
        t0 = time.time()
        for i in range(SEND_ONCE):
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            total_sent += MSG_SIZE
        t1 = time.time()
        if (delta := t1 - t0) < (SEND_INTERVAL):
            time.sleep(SEND_INTERVAL - delta)
        else:
            print("SLOW")

