import select, socket, sys, time, threading;
import os;
from os import path;

#get the name for the client output display
clientName = ""

#define port and host for connection
PORT = 5001
HOST = input("Enter server host IP: ")

#establish socket and connection to the IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.setblocking(1)


def getSetupClientInfo(): 
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
	while True:
		command_string = input("ENTER COMMAND > ")
		if (len(command_string) > 0):
			break
	return command_string

def outputSendMsg(messageList):
	#build output (me to username > message) and print
	messageIndex = 2

	outputString = "me to " + str(messageList[1]) + " > "

	while (messageIndex < len(messageList)):
		outputString += messageList[messageIndex] + " "
		messageIndex+=1

	#output attempted message to client display
	outputToHTMLDisplay(outputString)

def recvThread():
	while True:
		try:
			data = client.recv(1024)
			if not data: sys.exit(0)
			outputToHTMLDisplay(data.decode('utf-8'))
		except:
			#we've executed "leave"
			sys.exit(0)

def main():
	"""the approach I used server side didn't work with stdinput like it's
	described in the provided template files. So I went with a multi threaded
	approach client side. It's fairly similar"""

	#open and create a display for the client
	if (path.exists(clientName) and clientName != "client" and clientName != "client.py"):
		os.remove(clientName) #if the file is already in OS, start fresh

	f = open(clientName,"w+")
	createHTMLTemplate(f)
	f.close()

	#initialize and start the thread for receiving messages
	threading.Thread(target=recvThread).start()

	#loop to ask for input and send the data to the IM server
	while True:
		# get command
		command_string = getInput()
		if ("sendmsg" == command_string[0:7]):
			messageList = command_string.split()
			outputSendMsg(messageList)

		if ("leave" == command_string):
			print("exiting IM application")
			client.close()
			sys.exit(0)

		# send command
		client.send(bytes(command_string,"utf-8"))

if __name__ == '__main__': 
	clientName = getSetupClientInfo()
	main()