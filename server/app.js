const express = require('express');
const app = express();
const mongoose = require('mongoose');
require('dotenv').config();

const authRoutes = require('./routes/authRoutes');
const ideasRoutes = require('./routes/ideasRoutes');
const { requireAuth } = require('./middleware/authMiddleware');

app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Error connecting to MongoDB:', err.message));

// Routes
app.use('/auth', authRoutes);
app.use('/ideas', requireAuth, ideasRoutes);

module.exports = app;

