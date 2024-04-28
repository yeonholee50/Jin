const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/sentiment', async (req, res) => {
  try {
    const { text } = req.body;
    const pythonProcess = spawn('python', ['scripts/sentiment_analysis.py', text]);
    pythonProcess.stdout.on('data', (data) => {
      const sentiment = data.toString().trim();
      res.json({ sentiment });
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
