import select, socket, errno;
import time

count = 0
HEADER_SIZE = 10   # used for variable message size 
PORT = 5000        # arbitrary non-privileged port
HOST = "127.0.0.1" # retreives host of machine this code is run on

#establish socket and connection to the IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

inputs = [client]

while 1:
	command_string = input("enter command > ")
	count = count + 1
	msgToSend = command_string
	client.sendall(msgToSend.encode('utf-8'))
	data = client.recv(1024)
	print ("received " + str(data))