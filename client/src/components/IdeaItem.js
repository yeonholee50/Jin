import React from 'react';

const IdeaItem = ({ idea }) => {
  const handleVote = async () => {
    try {
      await axios.put(`/ideas/${idea._id}/vote`);
      fetchIdeas();
    } catch (err) {
      console.error('Error voting for idea:', err.message);
    }
  };

  return (
    <li>
      <span>{idea.text}</span>
      <button onClick={handleVote}>Vote ({idea.votes})</button>
    </li>
  );
};

export default IdeaItem;
