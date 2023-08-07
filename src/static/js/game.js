var socket = io();

window.powers = [];
window.player_character = null;
window.opponent_character = null;
window.match = null;

window.username = document.getElementById("username").textContent;
window.match_id = document.getElementById("match_id").textContent;
window.turn = true;

window.current_question = null;


function send(entry) {
    socket.send(JSON.stringify(entry));
}

socket.on('message', function (msg) {
    const command = JSON.parse(msg).command;

    switch (command.name) {
        case "match-info":
            window.match = command.match;
            break;
        case "character-info":
            window.player_character = command.character;
            break;
        case "opponent-character-info":
            window.opponent_character = command.character;
            break;
        case "start":
            start_game();
            break;
        case "set-turn":
            window.turn = command.turn === window.username;
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
    }
});


function start_game() {

}


function get_questions(difficulty) {
    send({
        command:
            {
                name: "get-question",
                subject: window.player_character.subject,
                difficulty: difficulty
            }
    });
}


function wrong_turn() {

}


function display_question() {
}


function submit_answer(answer) {
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
            damage: power.damage
        }
    });
}

function display_correct_answer() {

}


function display_wrong_answer() {

}


function damage(character, damage) {
    character.health -= damage;
}


function update_health() {

}


function display_timeout() {

}


send({command: {name: "joining", username: window.username, match_id: window.match_id}});
