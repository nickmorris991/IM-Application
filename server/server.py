import socket, select, sys
from process import process_command
from server_session import session

server_info = session() # tracks the sockets, usernames, etc

def get_registered_users():
	users = {}
	try:
		f = open("users.txt", "r")
		names = f.read().split()

		# add names to the list
		i = 0
		while (i+1 < len(names)):
			users[names[i]] = names[i+1]
			i+=2 # skip over passwords

		f.close()
		return users
	except:
		return users


def get_data(cli_socket):
	"""
	APPROACH: recv a predetermined length (buffersize) for incoming message.
	Use this integer to variable the buffer size of the message
	so that we don't run into problems where a message exceeds a fixed length.
	"""
	try:
		msg_size = cli_socket.recv(session.BUFFERSIZE)
		msg = cli_socket.recv(int(msg_size)+10)
		if not len(msg):
			return False #if the client forces disconnection
		return msg
	except:
		return False


def main():
	# create tcp/ip socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)

	# bind our socket and listen for connections
	server.bind((session.HOST, session.PORT))
	server.listen(5) #queue of up to 5 connections

	# list of sockets I expect to read from
	server_info.inputs.append(server)

	#manage input (clients) while server is running
	while server_info.inputs:
		readable, writable, exceptional = select.select(server_info.inputs, server_info.inputs, server_info.inputs)

		for s in readable:
			if s is server:
				# this branch handles connection requests from new clients
				print("received a connection request from a client.")
				client_connection, client_address = server.accept()
				print ("successful connection to: " + str(client_address))

				# save account info
				server_info.connected_sockets[client_connection] = client_address

				# append to running list of sockets
				client_connection.setblocking(0)
				server_info.inputs.append(client_connection) 
			else: 
				# this branch handles existing socket data (sent from clients)
				data = get_data(s)

				# check for forced closed connections and handle/cleanup appropriately
				if data is False:
					print("Closed connection: " + str(server_info.connected_sockets[s]))
					server_info.inputs.remove(s)
					address = server_info.connected_sockets[s]
					if (address in server_info.address_username):
						#if they are logged in when they force closed connection
						server_info.online_list.remove(server_info.address_username[server_info.connected_sockets[s]])
						del server_info.address_username[server_info.connected_sockets[s]]
					del server_info.connected_sockets[s]
					continue

				#process the request given by the client
				message_array = data.split() #split data to avoid whitespace complications
				process_command(message_array, s, server_info)

		for s in exceptional:
			del server_info.connected_sockets[s]

if __name__ == '__main__':
	#retrieve the stored registered users
	server_info.username_password = get_registered_users()
	#start application
	main()