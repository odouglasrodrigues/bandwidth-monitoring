const express = require('express')
const path = require('path')
const cors = require('cors');
const shell = require('shelljs')
const { exec } = require("child_process");


const app = express()
const server = require('http').createServer(app)
// const io = require('socket.io')(server)


const io = require('socket.io')(server, {
    cors: {
        origins: ['http://localhost:8080']
    }
});



app.use(cors())
app.use(express.static(path.join(__dirname, 'public')))
app.set('views', path.join(__dirname, 'public'))
app.engine('html', require('ejs').renderFile)
app.set('view engine', 'html')

app.use('/', (req, res) => {
    app.render('index.html')
})

let messages = []

io.on('connection', socket => {
    console.log('Socket Conectado:', socket.id)

    socket.on("StartTest", async (msg) => {
        console.log(socket.id, msg)
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