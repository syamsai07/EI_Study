import socketio

# Initialize SocketIO client
sio = socketio.Client()

# Connect to the server
sio.connect('http://localhost:3000')

# Join a chat room
sio.emit('joinRoom', {'username': 'Alice', 'roomId': 'Room123'})

# Receive a new message
@sio.on('messageReceived')
def on_message_received(data):
    username = data['username']
    message = data['message']
    print(f'{username}: {message}')

# Receive user joined event
@sio.on('userJoined')
def on_user_joined(data):
    username = data['username']
    users = data['users']
    print(f'{username} joined the room')
    print('Active users:', users)

# Receive user left event
@sio.on('userLeft')
def on_user_left(data):
    username = data['username']
    users = data['users']
    print(f'{username} left the room')
    print('Active users:', users)

# Send a chat message
message = input('Enter a message: ')
sio.emit('sendMessage', {'username': 'Alice', 'roomId': 'Room123', 'message': message})

# Leave the chat room
sio.emit('leaveRoom', {'username': 'Alice', 'roomId': 'Room123'})
