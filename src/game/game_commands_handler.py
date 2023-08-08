import random
import threading
import time

from networking import send_individual

import database.match_db_manager as match_db
import database.character_db_manager as character_db
import database.questions_db_manager as question_db


def joining(command, client):
    client.username = command["username"]

    players = match_db.get_match_players(command["match-id"])
    player = list(filter(lambda x: x.username == client.username, players))[0]

    character = character_db.get_character_by_name(player.character)

    match = match_db.get_match_by_id(command["match-id"])

    player.client_id = client.code
    match_db.update_player(match.match_id, player)

    client.send({"command": {"name": "match-info", "match": match.__dict__}})
    client.send({"command": {"name": "character-info", "character": character.__dict__}})
    [client.send({"command": {"name": "power-info", "power": power}}) for power in character.powers]

    if match.player_count == 2:
        match.started = True
        match.turn = players[0].username
        match_db.update_match(match)
        for player in players:
            for player_sender in players:
                if player.username != player_sender.username:
                    print("sending opponent")
                    character = character_db.get_character_by_name(player.character)
                    send_individual({"command": {"name": "opponent-character-info", "character": character.__dict__}}, player_sender.client_id)
        [send_individual({"command": {"name": "start"}}, player.client_id) for player in players]
        [send_individual({"command": {"name": "set-turn", "turn": match.turn}}, player.client_id) for player in players]


def get_question(command, client):
    match = match_db.get_match_by_id(command["match-id"])
    if match.turn != client.username:
        client.send({"command": {"name": "get-question-response", "response": "wrong turn"}})
        return

    questions = question_db.get_questions_by_subject_and_difficulty(command["subject"], command["difficulty"])
    random.shuffle(questions)
    question = questions[0]
    question.answer = None

    client.send({"command": {"name": "get-question-response", "response": "okay", "question": question.__dict__}})
    match.waiting_timeout_id += 1
    match_db.update_match(match)


def submit_answer(command, client):
    match = match_db.get_match_by_id(command["match-id"])
    if match.turn != client.username:
        client.send({"command": {"name": "submit-answer-response", "response": "wrong turn"}})
        return

    match.waiting_timeout_id += 1
    match_db.update_match(match)

    players = match_db.get_match_players(match.match_id)
    question = question_db.get_question_by_id(command["question-id"])

    if question.answer == command["answer"]:
        client.send({"command": {"name": "submit-answer-response", "response": "correct"}})

        for player in players:
            if player.client_id != client.code:
                player.health -= int(command["damage"])
            else:
                player.points += 1
            match_db.update_player(match.match_id, player)

        [send_individual({"command": {"name": "action", "action": "attack", "attacking": match.turn, "damage": command["damage"]}},
              player.client_id) for player in players]

    else:
        client.send({"command": {"name": "submit-answer-response", "response": "incorrect"}})
        [send_individual({"command": {"name": "action", "action": "empty"}}, player.client_id) for player in players]

    for player in players:
        print(player.health, player.username)
        if player.health <= 0:
            end_game(players)
            match.started = "ended"
            match_db.update_match(match)
            return

    switch_turn(match)


def switch_turn(match):
    players = match_db.get_match_players(match.match_id)
    if match.turn == players[0].username:
        match.turn = players[1].username
    else:
        match.turn = players[0].username

    match_db.update_match(match)

    [send_individual({"command": {"name": "set-turn", "turn": match.turn}}, player.client_id) for player in players]


def end_game(players):
    for player in players:
        if player.health <= 0:
            send_individual({"command": {"name": "lost-game"}}, player.client_id)
        else:
            send_individual({"command": {"name": "won-game"}}, player.client_id)


def time_out(match_id, timeout_id, client):
    match = match_db.get_match_by_id(match_id)
    time.sleep(30)
    if match.waiting_timeout_id != timeout_id:
        return
    client.send({"command": {"name": "time-out"}})
    switch_turn(match)
