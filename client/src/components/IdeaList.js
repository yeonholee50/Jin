import React from 'react';
import IdeaItem from './IdeaItem';

const IdeaList = ({ ideas }) => {
  return (
    <div>
      <h2>Ideas</h2>
      <ul>
        {ideas.map(idea => (
          <IdeaItem key={idea._id} idea={idea} />
        ))}
      </ul>
    </div>
  );
};

export default IdeaList;
