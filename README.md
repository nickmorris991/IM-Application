IMApplication README

Student: Nick Morris
Section: TR: 8:00 - 9:20





HOW TO RUN MY PROJECT: 
(this description will be for stdlinux but should apply more generally to any linux machine)

prerequisites:

1) Make sure you have python3 available on your machine of choice.
2) You'll need to be able to open multiple firefox windows to view the output display. So if you're running on the same account in multiple 
boxes of stdlinux you'll need to have multiple firefox profiles available to use (one for each machine). 
	a) to create a new user profile for firefox issue the "firefox -p" command. This will open up the profile wizard
	b) follow wizard's instructions for creating a profile, fairly straightforward.
	c) select start firefox after choosing the new profile you created. 
	d) cancel the request (ctrl+c)
	e) firefox should now auto start with your new user profile on this box

starting the server:

1) open an stdlinux mate/kde machine
2) open terminal
3) navigate to parent folder for project
4) issue command "python3 server.py" 
5) this should start the IM server and bind it to whatever stdlinux machine you're running on

starting the client:

1) open an stdlinux mate/kde machine
2) open terminal
3) navigate to parent folder for project
4) issue command "python3 client.py"
5) you'll be prompted to enter the IP address of the predefined server. Enter whatever IP you ran the server on. 
6) you'll now be prompted to name the .html file that will display your client output. I recommend a simple naming scheme like (c.html, c2.html, c3.html, etc for each new client you start). Make sure you include the file extension in the name, so "c.html" or "c2.html" NOT "c" or "c2".

using the application: 

1) open your output .html display window in a browser (firefox). It should be located in the parent directory of the project after following the instructions defined in the "starting the client" section. 
2) the display will refresh automatically for new output. 
3) Now you should be all set to begin interacting with the IM platform in the terminal (you'll see a prompt "ENTER COMMAND > " to issue valid commands defined by the messaging protocol). 
4) You should issue commands on the terminal and evaluate their output in the .html display window. 





VALID COMMANDS (PROTOCOL):
note: I defined things so that whitespace doesn't matter to the user. so "logout" and "logout   " are the same command. 
note: I define "logged in" and "online" to mean the same thing. This made logical sense to me because if you think about a normal messaging application a user isn't listed as "active" or "online" unless they are also "logged in".

per the document "charts on requirements" on Carmen. Valid commands are as follows:

1) register <username> <password> (e.g. ENTER COMMAND > register dave ogle)
-You can be logged in or logged out for this command. It made logical sense to me to be able to register a new user in either state. 
-You can't have duplicate usernames, but you can have duplicate passwords (obviously)
-You must provde these three arguments separated by at least one space each. 

2) login <username> <password> (e.g. ENTER COMMAND > login dave ogle)
-You must be logged out to issue this command. It didn't make logical sense to me to be able to login as multiple clients. 
-You must provide these three arguments separated by at least one space each. 
-You must issue a valid and registered username
-You must issue the correct password for the provided username
-You must provide a username that isn't already logged in. Therefore, you need to be logged out AND the username you give needs to be logged out.

3) listusers (e.g. ENTER COMMAND > listusers)
-You must provide the single argument above, and only that argument. 
-You must be logged in to issue this command. This made logical sense to me because if you want access to the users who are currently active or logged in, then it would make sense for you to have to be logged in. 

4) sendmsg <username> <message> (e.g. ENTER COMMAND > sendmsg studentA This is professor Ogle, nice work on your documentation.)
-You must provide AT LEAST these three arguments separated by at least one space each. Note that you can have more than three arguments but at minimum you need three. Also note that every argument/word you provide after <username> will count as the message. 
-You must be logged in to issue this command. Note that I define "online" and "logged in" the same. This made logical sense to me because if you think about any normal messaging app a client isn't listed as "online" unless they are logged in (e.g. facebook, instagram, slack, etc)
-You must provide a registered username
-You must provide a username that is currently online/logged in
-You may not send a message to yourself. 

5) logout (e.g. ENTER COMMAND > logout)
-You must provide the single argument above, and only that argument. 
-You must be logged in to issue this command.

