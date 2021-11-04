import os
import socket
import threading

IP = socket.gethostbyname('127.0.0.1')  # LOCALHOST
PORT = 4467
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

SERVER_DATA_PATH = "./"


def handle_client(conn, addr):
    # Server Acknolowdges new connection
    print(f"[NEW CONNECTION] {addr} connected. ")

    # Sends OK Command to client
    conn.send("OK@Welcome to the File Server ".encode(FORMAT))

    while 1:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")

        # CMD@MSG
        # data[0] = CMD
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"  # OK Command to client
            send_data += "LIST: List all the files from the server. \n"
            send_data += "FIND <filepath> : Finds specified file \n"
            send_data += "DELETE <filepath>: Delete a file from the server \n"
            send_data += "DISC : Disconnect from the server \n"
            send_data += "HELP : List all the commands. \n"
            conn.send(send_data.encode(FORMAT))

        # Disconnect client from server
        elif cmd == "DISC":
            break

        # List files in server
        elif cmd == "LIST":
            files = os.listdir("./")
            send_data = "OK@"
            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            pass

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm{SERVER_DATA_PATH}/{filename}")

        elif cmd == "REGISTERED":
            send_data = "OK@"
            send_data += "Registered succesfully"
            print("Registered succesfully")
            conn.send(send_data.encode(FORMAT))

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
