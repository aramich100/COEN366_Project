# OS and Socket Imports
import os
import sys
import socket
import threading

# For Color in Terminal
from colorama import Fore, Back, Style

# IP, PORT
IP = socket.gethostbyname('127.0.0.1')
PORT = 4466


ADDR = (IP, PORT)  # Adress Binding
SIZE = 1024  # Bytes
FORMAT = "utf-8"  # Text Format

UDPPort = 0
TCPPort = 0


# Main Function
def main(TCPPort, IP, name, FORMAT):

    print('\033[1m', Fore.BLUE + " \n \n - 🍆 - WELCOME CLIENT  - 🍆 - \n \n")

    print(Style.RESET_ALL)  # Reset text
    while 1:
        print(" Please enter a command. ")  # User Text Input
        inInput = input("  ⫸    ")

        if inInput == "REGISTER":  # If user inputs "REGISTER"
            print()
            UDPPort = int(input("UDP Port : "))  # User Inputs UDP Port
            ADR = (IP, UDPPort)  # Adresse Binding
            # Creating a socker for client
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Forming message to be sent to server
            send_data = "REGISTER"  # Command
            send_data += "@"+name
            send_data += "@"+str(IP)
            send_data += "@"+str(UDPPort)
            send_data += "@"+str(TCPPort)

            # Sending message to server
            client.sendto(send_data.encode("utf-8"), ADR)
            print("Register sent. Waiting..")

            # Receving response from server
            data, addr = client.recvfrom(1024)
            data = data.decode("utf-8")
            cmd, msg = data.split("@")  # Splitting Response : "CMD@MSG"
            print("Received command")

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
                        client.sendto(send_data.encode(FORMAT), ADR)

                        # Waiting for response
                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        print("data : ", data)
                        cmd, msg = data.split("@")
                        # If De-Registered was succesfull
                        if cmd == "OK":
                            client.close()
                            break

                    elif inInput == "RETRIEVE-ALL":
                        send_data = "RETRIEVE-ALL"
                        # client.send(send_data.encode(FORMAT))
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data = client.recvfrom(1024).decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(msg)

                    elif inInput == "RETRIEVE-INFOT":
                        send_data = "RETRIEVE-INFOT"
                        name = input("Name :  ")
                        # Sending to server
                        send_data += "@"+name
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data = client.recvfrom(1024).decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print("\n"+msg)

                    elif inInput == "PUBLISH":  # Publish a file

                        name = input("Name : ")

                        # Sending to server
                        send_data = "PUBLISHREJ@"+name
                        client.sendto(send_data.encode(FORMAT), ADR)

                        # Waiting for response to see if Name is in List of Clients in the server
                        rejInfo, addr = client.recvfrom(1024)
                        rejInfo = rejInfo.decode(FORMAT)
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
                                filename = p.split("/")[-1]
                                send_data = f"{inInput}@{name}@{filename}"
                                print("sending : ", send_data)
                                client.sendto(send_data.encode(FORMAT), ADR)

                                data, addr = client.recvfrom(1024)
                                data = data.decode(FORMAT)
                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)
                        else:  # User not in list of clients
                            print("PUBLISH-DENIED", mess)

                    elif inInput == "REMOVE":  # Remove
                        name = input("Name : ")
                        send_data = "REMOVEREJ@"+name
                        client.sendto(send_data.encode(FORMAT), ADR)
                        send_data = ""

                        rejInfo, addr = client.recvfrom(1024)
                        rejInfo = rejInfo.decode(FORMAT)
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
                                send_data = "REMOVE@"+name+"@"+str(p)
                                client.sendto(send_data.encode(FORMAT), ADR)
                                print("197: ", send_data)
                                data, addr = client.recvfrom(1024)
                                data = data.decode(FORMAT)
                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)

                        else:
                            print("REMOVE-DENIED #", mess)

                    elif inInput == "LIST":  # Lists available files in server directory

                        print()
                        send_data = "LIST"
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data = client.recvfrom(1024).decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(f"{msg}")
                        print()

                    elif inInput == "DOWNLOAD":
                        clientIP = input("Enter the desired clients IP:  ")
                        clientPort = input("Enter the desired clients Port:  ")
                        fileName = input(
                            "Enter the file you wish to download:  ")
                        ADR = (clientIP, int(clientPort))  # Adress Binding
                        FORMAT = "utf-8"  # Text Format
                        client = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
                        client.connect(ADR)  # Connecting to server

                        send_data = "DOWNLOAD@"
                        send_data += str(fileName)
                        client.send(send_data.encode(FORMAT))

                        data = client.recv(SIZE).decode(FORMAT)
                        data = data.split("@")

                        cmd = data[0]

                        if cmd == "FILE":
                            name, text = data[1], data[2]
                            filepath = os.path.join("./", name)
                            with open(filepath, "w") as f:  # opening the file
                                f.write(text)  # writing to a file the text
                                # Print file received by server
                                print(" 📁 File Received : ", filepath)
                                # Tell client that it was puiblished successfully

                        else:
                            print(data)

            elif cmd == "DISCONNECTED":
                print(f"{msg}")


def handle_client(conn, addr):
    data = conn.recv(SIZE).decode(FORMAT)
    data = data.split("@")

    files = os.listdir("./")  # List of files in current directory
    p = data[1]  # File name

    if p in files:
        with open(f"{p}", "r") as f:
            text = f.read()
        filename = p.split("/")[-1]
        command = "FILE"
        # Sends file to server
        send_data = f"{command}@{filename}@{text}"
        conn.sendto(send_data.encode(FORMAT), addr)
        #print(" [ DONE SENDING ] ")

    elif p not in files:
        send_data = "DOWNLOAD-ERROR@"+str(data[1]) + "@File does not exist"
        conn.sendto(send_data.encode(FORMAT), addr)

    #print("... Closing Thread ...")
    sys.exit()


def waitClient(TCPPort, IP):
    ADRC = (IP, TCPPort)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADRC)  # Bind the Ip and the Port
    server.listen()  # Listen for a client
    while 1:
        conn, addr = server.accept()  # Accepting a client
        thread = threading.Thread(target=handle_client, args=(
            conn, addr))  # Making a client a thread
        thread.start()  # Starting the thread and connecting the client


if __name__ == "__main__":
    name = input("Name :  ")  # User Inputs Name
    IP = input("IP :  ")  # User Inputs IP
    TCPPort = int(input("TCP Port : "))  # User Inputs TCP Port
    FORMAT = "utf-8"
    thread = threading.Thread(target=waitClient, args=(
        TCPPort, IP))  # Making a client a thread
    thread.start()
    main(TCPPort, IP, name, FORMAT)
