import socket
import time
import os
import sys


HOST = '0.0.0.0'
PORT = 5555


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("socket created")

except socket.error.msg:
    print("error")
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error.msg:
    print("Bind fialed, Error code ")
    sys.exit()

print("Socket bind complete")


while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break

    print(data)

    reply = 'ok, ' + data

    s.sendto(reply, addr)


s.close()
