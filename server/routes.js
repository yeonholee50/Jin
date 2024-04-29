const express = require('express');
const WebSocket = require('ws');
const { addUser, removeUser, getConnectedUsers, broadcastMessage } = require('./utils/realtime_collaboration');
const { getSharedDocument, updateSharedDocument } = require('./controllers/text_document');


const router = express.Router();
const { Post, Comment, User } = require('./models');
const { sendNotification } = require('./utils/notifications');
const contentModerationMiddleware = require('./middleware/content_moderation');

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

// Route to get user analytics
router.get('/userAnalytics', async (req, res) => {
    try {
        const users = await User.find().populate('posts').populate('comments').populate('likes');
        const userAnalytics = users.map(user => {
            return {
                userId: user._id,
                username: user.username,
                numPosts: user.posts.length,
                numComments: user.comments.length,
                numLikes: user.likes.length
            };
        });
        res.json(userAnalytics);
    } catch (error) {
        console.error('Error fetching user analytics:', error);
        res.status(500).json({ error: 'Could not fetch user analytics' });
    }
});

// Route to update shared document
router.post('/updateDocument', (req, res) => {
    const { newContent } = req.body;
    updateSharedDocument(newContent);
    broadcastMessage({ type: 'updateDocument', content: newContent });
    res.sendStatus(200);
});

// Route to create a new post
router.post('/posts', async (req, res) => {
    const { title, content, authorId } = req.body;

    try {
        const newPost = new Post({
            title,
            content,
            author: authorId
        });

        await newPost.save();
        res.status(201).json(newPost);
    } catch (error) {
        console.error('Error creating post:', error);
        res.status(500).json({ error: 'Could not create post' });
    }
});

// Route to get all posts
router.get('/posts', async (req, res) => {
    try {
        const posts = await Post.find().populate('author', 'username').populate('comments').populate('likes');
        res.json(posts);
    } catch (error) {
        console.error('Error fetching posts:', error);
        res.status(500).json({ error: 'Could not fetch posts' });
    }
});

// Route to create a new comment
router.post('/comments', async (req, res) => {
    const { content, authorId, postId } = req.body;

    try {
        const newComment = new Comment({
            content,
            author: authorId,
            post: postId
        });

        await newComment.save();

        const post = await Post.findByIdAndUpdate(postId, { $push: { comments: newComment._id } }, { new: true });
        res.status(201).json(post);

        // Notify post author about the new comment
        const postAuthor = await User.findById(post.author);
        if (postAuthor) {
            sendNotification(postAuthor._id, { type: 'notification', message: `New comment on your post: ${post.title}` });
        }
    } catch (error) {
        console.error('Error creating comment:', error);
        res.status(500).json({ error: 'Could not create comment' });
    }
});

// Route to create a new comment
router.post('/comments', contentModerationMiddleware, async (req, res) => {
    const { content, authorId, postId } = req.body;

    try {
        const newComment = new Comment({
            content,
            author: authorId,
            post: postId
        });

        await newComment.save();

        const post = await Post.findByIdAndUpdate(postId, { $push: { comments: newComment._id } }, { new: true });
        res.status(201).json(post);

        // Notify post author about the new comment
        const postAuthor = await User.findById(post.author);
        if (postAuthor) {
            sendNotification(postAuthor._id, { type: 'notification', message: `New comment on your post: ${post.title}` });
        }
    } catch (error) {
        console.error('Error creating comment:', error);
        res.status(500).json({ error: 'Could not create comment' });
    }
});

// Route to like a post
router.post('/posts/:postId/like', async (req, res) => {
    const { userId } = req.body;
    const { postId } = req.params;

    try {
        const post = await Post.findByIdAndUpdate(postId, { $addToSet: { likes: userId } }, { new: true });
        res.json(post);
    } catch (error) {
        console.error('Error liking post:', error);
        res.status(500).json({ error: 'Could not like post' });
    }
});

module.exports = router;


