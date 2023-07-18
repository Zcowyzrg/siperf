
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8050
MESSAGE = b"Hello, World!"

# TODO bind

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE.decode('utf-8'))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
for i in range(3):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
