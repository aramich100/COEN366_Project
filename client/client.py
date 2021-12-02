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


def clear(): return os.system('cls')


def printGreen(m):
    print()
    print(Fore.GREEN + m)  # Formatting
    print(Style.RESET_ALL)


def main(TCPPort, IP, name, FORMAT):  # Main Function
    print('\033[1m', Fore.BLUE +
          " \n \n -- WELCOME CLIENT! Enter 'REGISTER' to begin!  -- \n \n")
    print(Style.RESET_ALL)  # Reset text style

    while 1:
        print(" Please enter a command. ")  # asking user to input a command
        inInput = input("  ⫸    ")

        if inInput == "REGISTER":  # If user inputs "REGISTER"
            # storing the udp port entered by the user
            UDPPort = int(input("\n Servers UDP Port : "))
            ADR = (IP, UDPPort)  # Address Binding
            # Creating a socket for client
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(2)

            # Forming message to be sent to server
            send_data = "REGISTER"  # Command
            send_data += "@"+name  # users name
            send_data += "@"+str(IP)  # users ip
            send_data += "@"+str(UDPPort)  # upd port
            send_data += "@"+str(TCPPort)  # tcp port

            try:  # Sending message to server
                # sedning the address to the server
                client.sendto(send_data.encode(FORMAT), ADR)
                data, addr = client.recvfrom(1024)
            except socket.timeout as e:
                exit(e)

            data = data.decode("utf-8")  # Receving response from server
            cmd, msg = data.split("@")  # Splitting Response ex) "CMD@MSG"

            if cmd == "RD":  # Register Denied
                print(Fore.RED + "\n  " + msg)
                print(Style.RESET_ALL)

            if cmd == "OK":  # If servers cmd was OK
                print()
                print(Fore.GREEN + msg)  # Formatting
                print(Style.RESET_ALL)

                while 1:  # Once user is registered, it will loop again waiting for commands.
                    # waiting for nect commands after register
                    print(" \n Please enter a command. ")
                    inInput = input("\t⫸    ")

                    if inInput == "DE-REGISTER":  # if command is De-Register
                        send_data = "DE-REGISTER"
                        send_data += "@"+name
                        # sending data to server
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":  # If De-Registered was successful
                            client.close()
                            break

                    elif inInput == "RETRIEVE-ALL":  # if command is retrive all
                        send_data = "RETRIEVE-ALL"
                        # send the command to server
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(msg)

                    elif inInput == "RETRIEVE-INFOT":  # if the command is retrieve-infot
                        send_data = "RETRIEVE-INFOT"

                        # Enter name of client info is desired
                        name = input("Name :  ")

                        send_data += "@"+name
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print("\n"+msg)

                    elif inInput == "PUBLISH":  # if command is to Publish a file

                        send_data = "PUBLISHREJ@"+name
                        try:
                            client.sendto(send_data.encode(FORMAT), ADR)
                            client.settimeout(5)
                        except socket.timeout:
                            client.close
                            break

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

                                try:
                                    client.sendto(
                                        send_data.encode(FORMAT), ADR)
                                    client.settimeout(5)
                                except socket.timeout:
                                    client.close
                                    break

                                data, addr = client.recvfrom(1024)
                                data = data.decode(FORMAT)
                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)

                                else:
                                    print(msg)
                        else:  # User not in list of clients
                            print("PUBLISH-DENIED", mess)

                    elif inInput == "REMOVE":  # Remove
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
                                data, addr = client.recvfrom(1024)
                                data = data.decode(FORMAT)
                                cmd, msg = data.split("@")

                                if cmd == "OK":
                                    print(msg)

                                else:
                                    print("REMOVE-DENIED #", msg)

                        else:  # if file doesnt exist
                            print("REMOVE-DENIED #", mess)

                    elif inInput == "UPDATE-CONTACT":  # UPDATES CONTACT
                        # client enter new ip
                        updateIP = input("Enter your new IP : ")
                        # client enters new udp socket
                        updateUDP = input("Enter your new UDP Socket : ")
                        updateTCP = TCPPort

                        b = " "
                        while((b != "0") and (b != "1")):
                            b = input(
                                "\nWould you like to update your TCP Socket? \n You will be disconnected from all existing connectiong. \n 0 (NO) 1 (YES) : ")

                        if(b == "1"):
                            updateTCP = input("Enter your new TCP Socket : ")

                        send_data = "UPDATE-CONTACT@" + name+"@" + \
                            str(updateIP)+"@"+str(updateUDP)+"@"+str(updateTCP)
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            m = "\n UPDATE-CONFIRMED  #" + str(msg)
                            printGreen(m)
                        else:
                            print(Fore.RED + "\n UPDATE-DENIED #", msg)
                            print(Style.RESET_ALL)

                    elif inInput == "SEARCH-FILE":  # if client wants to search for a file
                        fn = input("File to search :  ")

                        send_data = "SEARCH-FILE@"
                        # send the file tha wants to be searched
                        send_data += str(fn)
                        client.sendto(send_data.encode(FORMAT), ADR)

                        data, addr = client.recvfrom(1024)
                        data = data.decode(FORMAT)
                        cmd, msg = data.split("@")

                        if cmd == "OK":
                            print(msg)
                        elif cmd == "NOTOK":  # if the search file didnt work
                            print(Fore.RED + "\n SEARCH-ERROR #",
                                  str(addr[1]), msg)
                            print(Style.RESET_ALL)

                    elif inInput == "DOWNLOAD":  # if command is to download something from another peer
                        # enter the peers ip
                        clientIP = input("Enter the desired clients IP:  ")
                        # enter the peers tcp port
                        clientPort = input(
                            "Enter the desired clients TCP Port:  ")
                        # enter the file you want from the peer
                        fileName = input(
                            "Enter the file you wish to download:  ")

                        ADR = (clientIP, int(clientPort))  # Address Binding
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
                                print(" 📁 File Received : ", filepath)
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

        send_data = f"{command}@{filename}@{text}"
        conn.sendto(send_data.encode(FORMAT), addr)

    elif p not in files:
        send_data = "DOWNLOAD-ERROR@"+str(data[1]) + "@File does not exist"
        conn.sendto(send_data.encode(FORMAT), addr)

    sys.exit()  # Closing Thread for TCP connection test


def waitClient(TCPPort, IP):
    ADRC = (IP, TCPPort)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADRC)  # Bind the Ip and the Port
    server.listen()  # Waiting for a TCP connection

    while 1:
        conn, addr = server.accept()  # Accepting a client
        thread = threading.Thread(target=handle_client, args=(
            conn, addr))  # Making a thread to handle client TCP
        thread.start()  # Starting the thread and connecting the client


if __name__ == "__main__":
    print("\n Welcome Client ! \n")
    name = input("Enter your name :  ")  # User Inputs Name
    IP = input("Enter servers IP :  ")  # User Inputs IP
    TCPIP = socket.gethostbyname(socket.gethostname())
    TCPPort = int(input("Enter your TCP Port : "))  # User Inputs TCP Port
    FORMAT = "utf-8"
    thread = threading.Thread(target=waitClient, args=(
        TCPPort, TCPIP))  # Making a client a thread
    thread.start()
    main(TCPPort, IP, name, FORMAT)
