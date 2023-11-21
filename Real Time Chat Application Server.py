from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

class Room:
    def __init__(self, id):
        self.id = id
        self.users = []
        self.messages = []

    def add_user(self, username):
        self.users.append(username)

    def remove_user(self, username):
        self.users.remove(username)

    def add_message(self, username, message):
        new_message = {'username': username, 'message': message}
        self.messages.append(new_message)
        return new_message

chat_rooms = {}

@socketio.on('joinRoom')
def join_room(data):
    username = data['username']
    room_id = data['roomId']
    join_room(room_id)

    if room_id not in chat_rooms:
        chat_rooms[room_id] = Room(room_id)

    room = chat_rooms[room_id]
    room.add_user(username)

    emit('userJoined', {'username': username, 'roomId': room_id, 'users': room.users}, room=room_id)

@socketio.on('leaveRoom')
def leave_room(data):
    username = data['username']
    room_id = data['roomId']
    leave_room(room_id)

    room = chat_rooms[room_id]
    room.remove_user(username)

    emit('userLeft', {'username': username, 'roomId': room_id, 'users': room.users}, room=room_id)

@socketio.on('sendMessage')
def send_message(data):
    username = data['username']
    room_id = data['roomId']
    message = data['message']

    room = chat_rooms[room_id]
    new_message = room.add_message(username, message)

    emit('messageReceived', new_message, room=room_id)

@socketio.on('disconnect')
def disconnect():
    print('User disconnected')

if __name__ == '__main__':
    socketio.run(app)
