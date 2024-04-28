// server/controllers/text_document.js

let sharedDocument = '';

const getSharedDocument = () => {
    return sharedDocument;
};

const updateSharedDocument = (newContent) => {
    sharedDocument = newContent;
};

module.exports = {
    getSharedDocument,
    updateSharedDocument
};
