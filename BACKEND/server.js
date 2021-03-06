const express = require('express')
const cors = require('cors');
const { exec } = require("child_process");

const app = express()
const server = require('http').createServer(app)

const io = require('socket.io')(server, {
    cors: {
        origins: ['*']
    }
});

app.use(cors())

let messages = []

io.on('connection', socket => {

    socket.on("StartTest", async (msg) => {
        const cmd = `python Socket.py ${msg.username} ${msg.durationTime} ${socket.id}`
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

server.listen(3000)