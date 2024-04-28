const express = require('express');
const router = express.Router();
const { addUser, removeUser, getConnectedUsers } = require('./utils/realtime_collaboration');
const { getSharedDocument, updateSharedDocument } = require('./controllers/text_document');

// Route to add a user
router.post('/addUser', (req, res) => {
    const { userId } = req.body;
    addUser(userId);
    res.sendStatus(200);
});

// Route to remove a user
router.post('/removeUser', (req, res) => {
    const { userId } = req.body;
    removeUser(userId);
    res.sendStatus(200);
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
    res.sendStatus(200);
});

module.exports = router;
