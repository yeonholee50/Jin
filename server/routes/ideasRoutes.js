const express = require('express');
const router = express.Router();
const ideasController = require('../controllers/ideasController');

// Get all ideas
router.get('/', ideasController.getAllIdeas);

// Create a new idea
router.post('/', ideasController.createIdea);

// Vote for an idea
router.put('/:id/vote', ideasController.voteForIdea);

module.exports = router;
