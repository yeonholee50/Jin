const express = require('express');
const WebSocket = require('ws');
const { addUser, removeUser, getConnectedUsers, broadcastMessage } = require('./utils/realtime_collaboration');
const { getSharedDocument, updateSharedDocument } = require('./controllers/text_document');

const router = express.Router();

// WebSocket server
const wss = new WebSocket.Server({ noServer: true });

// Handle WebSocket connections
wss.on('connection', (ws) => {
    ws.on('message', (message) => {
        // Broadcast the received message to all connected clients
        broadcastMessage(JSON.parse(message));
    });
});

// Middleware to upgrade HTTP requests to WebSocket requests
router.ws('/ws', (ws, req) => {
    const { userId } = req.query;
    addUser(userId, ws);

    ws.on('close', () => {
        removeUser(userId);
    });
});

// Route to get connected users
router.get('/connectedUsers', (req, res) => {
    const connectedUsers = getConnectedUsers();
    res.json(connectedUsers);
});

// Route to get shared document
router.get('/sharedDocument', (req, res) => {
    const documentContent = getSharedDocument();
    res.json({ content: documentContent });
});

// Route to update shared document
router.post('/updateDocument', (req, res) => {
    const { newContent } = req.body;
    updateSharedDocument(newContent);
    broadcastMessage({ type: 'updateDocument', content: newContent });
    res.sendStatus(200);
});

module.exports = router;

