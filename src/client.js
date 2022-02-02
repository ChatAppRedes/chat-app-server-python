const net = require('net');
const readlineSync = require('readline-sync');

const PORT = 3335;

const client = new net.Socket();

client.connect(PORT, 'localhost', () => {
  const username = process.argv[2];
  const jsonMessage = {
    username,
  };
  client.write(JSON.stringify(jsonMessage));
  while (true) {
    const message = readlineSync.question("=> ");
    if (message === 'desconectar') {
      client.write(JSON.stringify({
        username,
        message
      }));
      client.end();
      break;
    }
    client.write(JSON.stringify({
      username,
      message
    }))
  }
});