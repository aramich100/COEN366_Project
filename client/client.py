import os
import socket

from colorama import Fore, Back, Style
import emoji

IP = socket.gethostbyname('127.0.0.1')
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def main():
    # BOLD, EMOJI, COLOR
    print('\033[1m', Fore.BLUE + " \n \n - 🍆 - WELCOME CLIENT  - 🍆 - \n \n")

    while 1:
        print(Style.RESET_ALL)
        print(" Please enter a command. ")
        inInput = input("  ⫸    ")

        # If Client is Registered or tries to
        if inInput == "REGISTER":
            print()
            name = input("Name :  ")
            IP = input("IP :  ")
            UDPPort = int(input("UDP Port : "))
            TCPPort = int(input("TCP Port : "))
            ADR = (IP, TCPPort)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADR)

            # Forming message to be sent to server
            send_data = "REGISTER"
            send_data += "@"+name
            send_data += "@"+str(IP)
            send_data += "@"+str(UDPPort)
            send_data += "@"+str(TCPPort)

            # Sending message to server
            client.send(send_data.encode(FORMAT))

            data = client.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")

            # REGISTER@RQ
            if cmd == "RD":
                print(Fore.RED + "\n  " + msg)
                print(Style.RESET_ALL)

            if cmd == "OK":
                print()
                print(Fore.GREEN + msg)
                print(Style.RESET_ALL)
                while 1:
                    # If server replied "OK" :
                    print(" \n Please enter a command. ")
                    inInput = input("  ⫸    ")
                    if inInput == "DE-REGISTER":
                        name = input("Name :  ")
                        send_data = "DE-REGISTER"
                        send_data += "@"+name
                        client.send(send_data.encode(FORMAT))
                        data = client.recv(SIZE).decode(FORMAT)
                        cmd, msg = data.split("@")
                        if cmd == "OK":
                            client.close()
                            break

                    elif inInput == "PUBLISH":
                        name = input("Name : ")
                        send_data = "PUBLISH@" + name
                        client.send(send_data.encode(FORMAT))
                        print("Waiting for reply..")
                        data = client.recv(SIZE).decode(FORMAT)
                        if(data == "OKCLIENT"):
                            print("Client good")

                        listOfFiles = []
                        fileCount = 0
                        print("Enter the desired file name and extension (file.txt)")
                        print("Enter 0 when you have completed entering all files.")
                        while 1:
                            fileName = input("/ ")
                            if fileName == "0":
                                print(Fore.BLUE +
                                      "\n Total Files Selected : ", fileCount)
                                print(Style.RESET_ALL)
                                break

                            listOfFiles.append(fileName)
                            fileCount += 1

                        for p in listOfFiles:
                            print("1")
                            with open(f"{p}", "r") as f:
                                text = f.read()
                                print("2")
                            filename = p.split("/")[-1]
                            print("3")
                            # Sends file to server
                            send_data = f"{inInput}@{filename}@{text}"
                            print("4")
                            client.send(send_data.encode(FORMAT))
                            print("5")
                            data = client.recv(SIZE).decode(FORMAT)
                            print("6")

                            cmd, msg = data.split("@")
                            print(cmd)
                            if cmd == "OK":
                                print(msg)

                    # Lists available files
                    elif inInput == "LIST":
                        print()
                        send_data = "LIST"
                        client.send(send_data.encode(FORMAT))
                        data = client.recv(SIZE).decode(FORMAT)
                        cmd, msg = data.split("@")
                        if cmd == "OK":
                            # print("Files")
                            print(f"{msg}")
                        print()
                        # else: break because user wasnt registered (DENIED)

            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break

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
