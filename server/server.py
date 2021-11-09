import os
import socket
import threading
import string

from colorama import Fore, Back, Style

IP = socket.gethostbyname('127.0.0.1')  # LOCALHOST
PORT = 5555
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

clients = []

SERVER_DATA_PATH = "./"


def handle_client(conn, addr):
    # Server Acknolowdges new connection

    # Sends OK Command to client
    # conn.send("OK@Welcome to the COEN366 Project Terminal. First, you will need to register. Enter the command: REGISTER".encode(FORMAT))

    clientCount = 0

    while 1:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"  # OK Command to client
            send_data += "LIST: List all the files from the server. \n"
            send_data += "FIND <filepath> : Finds specified file \n"
            send_data += "DELETE <filepath>: Delete a file from the server \n"
            send_data += "DISC : Disconnect from the server \n"
            send_data += "HELP : List all the commands. \n"
            conn.send(send_data.encode(FORMAT))

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

        elif cmd == "PUBLISHREJ":
            name = data[1]

            if name in clients:
                send_data = "GOOD@"
                send_data += str(addr[1])
                conn.send(send_data.encode(FORMAT))

            else:
                send_data = "NOTOK@"
                send_data += str(addr[1])

                conn.send(send_data.encode(FORMAT))
                print(" PUBLISH-DENIED #", addr[1])

        elif cmd == "REMOVEREJ":
            name = data[1]

            if name in clients:
                send_data = "GOOD@"
                send_data += str(addr[1])
                conn.send(send_data.encode(FORMAT))

            else:
                send_data = "NOTOK@"
                send_data += str(addr[1])
                conn.send(send_data.encode(FORMAT))
                print(" REMOVE-DENIED #", addr[1])

        elif cmd == "PUBLISH":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)
                print(" 📁 File Received : ", filepath)
                send_data = "OK@PUBLISHED #"+str(addr[1])
                conn.send(send_data.encode(FORMAT))

        elif cmd == "REMOVE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = str(data[1])
            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.remove("./"+filename)
                    send_data += "REMOVED #"+str(addr[1])
                    conn.send(send_data.encode(FORMAT))
        elif cmd == "REGISTER":
            clientCount += 1
            if data[1] not in clients:
                send_data = "OK@"
                send_data += "REGISTERED # " + str(addr[1])
                conn.send(send_data.encode(FORMAT))

                name = data[1]
                IP = data[2]
                UDP = data[3]
                TCP = data[4]
                print(f" 🚨 [ NEW CONNECTION ] {addr} connected. ")
                print(data[0], ' ', '#', addr[1], ' ', data[1],
                      ' ', data[2], ' ', data[3], ' ', data[4])
                clientString = str(data[1])
                # Adds client to list
                clients.append(clientString)

            else:
                send_data = "RD@"
                send_data += "REGISTER-DENIED  # " + \
                    str(addr[1]) + " Clients name is already in use. "
                conn.send(send_data.encode(FORMAT))
                clients.remove(data[1])
                break

        elif cmd == "DE-REGISTER":
            clientCount -= 1

            if name in clients:
                clients.remove(name)
                send_data = "OK@"
                send_data += "De-Registered successfully"
                name = data[1]
                print("[DE-REGISTERED] ", str(addr), " ", str(data[1]))
                conn.send(send_data.encode(FORMAT))
                break
            else:
                print("That client is not connected. Please try again !")
                send_data = "NO@"
                conn.send(send_data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    print('\033[1m', Fore.CYAN + " \n \n - 💻 - WELCOME SERVER  - 💻 - \n \n")
    print("[STARTING] Server is starting. ")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[Listening] Server is listening. \n \n")

    while 1:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
