import socket, select, sys;

BUFFERSIZE = 5         # used to receive length of each message and scale recv buffer size based on message length

PORT = 5001            # arbitrary non-privileged port
HOST = ''              # retreives host of machine this code is run on

acceptedCommands = ["register", "login", "logout", "sendmsg", "listusers"]

onlineList = []        # list of online users (defined as users who have logged in)
inputs = []            # list of sockets
connectedSockets = {}  # dict to save socket info (key=cliSocket, value=IP)
usernamePassword = {}  # dict for password validation (key=username, value=password)
addressUsername = {}   # dict for sending messages (key=address, value=username)

"""
linked chain of connected keys represented by the three dictionaries above: 
socket -> address -> username -> password 
"""

def getRegisteredUsers():
	# if the file exists open it and read the names. If not return an empty list
	users = {}
	try:
		f = open("users.txt", "r")
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
	#write the user to our file/database, if the file doesn't exist create it 
	f = open("users.txt", "a+")
	f.write('\n')
	f.write(username)
	f.write('\n')
	f.write(password)
	f.write('\n')
	f.close()

def getData(cliSocket):
	"""
	APPROACH: recv a predetermined length (buffersize) that contains an 
	integer value representing the length of the incoming message.
	Use this integer value to variable the buffer size of the message
	so that we don't run into problems if a mesage exceeds a fixed length
	we decide in advance. 
	"""
	try:
		msgSize = cliSocket.recv(BUFFERSIZE)
		msg = cliSocket.recv(int(msgSize)+10)
		if not len(msg):
			#if the client forces disconnection
			return False
		return msg
	except:
		return False

def getAddress(sendingUsername):
	#iterate over logged in users (addressUsername) and return matching address
	for address, username in addressUsername.items():
		if (username == sendingUsername):
			return address

def getSocket(sendingAddress):
	#iterate over connectedSockets and return the socket associated with "sendingAddress"
	for socket, address in connectedSockets.items():
		if (address == sendingAddress):
			return socket

def checkArguments(commandName, messageArray, client):
	"""
	This function is used to pass errors back to the client if he/she
	incorrectly issued a command. Becasue we strip away whitespace before
	error checking, whitespace isn't taken into account. For a full list of 
	possible errors see the attached documentation. 
	"""
	if (commandName == "register"):
		# check length
		if (len(messageArray) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		# check unique username
		elif (messageArray[1].decode('utf-8') in usernamePassword.keys()):
			client.send(bytes("ERROR 202: Username taken", "utf-8"))
			return False
		 
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
		
		return True

	elif (commandName == "logout"):
		if (len(messageArray) != 1):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		elif (connectedSockets[client] not in addressUsername):
			client.send(bytes("ERROR 206: must be logged in to issue command", "utf-8"))
			return False
	
		return True
	elif (commandName == "sendmsg"):
		#check length
		if (len(messageArray) < 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False

		givenUsername = messageArray[1].decode('utf-8')
		clientAddress = connectedSockets[client]
		if (clientAddress not in addressUsername):
			client.send(bytes("ERROR 206: must be logged in to issue command", "utf-8"))
			return False
		if (givenUsername not in usernamePassword):
			client.send(bytes("ERROR 203: Unregistered username","utf-8"))
			return False
		if (givenUsername not in onlineList):
			client.send(bytes("ERROR 211: user isn't online", "utf-8"))
			return False

		clientUsername = addressUsername[clientAddress]
		# check for self sent messages, we don't allow those.
		if (givenUsername == clientUsername):
			client.send(bytes("ERROR 212: self sent message", "utf-8"))
			return False

		return True
	elif (commandName == "listusers"):
		#check length 
		if (len(messageArray) != 1):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False

		address = connectedSockets[client]
		if (address not in addressUsername):
			client.send(bytes("ERROR 206: must be online to issue command", "utf-8"))
			return False
		
		return True

def processCommand(messageArray, client):
	"""
	This function handles the actual logic behind each command. It uses checkArguments
	defined above as a helper method to accomplish this.

	note: extra whitespace is ignored in the format of these messages.
	"""
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
			properArgStructure = checkArguments("register", messageArray, client)
			if (properArgStructure):
				username = messageArray[1].decode('utf-8')
				password = messageArray[2].decode('utf-8')
				# save the user to our database (file) and add to the in app datastructure
				addUserToFile(username, password)
				usernamePassword[username] = password
				#notify client/server
				print("registered new user: " + str(username))
				client.send(bytes("registered successfully", "utf-8"))

		elif (command == "login"):
			"""
			when a user logs in we save their username with the address they login from.
			Thus, user's aren't tightly coupled with their address and can login from any machine.
			We also need to check they are logging in with the correct password

			expected format: "login <username> <password>"
			"""
			properArgStructure = checkArguments("login", messageArray, client)
			if (properArgStructure):
				# associate user address with their username.
				username = messageArray[1].decode('utf-8')
				addressUsername[userAddress] = username
				# add them to the list of online users
				onlineList.append(username)
				#notify client/server
				print("successfully logged in user: " + str(username))
				client.send(bytes("login successful", "utf-8"))

		elif (command == "logout"):
			properArgStructure = checkArguments("logout", messageArray, client)
			if (properArgStructure):
				callerAddress = connectedSockets[client]
				callerUsername = addressUsername[callerAddress]
				#cleanup user
				onlineList.remove(callerUsername)
				del addressUsername[callerAddress]
				#notify client/server
				print("successfully logged out user: " + str(callerUsername))
				client.send(bytes("successfully logged out", "utf-8"))

		elif (command == "sendmsg"):
			properArgStructure = checkArguments("sendmsg", messageArray, client)
			if (properArgStructure):
				"""
				Steps:
				1) get sender's username  2) get sending address 3) build output 
				4) send message using the client socket associated with the sending address
				
				output = "<sent from> <msg>"
				"""
				#get sender's username
				senderAddress = connectedSockets[client]
				senderUsername = addressUsername[senderAddress]

				#get sending address
				sendingUsername = messageArray[1].decode('utf-8')
				sendingAddress = getAddress(sendingUsername)

				#build output
				i = 2
				output = str(senderUsername) + " > "
				while (i < len(messageArray)):
					output += messageArray[i].decode('utf-8') + " "
					i+=1

				#notify server
				print("sent a message to: " + str(sendingUsername) + " from: " + str(senderUsername))

				#get sending socket and send message
				sendingSocket = getSocket(sendingAddress)
				sendingSocket.send(bytes(output, "utf-8"))


		elif (command == "listusers"):
			properArgStructure = checkArguments("listusers", messageArray, client)
			if (properArgStructure):
				#build list
				i = 0
				userList = ""
				while (i < len(onlineList)):
					userList += onlineList[i]
					userList += "\n"
					i+=1
				#notify server
				print("Issued 'listusers' command")
				#respond to client
				client.send(bytes(userList, "utf-8"))

def main():
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

				# save account info
				connectedSockets[clientConnection] = clientAddress

				# append to running list of sockets
				clientConnection.setblocking(0)
				inputs.append(clientConnection) 
			else: 
				# this branch handles existing socket data (sent from clients)
				data = getData(s)

				# check for forced closed connections and handle/cleanup appropriately
				if data is False:
					print("Closed connection: " + str(connectedSockets[s]))
					inputs.remove(s)
					address = connectedSockets[s]
					if (address in addressUsername):
						#if they are logged in when they force closed connection
						onlineList.remove(addressUsername[connectedSockets[s]])
						del addressUsername[connectedSockets[s]]
					del connectedSockets[s]
					continue

				#process the request given by the client
				messageArray = data.split() #split data to avoid whitespace complications
				processCommand(messageArray, s)

		for s in exceptional: 
			connectedSockets.remove(s)
			del connectedSockets[s]

if __name__ == '__main__':
	#retrieve the stored registered users
	usernamePassword = getRegisteredUsers()
	#start application
	main()


