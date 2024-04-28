const mongoose = require('mongoose');

const ideaSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true
  },
  votes: {
    type: Number,
    default: 0
  }
});

const Idea = mongoose.model('Idea', ideaSchema);

module.exports = Idea;
