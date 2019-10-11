# Echo server program
# socket.sendto(string, address) for direct messages

import socket, select, sys;

 
PORT = 5000        # arbitrary non-privileged port
HOST = 'localhost' # retreives host of machine this code is run on

users = {}         # dictionary defined key = username, value = clientsocket
onlineList = []    # list of online users

# create tcp/ip socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# bind our socket and listen for connections
server.bind((HOST, PORT))
server.listen(5) #queue of up to 5 connections

#list of sockets I expect to read from
inputs = [ server ] 

#list of sockets I expect to write to
outputs = [ ]


while inputs:
	readable, writable, exceptional = select.select(inputs, inputs, inputs)
	connection, addr = s.accept()
	print ("Connected by " + str(addr))
	connection.send(bytes("Welcome to the server", "utf-8"))
 # while 1:    
 # 	data = connection.recv(1024)    
 # 	if not data: break    
 # 	connection.sendall(data)

conn.close()