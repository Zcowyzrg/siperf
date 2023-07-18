from threading import Thread
import time
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8050

def print_total(totals):
    interval = 1
    running = True
    last_read = totals[0]
    while running:
        current_read = totals[0]
        delta =  current_read - last_read
        if delta > 0:
            print("Received: {} b/s".format(delta // interval))
            last_read = current_read
        time.sleep(1)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening on {}:{}".format(UDP_IP, UDP_PORT))

data_buffer = bytearray(2048)
total_received = [0]

th = Thread(target=print_total, args=[total_received])
#th.run() # check function
#sys.exit(0)
th.start()

while True:
    nbytes, addr = sock.recvfrom_into(data_buffer, 2048)
    #print("Received message: %s" % data_buffer[:nbytes])
    total_received[0] += nbytes

th.join()
