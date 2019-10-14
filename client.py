import select, socket, sys, time, threading;
import os;
from os import path;

PORT = 5001             # arbitrary non-privileged port
#HOST = "164.107.113.68" # retreives host of machine this code is run on
HOST = "127.0.0.1"
clientName = None

#establish socket and connection to the IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.setblocking(1)

def createHTMLTemplate(file):
	file.write("<!DOCTYPE html>\n")
	file.write("<html>\n")
	file.write("<head>\n")
	file.write("<meta http-equiv=\"refresh\" content=\"1\">\n")
	file.write("</head>\n")
	file.write("<body>\n")
	file.write("<h1>Client Output</h1>\n")
	file.write("</body>\n")
	file.write("</html>\n")

def outputToHTMLDisplay(message):
	f = open(clientName, "ab")
	f.seek(-14, 2)
	f.write(bytes("<p> $ ", "utf-8")) 
	f.write(bytes(message, "utf-8"))
	f.write(bytes("</p>\n", "utf-8"))
	f.close()

def getInput():
	command_string = input("ENTER COMMAND > ")

	return command_string

def loginOrRegDecision():
	while (True):
		command_string = input("login or register? > ")
		if (len(command_string) > 0): 
			break
	return command_string

def getUsername():
	while(True):
		username = input("username > ")
		if (len(username) > 0): 
			break
	return username

def getPassword():
	while(True):
		password = input("password > ")
		if (len(password) > 0): 
			break
	return password

def getLoggedInCommand():
	while(True):
		command = input("sendmsg, logout, or listusers? > ")
		if (len(command) > 0): 
			break
	return command

def getMessage():
	while(True):
		message = input("enter message > ")
		if (len(message) > 0):
			break
	return message

def recvThread():
	while True:
		data = client.recv(1024)
		if not data: sys.exit(0)
		outputToHTMLDisplay(data.decode('utf-8'))

def main():
	"""the approach I used server side didn't work with stdinput like it's
	described in the provided template files. So I went with a multi threaded
	approach client side. It's fairly similar"""

	if (path.exists(clientName)):
		os.remove(clientName) #if the file is already in OS, start fresh

	f = open(clientName,"w+")
	createHTMLTemplate(f)
	f.close()

	threading.Thread(target=recvThread).start()
	while True:
		command_string = getInput()
		client.send(bytes(command_string,"utf-8"))
	
if __name__ == '__main__': 
	clientName = input("Enter name for output display, this is not a username (e.g. client1Output.html): ")
	print("use the console/terminal for input and the file just created to view output")
	print("it will update in real time, no need to refresh")

	main()