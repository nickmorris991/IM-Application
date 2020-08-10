import select, socket, sys, time, threading
import os
from os import path
from client_session import session

client_info = session()

#define port and host for connection
client_info.host = input("Enter server host IP: ")

#establish socket and connection to the user defined IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((client_info.host, client_info.port))
client.setblocking(1)


# This function prompts the user to define a .html file to display their output.
def get_setup_client_info(): 
	
	cli_name = ""

	#get display name for this client
	while (cli_name == "" or cli_name == "client.html" or cli_name == "client.py" or cli_name == "client"):
		cli_name = input("Enter name for display file (e.g. client1Output.html), DONT USE NAME \"client\": ")

	print()
	print("use the console/terminal for input and the file just created to view output")
	print("it will update in real time, no need to refresh")
	print()
	print("Ready to send messages! Have fun!")
	print("note: See the documentation for how to enter commands")
	print()

	return cli_name


# This function creates the baseline HTML code to use as a template to add things to
def create_HTML_template(file):
	file.write("<!DOCTYPE html>\n")
	file.write("<html>\n")
	file.write("<head>\n")
	file.write("<meta http-equiv=\"refresh\" content=\"1\">\n")
	file.write("</head>\n")
	file.write("<body>\n")
	file.write("<h1>Client Output</h1>\n")
	file.write("</body>\n")
	file.write("</html>\n")


# used to ouptut responses from the server to the HTML display
def output_to_HTML_display(message):
	f = open(client_info.client_name, "ab")
	f.seek(-14, 2)
	f.write(bytes("<p> $ ", "utf-8")) 
	f.write(bytes(message, "utf-8"))
	f.write(bytes("</p>\n", "utf-8"))
	f.close()


# used to prompt the client for an input command.
def get_input():
	while True:
		command_string = input("ENTER COMMAND > ")
		if (len(command_string) > 0):
			break
	return command_string


# used to create a buffer string for the message protocal
def get_buffer():
	return ' ' * session.BUFFERSIZE


"""
used to output client side attempted messages sent
Format: "me to <username> > <message>"
"""
def output_send_msg(message_list):
	#build output (me to username > message) and print
	message_index = 2

	output_string = "me to " + str(message_list[1]) + " > "

	while (message_index < len(message_list)):
		output_string += message_list[message_index] + " "
		message_index+=1

	#output attempted message to client display
	output_to_HTML_display(output_string)


#used to manage the receiving thread for taking in data client side
def recv_thread():
	while True:
		try:
			"""
			receive data in chunks of maximum 1024. If we receive an especially long message
			it will just print on mulitple output lines. This seems acceptable to me.  
			"""
			data = client.recv(1024)
			if not data: sys.exit(0)
			output_to_HTML_display(data.decode('utf-8'))
		except:
			#we've executed "leave" command
			sys.exit(0)


def main():
	#open and create a display for the client
	if (path.exists(client_info.client_name) and client_info.client_name != "client" and client_info.client_name != "client.py"):
		os.remove(client_info.client_name) #if the file is already in OS, start fresh

	f = open(client_info.client_name,"w+")
	create_HTML_template(f)
	f.close()

	#initialize and start the thread for receiving messages
	threading.Thread(target=recv_thread).start()

	#loop to ask for input and send the data to the IM server
	while True:		
	        # get command issued to server
		command_string = get_input()

		# handle special cases for the command
		if ("sendmsg" == command_string[0:7]):
			message_list = command_string.split()
			output_send_msg(message_list)
			
		# construct packet <msgSize> <buffer> <msg> 
		msg_size = str(len(command_string))
		buff = get_buffer()
		msg = msg_size + buff + command_string

		# send command message to the IM server for processing
		client.send(bytes(msg,"utf-8"))

if __name__ == '__main__': 
	client_info.client_name = get_setup_client_info()
	main()