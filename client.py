import select, socket, sys, time, threading;
import os;
from os import path;

#get the name for the client output display
clientName = ""

#used to send message length for variable recv
BUFFERSIZE = 10

#define port and host for connection
PORT = 5001
HOST = input("Enter server host IP: ")

#establish socket and connection to the user defined IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.setblocking(1)


def getSetupClientInfo(): 
	"""
	This function prompts the user to define a .html file to display their output.
	"""
	cliName = ""

	#get display name for this client
	while (cliName == "" or cliName == "client.html" or cliName == "client.py" or cliName == "client"):
		cliName = input("Enter name for display file (e.g. client1Output.html), DONT USE NAME \"client\": ")

	print()
	print("use the console/terminal for input and the file just created to view output")
	print("it will update in real time, no need to refresh")
	print()
	print("Ready to send messages! Have fun!")
	print("note: See the documentation for how to enter commands")
	print()

	return cliName

def createHTMLTemplate(file):
	"""
	This function creates the baseline HTML code to use as a template to add things to
	"""
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
	"""used to ouptut responses from the server to the HTML display"""
	f = open(clientName, "ab")
	f.seek(-14, 2)
	f.write(bytes("<p> $ ", "utf-8")) 
	f.write(bytes(message, "utf-8"))
	f.write(bytes("</p>\n", "utf-8"))
	f.close()

def getInput():
	"""
	used to prompt the client for an input command.
	to see how these commands are defined please see the
	documentation folder in the project. 
	"""
	while True:
		command_string = input("ENTER COMMAND > ")
		if (len(command_string) > 0):
			break
	return command_string

def getBuffer():
	"""used to create a buffer string fro the message protocal"""
	i = 0
	buff = ""
	while (i < BUFFERSIZE): 
		buff = buff + " "
		i+=1
	return buff

def outputSendMsg(messageList):
	"""
	used to output client side attempted messages sent
	Format: "me to <username> > <message>"
	"""

	#build output (me to username > message) and print
	messageIndex = 2

	outputString = "me to " + str(messageList[1]) + " > "

	while (messageIndex < len(messageList)):
		outputString += messageList[messageIndex] + " "
		messageIndex+=1

	#output attempted message to client display
	outputToHTMLDisplay(outputString)

def recvThread():
	"""used to manage the receiving thread for taking in data client side"""
	while True:
		try:
			"""
			#receive data in chunks of maximum 1024. If we receive an especially long message
			#it will just print on mulitple output lines. This seems acceptable to me.  
			"""
			data = client.recv(1024)
			if not data: sys.exit(0)
			outputToHTMLDisplay(data.decode('utf-8'))
		except:
			#we've executed "leave" command
			sys.exit(0)

def main():
	"""
	the approach I used server side didn't work with stdinput like it's
	described in the provided template files. So I went with a multi threaded
	approach client side. It's logically fairly similar
	"""

	#open and create a display for the client
	if (path.exists(clientName) and clientName != "client" and clientName != "client.py"):
		os.remove(clientName) #if the file is already in OS, start fresh

	f = open(clientName,"w+")
	createHTMLTemplate(f)
	f.close()

	#initialize and start the thread for receiving messages
	threading.Thread(target=recvThread).start()

	#loop to ask for input and send the data to the IM server
	while True
:		# get command issued to server
		command_string = getInput()

		# handle special cases for the command
		if ("sendmsg" == command_string[0:7]):
			messageList = command_string.split()
			outputSendMsg(messageList)


		"""
		construct message data to send to IM server. 
		Data sent to server has the following format:
		<msgSize> <buffer> <msg> 
		"""
		msgSize = str(len(command_string))
		buff = getBuffer()
		msg = msgSize + buff + command_string

		# send command message to the IM server for processing
		client.send(bytes(msg,"utf-8"))

if __name__ == '__main__': 
	clientName = getSetupClientInfo()
	main()
