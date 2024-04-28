const connectedUsers = new Set();

const addUser = (userId) => {
    connectedUsers.add(userId);
    console.log(`User ${userId} connected.`);
};

const removeUser = (userId) => {
    connectedUsers.delete(userId);
    console.log(`User ${userId} disconnected.`);
};

const getConnectedUsers = () => {
    return Array.from(connectedUsers);
};

module.exports = {
    addUser,
    removeUser,
    getConnectedUsers
};
