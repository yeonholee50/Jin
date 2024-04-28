const express = require('express');
const app = express();
const ideasRoutes = require('./routes/ideasRoutes');

app.use(express.json());
app.use('/ideas', ideasRoutes);

module.exports = app;
