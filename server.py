import socket
from _thread import *
import sys

if len(sys.argv) > 1:
    server = sys.argv[1]
    port = int(sys.argv[2])
else:
    server = 'localhost'
    port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = socket.gethostbyname(server)
print("SERVER IP", server_ip)

try:
    s.bind((server_ip, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
# Protocol
# "ID:IN_GAME,ALREADY_PLAYED,MY_TURN,MY_HAND,ROUND_OVER,MY_CARDS"
mes = ["0:0,0,0,0,0,x", "1:0,0,0,0,0,x"]


def threaded_client(conn):
    global currentId, mes
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                mes[id] = reply                 

                if id == 0:
                    nid = 1      
                        
                if id == 1: 
                    nid = 0
               
				
                reply = mes[nid][:]                
                print("Sending: " + reply)
            
            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")    
    mes = ["0:0,0,0,0,0,x", "1:0,0,0,0,0,x"]
    conn.close()
    exit()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
