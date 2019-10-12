# Echo server program
# socket.sendto(string, address) for direct messages

import socket, select, sys;

HEADER_SIZE = 10   # used for variable message size 
PORT = 5000        # arbitrary non-privileged port
HOST = "127.0.0.1" # retreives host of machine this code is run on

users = {}         # dictionary (key = username, value = clientsocket)
onlineList = []    # list of online users

# create tcp/ip socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# bind our socket and listen for connections
server.bind((HOST, PORT))
server.listen(5) #queue of up to 5 connections

#list of sockets I expect to read from
inputs = [server] 

def retrieveData(cliConnection):
	try:
		header = cliConnection.recv(HEADER_SIZE)
		if not len(header):
			return False

		msgSize = int(header.decode('utf-8'))
		data = cliConnection.recv(msgSize)

		return {
		'header': header,
		'data': data
		}
	except:
		# the branch handles forced closed connections by the client
		# for example losing a connection or socket.close()
		return False


while inputs:
	readable, writable, exceptional = select.select(inputs, inputs, inputs)

	for socket in readable:
		if socket is server:
			# this branch handles connection requests
			print("received a connection request from a client")
			clientConnection, clientAddress = server.accept()
			print ("successfully connection to" + str(clientConnection))

			# retrieve client data
			cliData = retrieveData(clientConnection)

			# save users info
			clients[clientConnection] = cliData

			# append to running list of sockets
			inputs.append(clientConnection) 
			clientConnection.setBlocking(0)

		else: 
			# this branch handles existing sockets sending data
			msg = retrieveData(socket)
			print("existing socket sending data. Sent from: " + str(socket))

			cliData = clients[socket]

			print("message was: " + cliData['header'] + cliData['data'] + msg['header'] + msg['data'])

conn.close()