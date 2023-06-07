const { Server } = require('socket.io');
const http = require('http');
const { exec } = require('child_process');
const path = require('path');
const app = require('./app');

const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origins: ['*'],
    },
});

let messages = []

io.on('connection', socket => {

    socket.on("StartTest", async (msg) => {
        const local = path.resolve('methods/Socket.py');
        const cmd = `python3 ${local} ${msg.username} ${msg.durationTime} ${socket.id}`
        exec(cmd)

    });

    socket.on("RunningTest", (msg) => {
        socket.to(msg.id).emit("RunningTest", msg);
    });

    socket.on('ErrorTest', msg => {
        socket.to(msg.id).emit("ErrorTest", msg)
    })

    socket.on('FinishTest', msg => {
        socket.to(msg.id).emit("FinishTest", msg)
    })

    socket.on('sendMessage', data => {
        messages.push(data)
        socket.broadcast.emit('receivedMessage', data)
    })
})

server.listen(3000, () => {
    console.log('listening on *:5000');
});

module.exports = io;


