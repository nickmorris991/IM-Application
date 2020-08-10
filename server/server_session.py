class session:
    BUFFERSIZE = 5         # used to receive length of each message and scale recv buffer size based on message length
    PORT = 5001            # server port
    HOST = ''              # host of machine this code is executed on

    ACCEPTED_COMMANDS = ["register", "login", "logout", "sendmsg", "listusers"]

    def __init__(self):

        self.inputs = []             # list of sockets

        # note: socket -> address -> username -> password 
        self.connected_sockets = {}  # dict to save socket info (key=cliSocket, value=IP)
        self.address_username = {}   # dict for sending messages (key=address, value=username)
        self.username_password = {}  # dict for password validation (key=username, value=password)
        self.online_list = []        # list of online users (defined as users who have logged in)

