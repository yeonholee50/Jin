const WebSocket = require('ws');

const connectedUsers = new Map(); // Map to store WebSocket connections of users

const addUser = (userId, ws) => {
    connectedUsers.set(userId, ws);
    console.log(`User ${userId} connected.`);
};

const removeUser = (userId) => {
    connectedUsers.delete(userId);
    console.log(`User ${userId} disconnected.`);
};

const getConnectedUsers = () => {
    return Array.from(connectedUsers.keys());
};

const broadcastMessage = (message) => {
    connectedUsers.forEach(ws => {
        ws.send(JSON.stringify(message));
    });
};

module.exports = {
    addUser,
    removeUser,
    getConnectedUsers,
    broadcastMessage
};

