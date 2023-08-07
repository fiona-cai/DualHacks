var socket = io();

window.powers = [];
window.character = null;
window.match = null;



function send(entry) {
    socket.send(JSON.stringify(entry));
}

socket.on('message', function (msg) {
    const command = JSON.parse(msg).command;
    if (command.name === "match-info"){
        window.match = command.match;
    }
});

send({command: {name: "joining"}});


