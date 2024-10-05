// server.js
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: '*',
    }
});

io.on('connection', (socket) => {
    console.log('New client connected');

    socket.on('workspace-update', (data) => {
        // Broadcast updates to other clients
        socket.broadcast.emit('workspace-update', data);
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

server.listen(5002, () => {
    console.log('HoloSpace backend running on port 5002');
});
