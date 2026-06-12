const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const url = require('url');

require('dotenv').config();

const app = express();
const server = http.createServer(app);

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件 - 前端
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// 连接 MongoDB
const mongoUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/luxury-co';
mongoose.connect(mongoUri)
  .then(() => console.log('✅ MongoDB 连接成功'))
  .catch(err => console.error('❌ MongoDB 连接失败:', err));

// ==================== API 路由 ====================
app.use('/api/products', require('./routes/products'));
app.use('/api/orders', require('./routes/orders'));
app.use('/api/messages', require('./routes/messages'));
app.use('/api/auth', require('./routes/auth'));
app.use('/api/payment', require('./routes/payment'));
app.use('/api/conversations', require('./routes/conversations'));

// 根路由
app.get('/api', (req, res) => {
  res.json({
    message: '卓翌定制 - API 服务',
    version: '2.0.0',
    endpoints: {
      products: '/api/products',
      orders: '/api/orders',
      messages: '/api/messages',
      auth: '/api/auth',
      payment: '/api/payment',
      conversations: '/api/conversations',
    },
  });
});

// SPA 回退 - 所有非 API 路由返回 index.html
app.get('/{*splat}', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

// ==================== WebSocket 聊天 ====================
const wss = new WebSocket.Server({ server, path: '/ws/chat' });

// 存储已连接的客户端
const wsClients = new Map(); // convId -> Set<ws>

wss.on('connection', (ws, req) => {
  const query = url.parse(req.url, true).query;
  const convId = query.convId;

  if (!convId) {
    ws.close(4000, 'Missing convId');
    return;
  }

  // 加入对话房间
  if (!wsClients.has(convId)) {
    wsClients.set(convId, new Set());
  }
  wsClients.get(convId).add(ws);

  ws.send(JSON.stringify({
    type: 'connected',
    convId,
    message: '已连接到客服',
  }));

  ws.on('message', async (data) => {
    try {
      const msg = JSON.parse(data);

      if (msg.type === 'message') {
        const Conversation = require('./models/Conversation');
        const conv = await Conversation.findById(msg.convId || convId);
        if (conv) {
          conv.messages.push({
            sender: msg.sender || 'visitor',
            content: msg.content,
            type: msg.type || 'text',
          });
          await conv.save();

          const savedMsg = conv.messages[conv.messages.length - 1];

          // 广播给同一对话的所有客户端
          broadcastToConv(convId, {
            type: 'new_message',
            message: savedMsg,
          });
        }
      }
    } catch (err) {
      console.error('WS message error:', err);
    }
  });

  ws.on('close', () => {
    const clients = wsClients.get(convId);
    if (clients) {
      clients.delete(ws);
      if (clients.size === 0) {
        wsClients.delete(convId);
      }
    }
  });

  ws.on('error', (err) => {
    console.error('WS error:', err);
  });
});

// 广播消息到对话的所有连接
function broadcastToConv(convId, data) {
  const clients = wsClients.get(convId);
  if (clients) {
    const msg = JSON.stringify(data);
    clients.forEach(ws => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(msg);
      }
    });
  }
}

// 注册全局广播函数 (供 REST API 使用)
global.wsBroadcast = broadcastToConv;

// ==================== 启动服务器 ====================
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`\n🚀 卓翌定制服务器已启动`);
  console.log(`   HTTP:  http://localhost:${PORT}`);
  console.log(`   WS:    ws://localhost:${PORT}/ws/chat`);
  console.log(`   API:   http://localhost:${PORT}/api\n`);
});
