# Jin - Your Slackbot Assistant

Jin is a versatile Slackbot designed to enhance your Slack experience by integrating seamlessly with MongoDB. Jin helps you manage and interact with your data, automate tasks, and streamline your workflow.

- ✅ means features that have been implemented.

### **Basic Commands**
- **`/message-count`**: Lists number of messages sent by user on that specified channel. ✅ 
- **`/previous-messages`**: Lists previous messages sent by user on that specified channel. ✅ 
- **`/help`**: Lists available commands and their descriptions. ✅
- **`/ping`**: Confirms Jin’s activity with a simple acknowledgment. ✅

### **Database Interactions**
- **`/add [item]`**: Adds a new item or record to the MongoDB database.
- **`/list [collection]`**: Lists all items or records from a specified MongoDB collection.
- **`/find [query]`**: Searches the MongoDB database based on a query and returns matching results.

### **Notifications**
- **Scheduled Reminders**: Set reminders for important tasks or deadlines.
- **Daily Summary**: Receive daily or weekly summaries of activities or updates from the database.

### **Custom Responses**
- **Greeting Message**: Jin sends a personalized greeting upon interaction.
- **FAQ Responses**: Provides answers to frequently asked questions using predefined responses stored in MongoDB.

### **Interactive Features**
- **Polls/Surveys**: Create and participate in polls or surveys, with results stored and displayed from MongoDB.
- **Form Submission**: Submit forms through Slack, and have the data saved to MongoDB.

### **Data Insights**
- **Stats Overview**: Get statistics or summaries based on data from MongoDB.
- **Data Visualization**: View basic charts or graphs based on your data.

### **User Management**
- **Profile Information**: View or update your profile information stored in MongoDB.
- **Access Control**: Manage user permissions or roles with information stored in MongoDB.

## **Getting Started**

### **Prerequisites**
- Node.js and npm installed
- Access to a Slack workspace
- MongoDB database

### **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/jin-slackbot.git
   cd jin-slackbot
2. **Install Dependeicies**
    npm install
3. **Set Up Environment Variables**
    Create a .env file in the root directory and add your Slack API token and MongoDB connection string:
    SLACK_API_TOKEN=your-slack-api-token
    MONGODB_URI=your-mongodb-connection-string

4. **Start the Bot**
    - If you want to start server on laptop: npm start
    - If you want to start server remotely, I advise using Replit because it's free and has a clean UI 😊

### **Usage**
- Add Jin to Your Slack Workspace: Follow Slack’s instructions to add a new app to your workspace and configure it with the API token.
- Interact with Jin: Use the commands described in the Features section to interact with Jin and utilize its functionalities.

### **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (git checkout -b feature/your-feature)
3. Make your changes
4. Commit and push (git commit -am 'Add new feature' and git push origin feature/your-feature)
5. Open a pull request

### **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.