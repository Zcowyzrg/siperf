
import argparse
import socket
import time

UDP_PORT = 8050
BANDWIDTH = 10e6
MSG_SIZE = 1400
FLOOD_TIME = 10

parser = argparse.ArgumentParser( description='Sends controlled flood of UDP packets')
parser.add_argument('ip_address', help='Destination IP address')
parser.add_argument('-p', '--port', help=f'Destination port, default={UDP_PORT}',
                    default=UDP_PORT)
parser.add_argument('-b', '--bandwidth',
                    help=f'Target bandwidth in bits/s, default={BANDWIDTH}',
                    default=BANDWIDTH, type=int)
parser.add_argument('-s', '--msg_size', help=f'Datagram size, default={MSG_SIZE}',
                    default=MSG_SIZE, type=int)
parser.add_argument('-t', '--time', help=f'Flood time, default={FLOOD_TIME}',
                    default=FLOOD_TIME, type=int)

args = parser.parse_args()

MESSAGE = bytearray(args.msg_size)
SEND_HZ = 10
SEND_INTERVAL = 1 / SEND_HZ
SEND_ONCE = int(args.bandwidth / 8 / SEND_HZ // args.msg_size)

print(f'Destination IP={args.ip_address} PORT={args.port}')
print(f'BANDWIDTH={args.bandwidth:,} SIZE={args.msg_size}')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# TODO bind source address
t_end = time.time() + args.time

while time.time() < t_end:
    sent_per_second = 0
    for tick in range(SEND_HZ):
        t0 = time.time()
        for i in range(SEND_ONCE):
            sock.sendto(MESSAGE, (args.ip_address, args.port))
            sent_per_second += args.msg_size
        t1 = time.time()
        if (delta := t1 - t0) < (SEND_INTERVAL):
            time.sleep(SEND_INTERVAL - delta)
        else:
            print("SLOW")
    print(f'Sent: {sent_per_second:,}')
