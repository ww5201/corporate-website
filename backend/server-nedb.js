const express = require('express');
const cors = require('cors');
const path = require('path');
const Datastore = require('nedb');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const dataDir = path.join(__dirname, 'data');
const fs = require('fs');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir);

const productsDB = new Datastore({ filename: path.join(dataDir, 'products.db'), autoload: true });
const messagesDB = new Datastore({ filename: path.join(dataDir, 'messages.db'), autoload: true });
const ordersDB = new Datastore({ filename: path.join(dataDir, 'orders.db'), autoload: true });

// 产品
app.get('/api/products', (req, res) => {
  productsDB.find({}, (err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});
app.post('/api/products', (req, res) => {
  productsDB.insert({ ...req.body, createdAt: new Date() }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});
app.delete('/api/products/:id', (req, res) => {
  productsDB.remove({ _id: req.params.id }, {}, (err, n) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ success: true });
  });
});

// 留言
app.get('/api/messages', (req, res) => {
  messagesDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});
app.post('/api/messages', (req, res) => {
  messagesDB.insert({ ...req.body, createdAt: new Date(), read: false }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});
app.delete('/api/messages/:id', (req, res) => {
  messagesDB.remove({ _id: req.params.id }, {}, (err, n) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ success: true });
  });
});

// 订单
app.get('/api/orders', (req, res) => {
  ordersDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});
app.post('/api/orders', (req, res) => {
  ordersDB.insert({ ...req.body, createdAt: new Date(), status: 'pending' }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

app.listen(PORT, '0.0.0.0', () => console.log('Server running on port ' + PORT));
