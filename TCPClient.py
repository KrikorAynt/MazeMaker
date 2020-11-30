import socket 
import threading
import time
import MazeMaker

HEADER = 64
PORT = 5050             #server port
FORMAT = 'utf-8'        #encoding method
DC_MSSG = "!DC"         #disconnect message
HOST =  socket.gethostbyname(socket.gethostname()) #this needs to be changed to the address of the device that TCPSend is being run on
ADDR = (HOST, PORT)     #address

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #makes a socket called client
client.connect(ADDR)                                        #connects it to server

solution = MazeMaker.solution                               #gets the solution of the maze

#sends a message containing the string msg to the server and recieves a confirmation back
def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' '*(HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	print(client.recv(2048).decode(FORMAT))

#these stop, turn and activate the "robot"
def stop():
    send("[0,0,0,0]")
    time.sleep(1)
def turnR():
    stop()
    send("[0,255,255,0]")
    time.sleep(1)
    go()
def turnL():
    stop()
    send("[255,0,0,255]")
    time.sleep(1)
    go()
def go():
    send("[0,255,0,255]")
    time.sleep(1)

counter=1
Dir="Down"

#determines what action to do based on the current box and the next box in the solution
for i in solution:
    
    Out=str(i).strip("()")
    coords = Out.split(", ")
    x= int(coords[0])
    y= int(coords[1])
    if(counter<len(solution)):
        Out=str(solution[counter]).strip("()")
        coordsNxt = Out.split(", ")
        nx= int(coordsNxt[0])
        ny= int(coordsNxt[1])
        if(Dir=="Down"):
            if(x==nx and y<ny):
                go()
            elif(x<nx and y==ny):
                turnL()
                Dir="Right"
            elif(x>nx and y==ny):
                turnR()
                Dir="Left"
        if(Dir=="Up"):
            if(x==nx and y>ny):
                go()
            elif(x<nx and y==ny):
                turnR()
                Dir="Right"
            elif(x>nx and y==ny):
                turnL()
                Dir="Left"
        if(Dir=="Right"):
            if(x==nx and y<ny):
                turnR()
                Dir="Down"
            elif(x<nx and y==ny):
                go()
            elif(x==nx and y>ny):
                turnL()
                Dir="Up"
        if(Dir=="Left"):
            if(x==nx and y>ny):
                turnR()
                Dir="Up"
            elif(x>nx and y==ny):
                go()
            elif(x==nx and y<ny):
                turnL()
                Dir="Down"
                
    else:
        stop()    
        send("DONE")
    counter+=1
#disconnects the client from the server
send(DC_MSSG)