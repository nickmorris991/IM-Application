# input validation checks (see documenation for full list)
def valid_arg(command_name, message_array, client, session):

	if (command_name == "register"):
		# check length
		if (len(message_array) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		# check unique username
		elif (message_array[1].decode('utf-8') in session.username_password.keys()):
			client.send(bytes("ERROR 202: Username taken", "utf-8"))
			return False 
		return True

	elif (command_name == "login"):
		# if the client issuing the 'login' command is already logged in return error 
		if (session.connected_sockets[client] in session.address_username):
			client.send(bytes("ERROR 208: logout before logging in again", "utf-8"))
			return False
		# check length
		if (len(message_array) != 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False

		# check password and username errors
		given_username = message_array[1].decode('utf-8')
		given_password = message_array[2].decode('utf-8')
		if (given_username not in session.username_password.keys()):
			client.send(bytes("ERROR 203: Unregistered username","utf-8"))
			return False
		elif(session.username_password[given_username] != given_password):
			client.send(bytes("ERROR 204: Incorrect password","utf-8"))
			return False
		elif(given_username in session.online_list):
			client.send(bytes("ERROR 207: user already signed in","utf-8"))
			return False
		
		return True

	elif (command_name == "logout"):
		if (len(message_array) != 1):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False
		elif (session.connected_sockets[client] not in session.address_username):
			client.send(bytes("ERROR 206: must be logged in to issue command", "utf-8"))
			return False
	
		return True
        
	elif (command_name == "sendmsg"):
		#check length
		if (len(message_array) < 3):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False

		given_username = message_array[1].decode('utf-8')
		clientAddress = session.connected_sockets[client]
		if (clientAddress not in session.address_username):
			client.send(bytes("ERROR 206: must be logged in to issue command", "utf-8"))
			return False
		if (given_username not in session.username_password):
			client.send(bytes("ERROR 203: Unregistered username","utf-8"))
			return False
		if (given_username not in session.online_list):
			client.send(bytes("ERROR 211: user isn't online", "utf-8"))
			return False

		clientUsername = session.address_username[clientAddress]
		# check for self sent messages, we don't allow those.
		if (given_username == clientUsername):
			client.send(bytes("ERROR 212: self sent message", "utf-8"))
			return False
		return True

	elif (command_name == "listusers"):
		#check length 
		if (len(message_array) != 1):
			client.send(bytes("ERROR 201: Incorrect number of arguments", "utf-8"))
			return False

		address = session.connected_sockets[client]
		if (address not in session.address_username):
			client.send(bytes("ERROR 206: must be online to issue command", "utf-8"))
			return False
		return True