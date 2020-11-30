import socket
import threading
import time

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 5050        # The port used by the server
ADDR = (HOST,PORT)      #address
FORMAT = 'utf-8'        #encoding method
DC_MSSG = "!DC"         #disconnect message

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #makes a socket called server
server.bind(ADDR)                                           #binds the ADDR

#process done for each thread(client)
def handle_client(conn,addr):
    time.sleep(0.5)
    print("NEW CONNECT by ", addr)
    connected = True
    #constantly checks for new messages sent from the client and displays them with a time
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DC_MSSG:
                connected = False

            print("Recieved [",time.clock(),"]: ", msg)
            conn.send("Recieved Instruction".encode(FORMAT))
    conn.close()

#starts the server and constantly checks for new clients and gives them a thread
def start():
    server.listen()
    print("Server is on ", HOST)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print("[# of Connections]", {threading.activeCount() - 1})

print("Server Starting Up...")
start()