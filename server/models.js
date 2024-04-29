const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Define schema for posts
const postSchema = new Schema({
    title: String,
    content: String,
    author: { type: Schema.Types.ObjectId, ref: 'User' },
    comments: [{ type: Schema.Types.ObjectId, ref: 'Comment' }],
    likes: [{ type: Schema.Types.ObjectId, ref: 'User' }]
});

// Define schema for comments
const commentSchema = new Schema({
    content: String,
    author: { type: Schema.Types.ObjectId, ref: 'User' },
    post: { type: Schema.Types.ObjectId, ref: 'Post' }
});

// Define schema for users
const userSchema = new Schema({
    username: String,
    email: String,
    password: String,
    posts: [{ type: Schema.Types.ObjectId, ref: 'Post' }],
    comments: [{ type: Schema.Types.ObjectId, ref: 'Comment' }],
    likes: [{ type: Schema.Types.ObjectId, ref: 'Post' }]
});

const Post = mongoose.model('Post', postSchema);
const Comment = mongoose.model('Comment', commentSchema);
const User = mongoose.model('User', userSchema);

module.exports = {
    Post,
    Comment,
    User
};
