const express = require('express');
const cors = require('cors');    
const { Kafka } = require('kafkajs');
const WebSocket = require('ws');

const app = express();
app.use(cors());                         
app.use(express.json());

const kafka = new Kafka({
brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],});
const consumer = kafka.consumer({ groupId: 'api-group' });
const history = [];

app.get('/history', (req, res) => {
  const limit = parseInt(req.query.limit) || 50;
  res.json(history.slice(-limit));
});

const server = app.listen(3000, () => {
  console.log('API listening on port 3000');
});

const wss = new WebSocket.Server({ server, path: '/ws' });

wss.on('connection', ws => {
  console.log('WS client connected');
});

async function run() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'raw-sensor-data', fromBeginning: true });
  await consumer.run({
    eachMessage: async ({ message }) => {
      const data = JSON.parse(message.value.toString());
      const entry = { time: new Date().toISOString(), payload: data };
      history.push(entry);
      if (history.length > 500) history.shift();
      wss.clients.forEach(c => c.readyState === WebSocket.OPEN && c.send(JSON.stringify(data)));
    },
  });
}

run().catch(console.error);

