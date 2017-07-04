const http = require("http");
const app = require("./app");

const debug = require('debug')('express:server');
const PORT = 3000;

app.set('port', PORT);

const server = http.createServer(app);

server.listen(PORT);
server.on('error', (err) => debug(err));
server.on('listening', () => debug(`Listening on localhost:${PORT}`));
