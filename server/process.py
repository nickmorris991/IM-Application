from validation import valid_arg
from server_session import session

# logic behind each command
def process_command(message_array, client, server_info):
	command = message_array[0].decode('utf-8')
	user_address = server_info.connected_sockets[client]

	if (command not in session.ACCEPTED_COMMANDS):
		client.send(bytes("ERROR 200: Received unaccepted command.","utf-8"))
	else: 
		if (command == "register"):
			# expected format: "register <username> <password>"
			if (valid_arg("register", message_array, client, server_info)):
				username = message_array[1].decode('utf-8')
				password = message_array[2].decode('utf-8')
				# save the user to our database (file) and add to the in app datastructure
				add_user_to_file(username, password)
				server_info.username_password[username] = password
				#notify client/server
				print("registered new user: " + str(username))
				client.send(bytes("registered successfully", "utf-8"))

		elif (command == "login"):
			if (valid_arg("login", message_array, client, server_info)):
				# associate user address with their username.
				username = message_array[1].decode('utf-8')
				server_info.address_username[user_address] = username
				# add them to the list of online users
				server_info.online_list.append(username)
				#notify client/server
				print("successfully logged in user: " + str(username))
				client.send(bytes("login successful", "utf-8"))

		elif (command == "logout"):
			if (valid_arg("logout", message_array, client, server_info)):
				caller_address = server_info.connected_sockets[client]
				caller_username = server_info.address_username[caller_address]
				#cleanup user
				server_info.online_list.remove(caller_username)
				del server_info.address_username[caller_address]
				#notify client/server
				print("successfully logged out user: " + str(caller_username))
				client.send(bytes("successfully logged out", "utf-8"))

		elif (command == "sendmsg"):
			if (valid_arg("sendmsg", message_array, client, server_info)):
				#get sender's username
				sender_address = server_info.connected_sockets[client]
				sender_username = server_info.address_username[sender_address]

				#get sending address
				sending_username = message_array[1].decode('utf-8')
				sending_address = get_address(sending_username, server_info)

				#build output
				i = 2
				output = str(sender_username) + " > "
				while (i < len(message_array)):
					output += message_array[i].decode('utf-8') + " "
					i+=1

				#notify server
				print("sent a message to: " + str(sending_username) + " from: " + str(sender_username))

				#get sending socket and send message
				sendingSocket = get_socket(sending_address, server_info)
				sendingSocket.send(bytes(output, "utf-8"))

		elif (command == "listusers"):
			if (valid_arg("listusers", message_array, client, server_info)):
				print("Issued 'listusers' command")
				client.send(bytes("\n".join(server_info.online_list), "utf-8"))


def add_user_to_file(username, password):
	f = open("users.txt", "a+")
	f.write('\n')
	f.write(username)
	f.write('\n')
	f.write(password)
	f.write('\n')
	f.close()


def get_address(sending_username, server_info):
	#iterate over logged in users (addressUsername) and return matching address
	for address, username in server_info.address_username.items():
		if (username == sending_username):
			return address


def get_socket(sending_address, server_info):
	#iterate over connectedSockets and return the socket associated with "sendingAddress"
	for socket, address in server_info.connected_sockets.items():
		if (address == sending_address):
			return socket