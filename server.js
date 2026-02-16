// server.js
const http = require('http');

// Create server
const server = http.createServer((req, res) => {
    res.statusCode = 200; // HTTP OK
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello, Node.js Server!\n');
});

// Choose a port
const PORT = 3000;

// Start server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});