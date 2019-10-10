import select, socket, sys, Queue
# Echo client program

import socket
import time
count = 0
HOST = 'localhost'    # The remote host
PORT = 5001           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
inputs = [s, sys.stdin]
command_string = raw_input("enter string for me to keep echoing to server -> ")
while 1:    
	count = count+1    
	msgToSend = command_string    
	s.sendall(msgToSend)    
	data = s.recv(1024)    
	print 'Received', repr(data)    
	time.sleep(5)

s.close()