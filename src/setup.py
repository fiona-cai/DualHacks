from flask import Flask
from flask_socketio import SocketIO
from networking import Server

app = Flask(__name__)

app.config.from_object('settings')
socket_app = SocketIO(app)
server = Server(None, None, app, socket_app)
