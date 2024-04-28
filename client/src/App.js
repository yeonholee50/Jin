import React, { useState, useEffect } from 'react';
import axios from 'axios';
import IdeaList from './components/IdeaList';

const App = () => {
  const [ideas, setIdeas] = useState([]);
  const [text, setText] = useState('');

  useEffect(() => {
    fetchIdeas();
  }, []);

  const fetchIdeas = async () => {
    try {
      const response = await axios.get('/ideas');
      setIdeas(response.data);
    } catch (err) {
      console.error('Error fetching ideas:', err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/ideas', { text });
      fetchIdeas();
      setText('');
    } catch (err) {
      console.error('Error creating idea:', err.message);
    }
  };

  return (
    <div>
      <h1>Brainstorm Buddy</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your idea..."
        />
        <button type="submit">Submit</button>
      </form>
      <IdeaList ideas={ideas} />
    </div>
  );
};

export default App;
