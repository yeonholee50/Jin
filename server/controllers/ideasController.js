const Idea = require('../models/Idea');

// Get all ideas
exports.getAllIdeas = async (req, res) => {
  try {
    const ideas = await Idea.find();
    res.json(ideas);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// Create a new idea
exports.createIdea = async (req, res) => {
  const idea = new Idea({
    text: req.body.text
  });
  try {
    const newIdea = await idea.save();
    res.status(201).json(newIdea);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

// Vote for an idea
exports.voteForIdea = async (req, res) => {
  try {
    const idea = await Idea.findById(req.params.id);
    idea.votes++;
    const updatedIdea = await idea.save();
    res.json(updatedIdea);
  } catch (err) {
    res.status(404).json({ message: 'Idea not found' });
  }
};
