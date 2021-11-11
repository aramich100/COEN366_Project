# OS and Socket Imports
import os
import socket

# For Color in Terminal
from colorama import Fore, Back, Style

# IP, PORT
IP = socket.gethostbyname('127.0.0.1')
PORT = 4466


ADDR = (IP, PORT)  # Adress Binding
SIZE = 1024  # Bytes
FORMAT = "utf-8"  # Text Format


# Main Function
def main():

    print('\033[1m', Fore.BLUE + " \n \n - 🍆 - WELCOME CLIENT  - 🍆 - \n \n")

    while 1:
        print(Style.RESET_ALL)  # Reset text

        print(" Please enter a command. ")  # User Text Input
        inInput = input("  ⫸    ")

        if inInput == "REGISTER":  # If user inputs "REGISTER"
            print()
            name = input("Name :  ")  # User Inputs Name
            IP = input("IP :  ")  # User Inputs IP
            UDPPort = int(input("UDP Port : "))  # User Inputs UDP Port
            TCPPort = int(input("TCP Port : "))  # User Inputs TCP Port
            ADR = (IP, TCPPort)  # Adresse Binding

            # Creating a socker for client
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADR)  # Connecting to server

            # Forming message to be sent to server
            send_data = "REGISTER"  # Command
            send_data += "@"+name
            send_data += "@"+str(IP)
            send_data += "@"+str(UDPPort)
            send_data += "@"+str(TCPPort)

            # Sending message to server
            client.send(send_data.encode(FORMAT))

            # Receving response from server
            data = client.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")  # Splitting Response : "CMD@MSG"

            if cmd == "RD":  # Register Denined
                print(Fore.RED + "\n  " + msg)
                print(Style.RESET_ALL)

            if cmd == "OK":  # Register OK

                print()
                print(Fore.GREEN + msg)
                print(Style.RESET_ALL)

                # Once user is registered, it will loop again waiting for commands.
                while 1:

                    print(" \n Please enter a command. ")
                    inInput = input("  ⫸    ")

                    if inInput == "DE-REGISTER":  # De-Register
                        name = input("Name :  ")

                        # Sending to server
                        send_data = "DE-REGISTER"
                        send_data += "@"+name
                        client.send(send_data.encode(FORMAT))

                        # Waiting for response
                        data = client.recv(SIZE).decode(FORMAT)
                        cmd, msg = data.split("@")

                        # If De-Registered was succesfull
                        if cmd == "OK":
                            client.close()
                            break
                    elif inInput == "RETRIEVE-ALL":
                        send_data = "RETRIEVE-ALL"
                        client.send(send_data.encode(FORMAT))

                        data = client.recv(SIZE).decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(msg)

                    elif inInput == "PUBLISH":  # Publish a file

                        name = input("Name : ")

                        # Sending to server
                        send_data = "PUBLISHREJ@"+name
                        client.send(send_data.encode(FORMAT))

                        # Waiting for response to see if Name is in List of Clients in the server
                        rejInfo = client.recv(SIZE).decode(FORMAT)
                        cmd, mess = rejInfo.split("@")

                        if cmd == "GOOD":  # User can Publish files

                            listOfFiles = []
                            fileCount = 0

                            print(
                                "Enter the desired file name and extension (file.txt)")
                            print(
                                "Enter 0 when you have completed entering all files.")

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
                                with open(f"{p}", "r") as f:
                                    text = f.read()
                                filename = p.split("/")[-1]
                                # Sends file to server
                                send_data = f"{inInput}@{filename}@{text}"
                                client.send(send_data.encode(FORMAT))

                                data = client.recv(SIZE).decode(FORMAT)
                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)
                        else:  # User not in list of clients
                            print("PUBLISH-DENIED", mess)

                    elif inInput == "REMOVE":  # Remove
                        name = input("Name : ")
                        send_data = "REMOVEREJ@"+name
                        client.send(send_data.encode(FORMAT))

                        rejInfo = client.recv(SIZE).decode(FORMAT)
                        cmd, mess = rejInfo.split("@")

                        if cmd == "GOOD":  # If user can Remove a file
                            listOfFiles = []
                            fileCount = 0

                            print(
                                "Enter the desired file name and extension (file.txt)")
                            print(
                                "Enter 0 when you have completed entering all files.")

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
                                send_data = "REMOVE@"+str(p)
                                client.send(send_data.encode(FORMAT))

                                data = client.recv(SIZE).decode(FORMAT)

                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)

                        else:
                            print("REMOVE-DENIED #", mess)

                    elif inInput == "LIST":  # Lists available files in server directory
                        print()
                        send_data = "LIST"
                        client.send(send_data.encode(FORMAT))

                        data = client.recv(SIZE).decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(f"{msg}")
                        print()
                        # else: break because user wasnt registered (DENIED)

            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break


if __name__ == "__main__":
    main()
