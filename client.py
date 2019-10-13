import select, socket, errno;
import time

PORT = 5001             # arbitrary non-privileged port
HOST = "164.107.113.68" # retreives host of machine this code is run on

#establish socket and connection to the IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
	command_string = input("ENTER COMMAND > ")

	msgToSend = command_string
	client.sendall(msgToSend.encode('utf-8'))

	data = client.recv(1024)
	print(data.decode('utf-8'))