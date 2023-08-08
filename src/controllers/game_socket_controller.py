from flask_socketio import SocketIO
from networking import Client
from flask import request
from setup import socket_app, server
import game.game_commands_handler as command_handler

import json


@socket_app.on("connect")
def new_connection():
    client_id = request.sid
    client = Client(client_id, server, None)
    server.list_of_all_clients.append(client)
    print("new client", request.sid)


@socket_app.on("message")
def message_handler(message):
    message = json.loads(message)
    command = message["command"]
    print(command)

    client = list(filter(lambda x: x.code == request.sid, server.list_of_all_clients))[0]


    if command["name"] == "joining":
        command_handler.joining(command, client)

    elif command["name"] == "get-question":
        command_handler.get_question(command, client)

    elif command["name"] == "submit-answer":
        command_handler.submit_answer(command, client)

    """
    commands:
    joining
    start-game
    set-turns
    submit-answer
    time-out
    win
    lose
    get-game-info-update
    wrong-match-id
    game-ended """

