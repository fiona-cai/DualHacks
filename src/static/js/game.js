window.socket = io();

window.powers = [];
window.player_character = null;
window.opponent_character = null;
window.match = null;

window.username = document.getElementById("username").textContent;
window.match_id = document.getElementById("match_id").textContent;
window.turn = true;

window.current_question = null;

window.game_state = "waiting-for-opponent";


function send(entry) {
    window.socket.send(JSON.stringify(entry));
}

socket.on('message', function (msg) {

    const command = JSON.parse(msg).command;
    console.log(command);

    switch (command.name) {
        case "match-info":
            window.match = command.match;
            break;
        case "character-info":
            window.player_character = command.character;
            document.getElementById("player-image").src = "/static/images/"+command.character.images_buckets_name;
            break;
        case "opponent-character-info":
            window.opponent_character = command.character;
            document.getElementById("opponent-image").src = "/static/images/"+command.character.images_buckets_name;
            break;
        case "power-info":
            window.powers.push(command.power);
            switch (command.power.difficulty) {
                case 1: {
                    document.getElementById("power-1").value = command.power.name;
                    break;
                }
                case 2: {
                    document.getElementById("power-2").value = command.power.name;
                    break;
                }
                case 3: {
                    document.getElementById("power-3").value = command.power.name;
                    break;
                }
            }
            break;
        case "start":
            start_game();
            break;
        case "set-turn":
            window.turn = command.turn == window.username;
            update_turn();
            break;
        case "get-question-response":
            switch (command.response) {
                case "wrong-turn":
                    wrong_turn();
                    break;
                case "okay":
                    window.current_question = command.question;
                    display_question();
                    break;
            }
            break;
        case "time-out":
            display_timeout();
            break;
        case "submit-answer-response":
            switch (command.response) {
                case "wrong-turn":
                    wrong_turn();
                    break;
                case "correct":
                    display_correct_answer();
                    break;
                case "incorrect":
                    display_wrong_answer();
                    break;
            }
            break;
        case "action": {
            if (command.action == "attack") {
                if (command.attacking === window.username) {
                    damage(window.opponent_character, command.damage);
                } else {
                    damage(window.player_character, command.damage);
                }
                break;
            }
            break;
        }
        case "won-game":
            display_win();
            end_game();
            break;
        case "lost-game":
            display_lose();
            end_game();
            break;
    }
});


function start_game() {
    window.game_state = "playing";
    update_health();
}


function get_questions(difficulty) {
    send({
        command:
            {
                name: "get-question",
                subject: window.player_character.subject,
                difficulty: difficulty,
                "match-id": window.match_id
            }
    });
}


function wrong_turn() {
    document.getElementById("message").textContent = "not your turn";
}


function display_question() {
    document.getElementById("question-prompt").textContent = window.current_question.question;

    for (let i = 0; i < window.current_question.options; i++) {
        const option_id = i + 1;
        document.getElementById("option-" + option_id).value = window.current_question.options[i];
    }

    document.getElementById("option-1").value = window.current_question.options[0];
    document.getElementById("option-2").value = window.current_question.options[1];
    document.getElementById("option-3").value = window.current_question.options[2];
    document.getElementById("option-4").value = window.current_question.options[3];

    var modal = document.getElementById("myModal");
    var btn = document.getElementById("modal-open");
    var span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";
}


function submit_answer(option_id) {
    const answer = document.getElementById(option_id).value
    var power = null;
    for (let i = 0; i < window.powers.length; i++) {
        if (window.powers[i].difficulty === window.current_question.difficulty) {
            power = window.powers[i];
        }
    }
    send({
        command: {
            name: "submit-answer",
            "question-id": window.current_question.question_id,
            answer: answer,
            damage: power.damage,
            "match-id": window.match_id
        }
    });

    close_pop_up()
}

function display_correct_answer() {
    document.getElementById("message").textContent = "correct answer";
}


function display_wrong_answer() {
    document.getElementById("message").textContent = "wrong answer";
}


function damage(character, damage) {
    character.health -= damage;
    update_health();
}


function update_health() {
    document.getElementById("player-health").textContent = window.player_character.health;
    document.getElementById("opponent-health").textContent = window.opponent_character.health;
}


function display_timeout() {
    document.getElementById("message").textContent = "timeout";
    close_pop_up();
}


function close_pop_up() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}


function display_win() {
    document.getElementById("message").textContent = "you won";
}


function display_lose() {
    document.getElementById("message").textContent = "you lost";
}


function end_game() {
    window.game_state = "ended"
}

function update_turn() {
    if (window.turn) {
        document.getElementById("turn").textContent = "your turn";
    } else {
        document.getElementById("turn").textContent = "opponent turn";
    }
}

send({command: {name: "joining", username: window.username, "match-id": window.match_id}});
