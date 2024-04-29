const { User } = require('../models');
const { analyzeContent } = require('../utils/text_classification');

const contentModerationMiddleware = async (req, res, next) => {
    try {
        // Analyze post/comment content for inappropriate content
        const { content } = req.body;
        const isContentAppropriate = await analyzeContent(content);

        if (!isContentAppropriate) {
            // Content is inappropriate, handle moderation
            // For now, we'll just log the occurrence
            console.log(`Inappropriate content detected: ${content}`);
            // We can add further actions here like hiding the content, notifying moderators, etc.
        }

        // Proceed to next middleware
        next();
    } catch (error) {
        console.error('Error moderating content:', error);
        res.status(500).json({ error: 'Content moderation error' });
    }
};

module.exports = contentModerationMiddleware;
