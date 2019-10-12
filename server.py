# Echo server program
# socket.sendto(string, address) for direct messages

import socket, select, sys;

HEADER_SIZE = 10   # used for variable message size 
PORT = 5000        # arbitrary non-privileged port
HOST = "127.0.0.1" # retreives host of machine this code is run on

user_name = []     # list of registered user_names retreived from the stored file
onlineList = []    # list of online users (defined as users who have logged in)
inputs = []        # list of sockets
connections = 0    # running number of active connections

# create tcp/ip socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# bind our socket and listen for connections
server.bind((HOST, PORT))
server.listen(5) #queue of up to 5 connections

#list of sockets I expect to read from
inputs.append(server)

while inputs:
	readable, writable, exceptional = select.select(inputs, inputs, inputs)

	for socket in readable:
		if socket is server:
			# this branch handles connection requests from new clients
			print("received a connection request from a client.")
			clientConnection, clientAddress = server.accept()
			print ("successful connection to: " + str(clientAddress))

			# account for active connection
			connection += 1

			# append to running list of sockets
			clientConnection.setblocking(0)
			inputs.append(clientConnection) 
		else: 
			# this branch handles existing sockets sending data (data from clients)
			data = socket.recv(1024)
			print("existing socket sending data. Sent from: " + str(socket))
			print("existing socket sent data, the data was: " + str(data))
			socket.send(bytes("recieved data", 'utf-8'))