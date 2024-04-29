// demo of words we can't use. will populate later with real curse words to make it realistic when bot comes on live.
//we can edit later if needed
const curseWords = [
    'stupid',
    'damn',
    'heck',
    // Add more curse words as needed - usually words that don't help with the discussion
];

// Function to analyze text content for inappropriate language
const analyzeContent = (content) => {
    // Convert content to lowercase for case-insensitive comparison
    const lowercaseContent = content.toLowerCase();

    // Check if any curse words are present in the content
    for (const curseWord of curseWords) {
        if (lowercaseContent.includes(curseWord)) {
            return true; // Inappropriate content detected
        }
    }

    return false; // Content is appropriate
};

module.exports = {
    analyzeContent
};
