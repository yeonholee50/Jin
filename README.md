# Brainstorm Buddy: The Innovative Slack Bot for Idea Generation

Brainstorm Buddy is a Slack bot designed to facilitate brainstorming sessions and inspire creativity within teams.

## Features

- **Idea Generation:** The bot actively monitors Slack channels for potential brainstorming sessions and provides prompts or guiding questions to spark creativity.
- **Prompt Suggestions:** Based on the context of the conversation, the bot suggests relevant prompts or challenges to inspire idea generation.
- **Idea Tracking:** Team members can submit their ideas directly to the bot within Slack channels, which organizes and catalogs them for further discussion.
- **Voting and Ranking:** The bot facilitates voting and ranking of ideas, streamlining the decision-making process for teams.
- **Integration with External Tools:** Brainstorm Buddy integrates with external tools such as Trello and Google Docs for seamless collaboration and project management.

## Technical Implementation

- **Slack API:** The bot interacts with the Slack API to listen for messages, respond to user requests, and post updates within Slack channels.
- **NLP and ML:** Brainstorm Buddy uses natural language processing (NLP) and machine learning (ML) techniques to analyze message content, identify keywords, and generate prompts or suggestions.
- **Database:** Ideas submitted by users are stored and managed in a database (e.g., MongoDB) to maintain a centralized repository for brainstorming sessions.
- **Integration:** The bot integrates with external tools and services commonly used for project management or idea development, enhancing collaboration and productivity.

## Getting Started

1. Clone the repository:
   git clone https://github.com/yeonholee50/SlackBot.git
2. Install dependencies:
    cd brainstorm-buddy
    npm install
3. Set up environment variables:
    Create a .env file in the root directory.
    Define environment variables such as Slack API token, database connection string, etc.
4. Start the bot:
    npm start
5. Invite the bot to your Slack workspace and add it to channels where you want it to participate in brainstorming sessions.

## Usage

- Connect to the server using WebSocket at `ws://localhost:3000/ws?userId=<userId>`.
- Use the provided WebSocket API to authenticate, send rich text formatting changes, and user cursor positions.
- Use the provided REST API endpoints for managing posts, comments, and likes.

## API Endpoints

- `POST /posts`: Create a new post.
- `GET /posts`: Get all posts.
- `POST /comments`: Create a new comment for a post.
- `POST /posts/:postId/like`: Like a post.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any enhancements or bug fixes.
