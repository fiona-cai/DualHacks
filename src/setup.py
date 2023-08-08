from datetime import timedelta

from flask import Flask
from flask_socketio import SocketIO
from networking import Server
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object('settings')
Flask.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(hours=10)
socket_app = SocketIO(app)
server = Server("127.0.0.1", 5000, app, socket_app)

mail = Mail(app)
