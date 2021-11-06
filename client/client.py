import os
import socket


IP = socket.gethostbyname('127.0.0.1')
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def main():
    print(" -- WELCOME CLIENT --")

    while 1:
        print(" Please enter a command. ")
        inInput = input(">>  ")

        #ADR = ("127.0.0.1", 4455)
        #admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # admin.connect(ADR)

        if inInput == "REGISTER":
            name = input("Name :  ")
            IP = input("IP :  ")
            UDPPort = int(input("UDP Port : "))
            TCPPort = int(input("TCP Port : "))
            ADR = (IP, TCPPort)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADR)

            send_data = "REGISTER"
            send_data += "@"+name
            send_data += "@"+str(IP)
            send_data += "@"+str(UDPPort)
            send_data += "@"+str(TCPPort)

            client.send(send_data.encode(FORMAT))

            print(" Please enter a command. ")
            inInput = input(">>  ")
            if inInput == "DE-REGISTER":
                name = input("Name :  ")
                send_data = "DE-REGISTER"
                send_data += "@"+name
                client.send(send_data.encode(FORMAT))
                client.close()

    #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # client.connect(ADDR)

    while 1:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        # REGISTER@RQ

        if cmd == "OK":
            print(f"{msg}")

        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break

        data = input(">  ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "UPLOAD":
            # UPLOAD FILE NAME
            path = data[1]
            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

        elif cmd == "REGISTER":
            send_data = cmd
            registerCmd = input(
                "To register, enter: YourName IPaddress UDPsocket# TCPsocket#\n")
            words = registerCmd.split()
            clientName = words[0]
            #clientIP = words[1]
            #clientUDP = words[2]
            #clientTCP = words[3]

            # print(clientName)
            send_data += "@"+clientName
            # print(f"{send_data}")

            client.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode())

    print("Disconnected from the server. ")
    client.close()


if __name__ == "__main__":
    main()
