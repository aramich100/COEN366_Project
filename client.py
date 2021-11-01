import socket
import sys

client_host = '0.0.0.0'
client_port = 5556

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except socket.error:
    print("Failes to created socket")
    sys.exit()

s.bind((client_host, client_port))

host = 'localhost'
port = 5555


while (1):
    msg = input('Enter message to send: ')
    msg_bytes = str.encode(msg)

    try:
        s.sendto(msg_bytes, (host, port))
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print(reply)

    except socket.error.msg_bytes:
        print("Error")
