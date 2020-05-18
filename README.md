# IMApplication README
- A simple terminal instant messaging application to practice TCP socket programming. 

## How To Run
(this description will be for stdlinux but should apply more generally to any linux machine)

starting the server:

2) open terminal
3) navigate to parent folder for project
4) issue command "python3 server.py" 
5) this will start the server and bind it to the host

starting the client:

1) open an stdlinux mate/kde machine
2) open terminal
3) navigate to parent folder for project
4) issue command "python3 client.py"
5) Enter whatever IP you ran the server on. 
6) Name the .html file that will display your client output. Include file extension in the name.
*if you're running multiple clients on the same linux machine, name their display output files differently. 

## Using The Application: 

1) Open your output .html. It will be located in the parent directory of the project.
2) The display will refresh automatically for new output. 
3) Issue commands in the terminal, view output in the .html file.

### Valid Commands
note: I defined things so that whitespace doesn't matter to the user. so "logout" and "logout   " are the same command. 

Valid commands are as follows:

1) register <username> <password> (e.g. ENTER COMMAND > register dave ogle)
-You can be logged in or logged out for this command.
-You must provde these three arguments separated by at least one space each. 

2) login <username> <password> (e.g. ENTER COMMAND > login dave ogle)
-You must be logged out to issue this command.
-You must provide these three arguments separated by at least one space each. 
-You must issue a valid and registered username
-You must issue the correct password for the provided username
-You must provide a username that isn't already logged in.

3) listusers (e.g. ENTER COMMAND > listusers)
-This command lists all active users. You must be logged in to issue this command.

4) sendmsg <username> <message> (e.g. ENTER COMMAND > sendmsg userA test message.)
-You must provide AT LEAST these three arguments separated by at least one space each. 
-You must be logged in to issue this command. Note that I define "online" and "logged in" the same.
-You must provide a registered username
-You must provide a username that is currently online/logged in
-You may not send a message to yourself. 

5) logout (e.g. ENTER COMMAND > logout)
-You must provide the single argument above, and only that argument. 
-You must be logged in to issue this command.

