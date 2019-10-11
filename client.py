import select, socket, sys;
# Echo client program
count = 0
HOST = socket.gethostname()    # The remote host
PORT = 5000                    # The same port as used by the server

#establish socket and connection to the IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = s.recv(1024)
print(message.decode("utf-8"))


# inputs = [s, sys.stdin]
# command_string = raw_input("enter string for me to keep echoing to server -> ")
# while 1:    
# 	count = count+1    
# 	msgToSend = command_string    
# 	s.sendall(msgToSend)    
# 	data = s.recv(1024)    
# 	print 'Received', repr(data)    
# 	time.sleep(5)

s.close()