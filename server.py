import socket, select, sys;

PORT = 5000            # arbitrary non-privileged port
HOST = "127.0.0.1"     # retreives host of machine this code is run on

acceptedCommands = ["register", "login", "logout", "sendmsg", "listusers"]

onlineList = []        # list of online users (defined as users who have logged in)
inputs = []            # list of sockets
connectedSockets = {}  # dict to save socket info (key=cliSocket, value=IP)
usernamePassword = {}  # dict for password validation (key=username, value=password)
addressUsername = {}   # dict for sending messages (key=address, value=username)

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
		f.close()
		return users
	except:
		return users

def addUserToFile(username, password):
	#write the user to our file, if the file doesn't exist create it 
	f = open("regUsernames.txt", "a+")
	f.write('\n')
	f.write(username)
	f.write('\n')
	f.write(password)
	f.write('\n')
	f.close()

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
		# check length
		if (len(messageArray) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		# check unique username
		elif (messageArray[1].decode('utf-8') in usernamePassword.keys()):
			client.send(bytes("ERROR 202: Username taken", "utf-8"))
			return False
		else: 
			return True

	elif (commandName == "login"):
		# if the client issuing the 'login' command is already logged in return error 
		if (connectedSockets[client] in addressUsername):
			client.send(bytes("ERROR 208: logout before logging in again", "utf-8"))
			return False
		# check length
		if (len(messageArray) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		# check password and username errors
		givenUsername = messageArray[1].decode('utf-8')
		givenPassword = messageArray[2].decode('utf-8')
		if (givenUsername not in usernamePassword.keys()):
			client.send(bytes("ERROR 203: Unregistered username","utf-8"))
			return False
		elif(usernamePassword[givenUsername] != givenPassword):
			client.send(bytes("ERROR 204: Incorrect password","utf-8"))
			return False
		elif(givenUsername in onlineList):
			client.send(bytes("ERROR 207: user already signed in","utf-8"))
			return False
		else:
			return True

	elif (commandName == "logout"):
		pass
	elif (commandName == "sendmsg"):
		pass
	elif (commandName == "listusers"):
		#check length 
		if (len(messageArray) != 1):
			client.send(bytes("ERROR 205: Incorrect number of arguments", "utf-8"))
			return False

		address = connectedSockets[client]
		if (address not in addressUsername):
			client.send(bytes("ERROR 206: must be online to issue command", "utf-8"))
			return False
		else: 
			return True

def processCommand(messageArray, client):
	# command to be processed
	command = messageArray[0].decode('utf-8')

	# get the userAddress so I know who sent the command
	userAddress = connectedSockets[client]

	if (command not in acceptedCommands):
		#send array message saying you didn't send an accepted command
		client.send(bytes("ERROR 200: Received unaccepted command.","utf-8"))
	else: 
		if (command == "register"):
			"""
			here we check format of arguments for followed protocal.
			extract the username and password and save it to our structures (file, in app)

			expected format: "register <username> <password>"
			"""
			properStructure = checkArguments("register", messageArray, client)
			if (properStructure):
				username = messageArray[1].decode('utf-8')
				password = messageArray[2].decode('utf-8')
				# save the user to our database (file) and add to the in app datastructure
				addUserToFile(username, password)
				usernamePassword[username] = password
				client.send(bytes("registered successfully", "utf-8"))

		elif (command == "login"):
			"""
			when a user logs in we save their username with the address they login from.
			Thus, user's aren't tightly coupled with their address and can login from any machine.
			We also need to check they are logging in with the correct password

			expected format: "login <username> <password>"
			"""
			properStructure = checkArguments("login", messageArray, client)

			if (properStructure):
				# associate user address with their username.
				username = messageArray[1].decode('utf-8')
				addressUsername[userAddress] = username
				# add them to the list of online users
				onlineList.append(username)
				client.send(bytes("login successful", "utf-8"))

		elif (command == "logout"):
			checkArguments("logout", messageArray, client)

		elif (command == "sendmsg"):
			checkArguments("sendmsg", messageArray, client)

		elif (command == "listusers"):
			properStructure = checkArguments("listusers", messageArray, client)
			if (properStructure):
				i = 0
				outputString = ""
				while (i < len(onlineList)):
					outputString += onlineList[i]
					outputString += "\n"
					i+=1
				client.send(bytes(outputString, "utf-8"))

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

	#manage input (clients) while server is running
	while inputs:
		readable, writable, exceptional = select.select(inputs, inputs, inputs)

		for s in readable:
			if s is server:
				# this branch handles connection requests from new clients
				print("received a connection request from a client.")
				clientConnection, clientAddress = server.accept()
				print ("successful connection to: " + str(clientAddress))

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

				# check for forced closed connections and handle/cleanup appropriately
				if data is False:
					print("Closed connection from: " + str(connectedSockets[s]))
					inputs.remove(s)
					username = addressUsername[connectedSockets[s]]
					if (username in onlineList):
						onlineList.remove(addressUsername[connectedSockets[s]])
						del addressUsername[connectedSockets[s]]
					del connectedSockets[s]
					continue

				#process the request given by the client
				messageArray = data.split()
				processCommand(messageArray, s)

if __name__ == '__main__':
	usernamePassword = getRegisteredUsers()
	main()