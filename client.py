import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step


host = "172.30.119.48"

port = 5001

# the name of file we want to send, make sure it exists
filename = "t.txt"
# get the file size
filesize = os.path.getsize(filename)

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")


s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(
    filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break

        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

s.close()
