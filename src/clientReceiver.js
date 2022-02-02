const net = require('net');

const PORT = 3335;

const client = new net.Socket();

client.connect(PORT, 'localhost', () => {
  const jsonMessage = {
    receiver: true,
  };
  client.write(JSON.stringify(jsonMessage));
});

client.on('data', data => {
  console.log(data?.toString());
})