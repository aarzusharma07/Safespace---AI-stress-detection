const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mqtt = require('mqtt');

// MQTT broker connection options
const options = {
  host: 'e6c6013aac5e48e3837494ccce82e291.s1.eu.hivemq.cloud',
  port: 8883,
  protocol: 'mqtts',
  username: 'Suyash8874g',
  password: 'Suyash@2404'
};

const topicToSubscribe = 'esp32/health';

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files from 'public' folder
app.use(express.static('public'));

// Redirect root URL to hardware.html
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/hardware.html');
});

// Connect to MQTT broker
const client = mqtt.connect(options);

client.on('connect', () => {
  console.log('✅ Connected to MQTT Broker');
  client.subscribe(topicToSubscribe, (err) => {
    if (err) {
      console.error('❌ Subscription error:', err);
    } else {
      console.log(`📡 Subscribed to topic: ${topicToSubscribe}`);
    }
  });
});

// On MQTT message received, emit to frontend via Socket.IO
client.on('message', (topic, message) => {
  const data = message.toString();
  console.log(`📥 Received on [${topic}]:`, data);
  io.emit('mqtt_message', { topic, message: data });
});

client.on('error', (error) => {
  console.error('❌ Connection error:', error);
});

// Socket.IO connection events
io.on('connection', (socket) => {
  console.log('A client connected');
  socket.on('disconnect', () => {
    console.log('A client disconnected');
  });
});

// Start the server on port 3000
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
