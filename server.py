import socket, select, sys;

PORT = 5000            # arbitrary non-privileged port
HOST = "127.0.0.1"     # retreives host of machine this code is run on

onlineList = []        # list of online users (defined as users who have logged in)
inputs = []            # list of sockets
connectedSockets = {}  # dict to save socket info (key=cliSocket, value=IP)
usernamePassword = {}  # dict for password validation (key=username, value=password)
usernameAddress = {}   # dict for sending messages (key=username, value=address)

acceptedCommands = ["register", "login", "logout", "sendmsg", "listusers"]


def getRegisteredUsers():
	# if the file exists open it and read the names if not return empty list
	users = {}

	try:
		f = open("regUsernames.txt", "r")
		names = f.read()
		names = names.split()
		# loop over names and add them to the list
		i = 0
		while (i+1 < len(names)):
			users[names[i]] = names[i+1]
			i+=2
		return users
	except:
		return users

def getData(cliSocket):
	try:
		message = cliSocket.recv(1024)

		if not len(message):
			return False

		return message
	except:
		return False

def checkArguments(commandName, messageArray, client):

	if (commandName == "register"):
		if (len(messageArray) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
		elif (messageArray[0].decode('utf-8') not in usernamePassword):
			pass
	elif (commandName == "login"):
		pass
	elif (commandName == "logout"):
		pass
	elif (commandName == "sendmsg"):
		pass
	elif (commandName == "listusers"):
		pass

def processCommand(messageArray, client):

	command = messageArray[0].decode('utf-8')
	userAddress = connectedSockets[client]

	if (command not in acceptedCommands):
		#send array message saying you didn't send an accepted command
		client.send(bytes("ERROR 200: Received unaccepted command.","utf-8"))
	else: 
		if (command == "register"):
			# expected format: "register <username> <password>"
			checkArguments("register", messageArray, client)

		elif (command == "login"):
			"""
			when a user logs in we save their username with the address they login from.
			Thus, user's aren't tightly coupled with their address and can login from any machine.
			"""
			checkArguments("login", messageArray, client)

			# associate user address with their username.
			username = messageArray[1].decode('utf-8')
			usernameAddress[username] = userAddress

		elif (command == "logout"):
			checkArguments("logout", messageArray, client)

		elif (command == "sendmsg"):
			checkArguments("sendmsg", messageArray, client)

		elif (command == "listusers"):
			checkArguments("listusers", messageArray, client)

def main():
	# running number of active connections
	connections = 0    

	# create tcp/ip socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)

	# bind our socket and listen for connections
	server.bind((HOST, PORT))
	server.listen(5) #queue of up to 5 connections

	# list of sockets I expect to read from
	inputs.append(server)

	# get registered users (name, password) from saved file
	usernamePassword = getRegisteredUsers()

	#manage input (clients) while server is running
	while inputs:
		readable, writable, exceptional = select.select(inputs, inputs, inputs)

		for s in readable:
			if s is server:
				# this branch handles connection requests from new clients
				print("received a connection request from a client.")
				clientConnection, clientAddress = server.accept()
				print ("successful connection to: " + str(clientAddress))
				print ("client socket is: " + str(clientConnection))

				# account for active connection
				connections += 1

				# save account info
				connectedSockets[clientConnection] = clientAddress

				# append to running list of sockets
				clientConnection.setblocking(0)
				inputs.append(clientConnection) 
			else: 
				# this branch handles existing sockets sending data (sent from clients)
				data = getData(s)

				if data is False:
					print("Closed connection from: " + str(connectedSockets[s]))
					inputs.remove(s)
					del connectedSockets[s]
					continue

				#process the request given by the client
				messageArray = data.split()
				processCommand(messageArray, s)

if __name__ == '__main__':
	main()
