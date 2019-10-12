import socket, select, sys;

PORT = 5000            # arbitrary non-privileged port
HOST = "127.0.0.1"     # retreives host of machine this code is run on

usernames = []         # list of registered usernames retreived from the stored file
onlineList = []        # list of online users (defined as users who have logged in)
inputs = []            # list of sockets
connectedSockets = {}  # dict to save user info (key=cliSocket, value=IP)

acceptedCommands = ["register", "login", "logout", "sendmsg", "listusers"]

def getRegisteredUsers():
	# if the file exists open it and read the names if not return empty list
	usernamesList = []

	try:
		f = open("regUsernames.txt", "r")
		names = f.read()
		names = names.split()
		# loop over names and add them to the list
		i = 0
		while (i < len(names)):
			usernamesList.append(names[i])
			i+=1
		return usernamesList
	except:
		return usernamesList

def getData(cliSocket):
	try:
		message = cliSocket.recv(1024)

		if not len(message):
			return False

		return message
	except:
		return False

def checkArguments(commandName, messageArray, client):

	if (commandName is "register"):
		if (len(messageArray) != 3):
			s.send(bytes("ERROR 201: Incorrect number of arguments provided", "utf-8"))
		elif (messageArray[0].decode('utf-8') in usernames):
			pass
	elif (commandName is "login"):
		pass
	elif (commandName is "logout"):
		pass
	elif (commandName is "sendmsg"):
		pass
	elif (commandName is "listusers"):
		pass

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

	# get registered users from saved file
	usernames = getRegisteredUsers()

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

				#handle forced shutdowns from the client
				if data is False:
					print("Closed connection from: " + str(connectedSockets[s]))
					inputs.remove(s)
					del connectedSockets[s]
					continue

				# get IP address of user so we know who sent this data
				userIP = connectedSockets[s]

				# get message broken into meaningful pieces (['command', 'arg1', 'arg2', 'word1', 'word2'])
				messageArray = data.split()
				command = messageArray[0].decode('utf-8')

				if (command not in acceptedCommands):
					#send array message saying you didn't send an accepted command
					s.send(bytes("ERROR 200: Received unaccepted command. Try again","utf-8"))
				else: 
					if (command is "register"):
						# expected format: "register <username> <password>"
						checkArguments("register", messageArray, s)

					elif (command is "login"):
						checkArguments("login", messageArray, s)

					elif (command is "logout"):
						checkArguments("logout", messageArray, s)

					elif (command is "sendmsg"):
						checkArguments("sendmsg", messageArray, s)

					elif (command is "listusers"):
						checkArguments("listusers", messageArray, s)

if __name__ == '__main__':
	main()
