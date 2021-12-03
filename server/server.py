import os
import socket
import threading
import string

from colorama import Fore, Back, Style

from pyfiglet import Figlet


IP = socket.gethostbyname('127.0.0.1')  # Setting the IP adress of the socket
PORT = 6666  # Setting the UDP Port number (might change)
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

clients = []  # List that stores clients information

SERVER_DATA_PATH = "./"
CLIENT_NAME = ""
name = ""


def checkReq(name, req):  # checks if client name and req# match
    # getting the database file of the clientname.txt
    fileP = "./db/"+str(name)+".txt"
    f = open(fileP, "r")  # open the file of clientname.txt
    first_line = f.readline()  # reading the file
    first_line = first_line.split("\t")  # splitting the line by tabs

    # the first index in the file is the name of the user
    fname = first_line[0]
    freq = first_line[4]  # the fifth index is the users RQ#

    if(fname == name and freq == str(req)):  # checking if the clients name and RQ# are the same
        return True
    return False


def checkClient(name):  # Checks if client already exists
    fileName = name+".txt"  # name + .txt is the name of the file
    files = os.listdir("./db")  # List of files in directory
    if fileName in files:  # if the name.txt is in the the files list already
        return True
    else:
        return False


def checkTCP(tcp):  # checks the clients tcp port
    files = os.listdir("./db")  # files in database directory
    l = len(files)  # number of files
    for client in files:  # for all the clients in the files database
        filePath = "./db/"+str(client)
        f = open(filePath, "r")
        line = f.read()
        if str(tcp) in line:
            return True
    return False


def handle_client(data, addr):  # Handles client Thread (request and response)
    # connecting to the socket port
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientCount = 0

    # Data received from the client as a reponse
    # data = conn.recv(SIZE).decode(FORMAT)
    data = data.split("@")
    # The first thing the client inputs is a command which is stored in cmd
    cmd = data[0]

    if cmd == "HELP":  # if the command is help
        send_data = "OK@"  # OK Command to client
        send_data += "LIST: List all the files from the server. \n"
        send_data += "FIND <filepath> : Finds specified file \n"
        send_data += "DELETE <filepath>: Delete a file from the server \n"
        send_data += "DISC : Disconnect from the server \n"
        send_data += "HELP : List all the commands. \n"
        conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "RETRIEVE-INFOT":  # if the command is retrieve-infot to get the info of a specific peer
        # stores the files in the database in files list
        files = os.listdir("./db")
        l = len(files)
        fileN = str(data[1])+".txt"  # data[1] is the name of the client.txt
        name = "./db/"+str(data[1])+".txt"
        if fileN in files:  # if the client exists
            send_data = "OK@RETRIEVE-INFOT" + \
                str(addr[1]) + " \n [ "  # send the peers RQ#
            f = open(name, "r")
            for x in f:
                send_data += (str(x.strip('\n')))  # Send the peers ip and
            send_data += " ]"
            conn.sendto(send_data.encode(FORMAT), addr)
        else:  # the peer doesnt exist
            send_data = "OK@RETRIEVE-ERROR " + \
                str(addr[1])+" Client does not exist"
            conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "RETRIEVE-ALL":  # this commands gets all the info about the registered peers
        files = os.listdir("./db")
        l = len(files)

        send_data = "OK@RETRIEVE " + \
            str(addr[1]) + \
            " \n-  NAME \t   IP \t\t UDP \t TCP \t REQ \t Published Files   -"  # format to send to peers

        for client in files:  # sending all the info of every peer
            filePath = "./db/"+str(client)
            f = open(filePath, "r")
            send_data += " \n [ "
            for x in f:
                send_data += (str(x.strip('\n')))
            send_data += " ]"

        conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "PUBLISHREJ":
        name = data[1]
        if checkClient(name):
            send_data = "GOOD@"
            send_data += str(addr[1])
            conn.sendto(send_data.encode(FORMAT), addr)

        else:
            send_data = "NOTOK@"
            send_data += str(addr[1])
            conn.sendto(send_data.encode(FORMAT), addr)
            print(" PUBLISH-DENIED #", addr[1])

    elif cmd == "REMOVEREJ":
        name = data[1]

        if checkClient(name) and checkReq(name, addr[1]):
            send_data = "GOOD@"
            send_data += str(addr[1])
            conn.sendto(send_data.encode(FORMAT), addr)

        else:
            send_data = "NOTOK@"
            send_data += str(addr[1])
            conn.sendto(send_data.encode(FORMAT), addr)
            print(" REMOVE-DENIED #", addr[1])

    elif cmd == "PUBLISH":  # If the client wants to send a file to the server

        # assigning the name of the file and the file name
        name, fname = data[1], data[2]
        fileExtension = fname[-3:]

        if (fileExtension == "txt"):  # if the client wants to publish a txt file
            filepath = fname
            fileP = "./db/"+str(name)+".txt"
            f = open(fileP, "a")
            f.write(filepath + "\t")  # write and publish the file
            f.close()
            send_data = "OK@PUBLISHED #"+str(addr[1])

            conn.sendto(send_data.encode(FORMAT), addr)
            conn.settimeout(4)

        else:  # if the user didnt publish a txt file
            print(" [ ERROR ]\tOnly txt files are permitted. ")
            send_data = "NOTOK@ PUBLISH-DENIED #" + \
                str(addr[1]) + " File type is not supported. "
            conn.sendto(send_data.encode(FORMAT), addr)
            conn.settimeout(4)

    elif cmd == "REMOVE":  # If the client wants to delete a file from the server
        # access the files in the directory
        files = os.listdir(SERVER_DATA_PATH)
        name = str(data[1])
        filename = str(data[2])
        if len(files) == 0:  # if there are no files in the folder
            send_data = "NOTOK@"
            send_data += "The server directory is empty"
            # print("145")
            conn.sendto(send_data.encode(FORMAT), addr)
        else:  # if the file exists
            # getting the file in the directory
            fileP = "./db/"+str(name)+".txt"
            # print(fileP)
            f = open(fileP, "r")
            lines = f.readlines()

            if(len(lines) > 1):
                # print(lines)
                line1 = lines[0]
                line2 = lines[1]
                if(filename in line2):
                    line2 = line2.replace(filename, "")
                    f.close()
                    f2 = open(fileP, "w")
                    #print("line 2 : ", line2)
                    f2.write(line1)
                    f2.write(line2.lstrip())  # removing the lines of the file
                    f2.close()
                    send_data = "OK@"
                    send_data += "REMOVED #" + str(addr[1])
                    conn.sendto(send_data.encode(FORMAT), addr)

                else:
                    send_data = "NOTOK@"
                    send_data += str(addr[1])
                    conn.sendto(send_data.encode(FORMAT), addr)

            else:
                send_data = "NOTOK@"
                send_data += str(addr[1])
                conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "UPDATE-CONTACT":  # if the command is for the user to uopdate their contact
        # assigning user's info
        name, new_ip, new_udp, new_tcp = data[1], data[2], data[3], data[4]
        if(len(name) < 5):
            line1 = str(name)+"\t\t"+str(new_ip)+"\t" + \
                str(new_udp)+"\t"+str(new_tcp)+"\t"+str(addr[1])+"\n"
        else:
            line1 = str(name)+"\t"+str(new_ip)+"\t"+str(new_udp) + \
                "\t"+str(new_tcp)+"\t"+str(addr[1])+"\n"

        fileExtension = "./db/"+str(name)+".txt"
        if checkClient(name):  # Checks if client exists
            f = open(fileExtension, "r")
            lines = f.readlines()
            if(len(lines) > 1):
                line2 = lines[1]
                f.close()
                send_data = "OK@PUBLISHED #"+str(addr[1])
                f2 = open(fileExtension, "w")
                f2.write(line1)
                f2.write(line2)
                f2.close()
                send_data = "OK@" + \
                    str(addr[1])+"\t"+str(name)+"\t"+str(new_ip) + \
                    "\t"+str(new_udp)+"\t"+str(new_tcp)
                conn.sendto(send_data.encode(FORMAT), addr)

            elif(len(lines) < 2):
                f.close()
                send_data = "OK@PUBLISHED #"+str(addr[1])
                f2 = open(fileExtension, "w")
                f2.write(line1)
                f2.close()
                send_data = "OK@" + \
                    str(addr[1])+"\t"+str(name)+"\t"+str(new_ip) + \
                    "\t"+str(new_udp)+"\t"+str(new_tcp)
                conn.sendto(send_data.encode(FORMAT), addr)

        else:
            send_data = "NOT-OK@" + \
                str(addr[1])+"\t"+str(name)+"\t"+"Client name does not exist"
            conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "SEARCH-FILE":  # if the client wants to search for a file
        files = os.listdir("./db")
        l = len(files)
        fname = data[1]  # the file name is the index 1 of data

        send_data = "OK@RETRIEVE #" + \
            str(addr[1]) + \
            " \n-  NAME \t   IP \t\t TCP -"

        fileExists = False
        for client in files:
            filePath = "./db/"+str(client)
            f = open(filePath, "r")
            lines = f.readlines()
            firstLine = lines[0].split("\t")
            cName = firstLine[0]
            if(len(lines) > 1):  # If client has published any files
                if(fname in lines[1]):  # If file name is in first line
                    if(len(cName) < 5):  # Formating fix with tabs for clients with short names
                        fileExists = True  # File exists true
                        send_data += " \n [ "+firstLine[0] + \
                            "\t\t"+firstLine[2]+"\t"+firstLine[4]+" ]"
                    else:
                        fileExists = True  # File exists true
                        send_data += " \n [ "+firstLine[0] + \
                            "\t"+firstLine[1]+"\t"+firstLine[3]+" ]"

        if(fileExists):  # If file exists
            conn.sendto(send_data.encode(FORMAT), addr)

        elif(not fileExists):  # If no client has the file
            send_data = "NOTOK@FILE DOES NOT EXIST"
            conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "REGISTER":  # If the client command is REGISTER, frist thing the client does

        if (not(checkClient(str(data[1]))) and not(checkTCP(data[4]))):
            send_data = "OK@"
            # Send to the client that they registred with this unique rq number
            send_data += "REGISTERED # " + str(addr[1])
            # Encode the data and send it
            conn.sendto(send_data.encode(FORMAT), addr)
            conn.settimeout(4)

            name = data[1]  # Store the clients name in name
            CLIENT_NAME = name
            IP = str(addr[0])  # Store the clients ip address
            UDP = data[3]  # Store the clients udp port
            TCP = data[4]  # Store the clients tcp port
            REQ = str(addr[1])

            # creating a file in the directory with the clients name
            fileName = "./db/" + name + ".txt"
            f = open(fileName, "x")
            f.write(name)  # storing all of the clients info
            if(len(name) < 5):
                f.write("\t")
            f.write("\t"+IP+"\t")
            f.write(UDP+"\t")
            f.write(TCP+"\t")
            f.write(REQ+"\t\n")
            f.close()

            # Print hat there is a new connection with the ip and rq#
            print(f" 🚨 [ NEW CONNECTION ] {addr[1]} connected. ")
            clientString = str(data[1])
            clients.append(clientString)  # Adds client name to list

        else:  # If the clients name is already in the list of clients, deny him
            send_data = "RD@"  # Send to the client that they are denied and the reson why
            send_data += "REGISTER-DENIED  # " + \
                str(addr[1]) + " Clients name or TCP Port is already in use. "
            conn.sendto(send_data.encode(FORMAT), addr)

    elif cmd == "DE-REGISTER":  # If client wants to deregister
        clientCount -= 1  # Decrement the client count
        name = data[1]
        # If the name exists in clients list
        if checkClient(name) and checkReq(name, addr[1]):
            send_data = "OK@"
            send_data += "De-Registered successfully"  # What to send back to the user
            name = data[1]
            filename = name+".txt"
            print(f" 🔌 [ DE-REGISTERED ] {addr[1]} disconnected. ")
            os.remove("./db/"+filename)
            conn.sendto(send_data.encode(FORMAT), addr)

        else:  # if the client that wants to deregister enters the wrong name
            print(" [DENIED] DE-REGISTER was denied. ")
            send_data = "NOTOK@"
            send_data += " DE-REGISTER DENIED "  # What to send back to the user
            conn.sendto(send_data.encode(FORMAT), addr)
            # send_data = "NO@"
            # conn.sendto(send_data.encode(FORMAT), addr)


def main():
    # Welcome message for the server
    f = Figlet(font='slant')
    print(Fore.CYAN + f.renderText('WELCOME \nDr.FERHAT'))
    print("[STARTING] Server is starting. \n")
    # UDP_IP = "127.0.0.1"  # Locahokhost for now
    UDP_IP = socket.gethostbyname(socket.gethostname())
    UDP_PORT = 6666

    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP connection
    conn.bind((UDP_IP, UDP_PORT))  # binding the ip and port

    while True:
        # can only receive 1024 bytes at a time
        data, addr = conn.recvfrom(1024)
        data = data.decode(FORMAT)
        thread = threading.Thread(target=handle_client, args=(
            data, addr))  # Making a client a thread for UDP
        thread.start()


if __name__ == "__main__":
    main()
