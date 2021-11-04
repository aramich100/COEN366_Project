import os
import socket
import threading

IP = socket.gethostbyname('127.0.0.1')
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected. ")
    conn.send("OK@Welcome to the File Server ".encode(FORMAT))

    while 1:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"
            send_data += "LIST: List all the files from the server. \n"
            send_data += "UPLOAD <path>: Upload a file to the server \n"
            send_data += "DELETE <filepath>: Delete a file from the server \n"
            send_data += "LOGOUT : Disconnect from the server \n"
            send_data += "HELP : List all the commands. \n"

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break

        elif cmd == "LIST":
            pass

        elif cmd == "UPLOAD":
            pass

        elif cmd == "DELETE":
            pass

        print(f"[DISCONNECTED] {addr} disconencted")


def main():
    print("[STARTING] Server is starting. ")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[Listening] Server is listening. ")

    while 1:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
