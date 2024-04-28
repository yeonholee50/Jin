const express = require('express');
const WebSocket = require('ws');
const { addUser, removeUser, getConnectedUsers, broadcastMessage } = require('./utils/realtime_collaboration');
const { getSharedDocument, updateSharedDocument } = require('./controllers/text_document');

const router = express.Router();

// WebSocket server
const wss = new WebSocket.Server({ noServer: true });

// Handle WebSocket connections
wss.on('connection', (ws) => {
    let userId;

    ws.on('message', (message) => {
        const { type, payload } = JSON.parse(message);

        switch (type) {
            case 'auth':
                userId = payload.userId;
                addUser(userId, ws);
                break;
            case 'cursor':
                // Broadcast user cursor position to all other clients
                broadcastMessage({ type: 'cursor', payload });
                break;
            case 'richText':
                // Broadcast rich text formatting changes to all other clients
                broadcastMessage({ type: 'richText', payload });
                break;
            default:
                break;
        }
    });

    ws.on('close', () => {
        if (userId) {
            removeUser(userId);
        }
    });
});

// Middleware to upgrade HTTP requests to WebSocket requests
router.ws('/ws', (ws, req) => {
    // No authentication needed here, as it's handled in the message handler
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


