import os
import socket
import threading
import string

from colorama import Fore, Back, Style


IP = socket.gethostbyname('127.0.0.1')  # Setting the IP adress of the socket
PORT = 6666  # Setting the Port number (might change)
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

clients = []  # List that stores clients information

SERVER_DATA_PATH = "./"
CLIENT_NAME = ""


def checkClient(name):  # Checks if client already exists
    fileName = name+".txt"  # name + .txt
    files = os.listdir("./db")  # List of files in directory
    if fileName in files:
        return True
    else:
        return False


def handle_client(conn, addr):  # Handles client Thread (request and response)
    clientCount = 0

    while 1:
        # Data reveived from the client as a reponse
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        # The first thing the client inputs is a command which is stored in cmd
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"  # OK Command to client
            send_data += "LIST: List all the files from the server. \n"
            send_data += "FIND <filepath> : Finds specified file \n"
            send_data += "DELETE <filepath>: Delete a file from the server \n"
            send_data += "DISC : Disconnect from the server \n"
            send_data += "HELP : List all the commands. \n"
            conn.sendto(send_data.encode(FORMAT), ADDR)

        elif cmd == "RETRIEVE-INFOT":
            files = os.listdir("./db")
            l = len(files)
            fileN = str(data[1])+".txt"
            name = "./db/"+str(data[1])+".txt"
            if fileN in files:
                send_data = "OK@RETRIEVE-INFOT"+str(addr[1]) + " \n [ "
                f = open(name, "r")
                for x in f:
                    send_data += (str(x.strip('\n')))
                send_data += " ]"
                conn.send(send_data.encode(FORMAT))
            else:
                send_data = "OK@RETRIEVE-ERROR " + \
                    str(addr[1])+" Client does not exist"
                conn.send(send_data.encode(FORMAT))

        elif cmd == "RETRIEVE-ALL":
            files = os.listdir("./db")
            l = len(files)

            send_data = "OK@RETRIEVE "+str(addr[1]) + " \n [ "

            for client in files:
                filePath = "./db/"+str(client)
                f = open(filePath, "r")
                send_data += " \n [ "
                for x in f:
                    send_data += (str(x.strip('\n')))
                send_data += " ] , "

            send_data += " ]"
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

        elif cmd == "PUBLISH":  # If the client wants to send a file to the server
            # Setting the name of the client and the file
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:  # opening the file
                f.write(text)  # writing to a file the text
                # Print file received by server
                print(" 📁 File Received : ", filepath)
                # Tell client that it was puiblished successfully

            fileP = "./db/"+str(CLIENT_NAME)+".txt"
            f = open(fileP, "a")
            f.write(filepath[2:] + "\t")
            f.close()
            send_data = "OK@PUBLISHED #"+str(addr[1])
            conn.send(send_data.encode(FORMAT))

        elif cmd == "REMOVE":  # If the client wants to delete a file from the server
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = str(data[1])
            if len(files) == 0:  # if there are no files in the folder
                send_data += "The server directory is empty"
            else:
                if filename in files:  # if the file exists, remove it
                    os.remove("./"+filename)
                    send_data += "REMOVED #"+str(addr[1])
                    conn.send(send_data.encode(FORMAT))

        elif cmd == "REGISTER":  # If the client command is REGISTER, frist thing the client does
            clientCount += 1  # Increment client count
            # If the clients Name doesnt already exist in the list of clients, register them
            if (not(checkClient(str(data[1])))):
                send_data = "OK@"
                # Send to the client that they registred with this unique rq number
                send_data += "REGISTERED # " + str(addr[1])
                # Encode the data and send it
                conn.sendto(send_data.encode(FORMAT), ADDR)

                name = data[1]  # Store the clients name in name
                CLIENT_NAME = name
                IP = data[2]  # Store the clients ip address
                UDP = data[3]  # Store the clients udp port
                TCP = data[4]  # Store the clients tcp port

                fileName = "./db/" + name + ".txt"
                f = open(fileName, "x")
                f.write(name+"\t")
                f.write(IP+"\t")
                f.write(UDP+"\t")
                f.write(TCP+"\t\n")
                f.close()

                # Print hat there is a new connection with the ip and rq#
                print(f" 🚨 [ NEW CONNECTION ] {addr} connected. ")
                print(data[0], ' ', '#', addr[1], ' ', data[1],  # Print all the inputed user informartion
                      ' ', data[2], ' ', data[3], ' ', data[4])
                clientString = str(data[1])
                clients.append(clientString)  # Adds client name to list

            else:  # If the clients name is already in the list of clients, deny him
                send_data = "RD@"  # Send to the client that they are denied and the reson why
                send_data += "REGISTER-DENIED  # " + \
                    str(addr[1]) + " Clients name is already in use. "
                conn.sendto(send_data.encode(FORMAT), ADDR)
                # clients.remove(data[1])
                break

        elif cmd == "DE-REGISTER":  # If client wants to deregister
            clientCount -= 1  # Decrement the client count
            if name in clients:  # If the name exists in clients list
                clients.remove(name)  # Remove the name from the list
                send_data = "OK@"
                send_data += "De-Registered successfully"  # What to send back to the user
                name = data[1]
                print("[DE-REGISTERED] ", str(addr), " ", str(data[1]))
                conn.send(send_data.encode(FORMAT))
                break
            else:  # if the client that wants to deregister enters the wrong name
                print("That client is not connected. Please try again !")
                send_data = "NO@"
                conn.send(send_data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    # Welcome message for the server
    print('\033[1m', Fore.CYAN + " \n \n - 💻 - WELCOME SERVER  - 💻 - \n \n")
    print("[STARTING] Server is starting. ")
    # Connect the server to a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)  # Bind the Ip and the Port
    # server.listen()  # Listen for a client
    print("[Listening] Server is listening. \n \n")

    while 1:
        data, addr = server.recvfrom(1024)  # Accepting a client
        # thread = threading.Thread(target=handle_client, args=(conn, addr))  # Making a client a thread
        # thread.start()  # Starting the thread and connecting the client
        print("received message: %s" % data)


if __name__ == "__main__":
    main()
