from threading import Thread
import time
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 8050

def print_total(totals):
    interval = 1
    running = True
    last_read = totals[0]
    while running:
        current_read = totals[0]
        if (delta := current_read - last_read) > 0:
            bytes_sec = delta // interval
            bits_sec = bytes_sec * 8
            print(f"Received: {bytes_sec:,} B/s ({bits_sec:,} bit/s)")
            last_read = current_read
        time.sleep(interval)


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
