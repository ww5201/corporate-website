const express = require("express");
const http = require("http");
const cors = require("cors");
const path = require("path");
const Datastore = require("nedb");
const fs = require("fs");
const multer = require("multer");
const WebSocket = require("ws");

const paymentRouter = require("./routes/payment");
const authRouter = require("./routes/auth");

const app = express();
const server = http.createServer(app);
const PORT = 3000;

// ==================== WebSocket Server ====================
const wss = new WebSocket.Server({ server, path: "/ws/chat" });
const wsClients = new Map(); // convId -> Set<ws>

wss.on("connection", (ws, req) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const convId = url.searchParams.get("convId");
  if (!convId) {
    ws.close(1008, "Missing convId");
    return;
  }

  if (!wsClients.has(convId)) {
    wsClients.set(convId, new Set());
  }
  wsClients.get(convId).add(ws);
  ws.convId = convId;

  ws.on("message", (raw) => {
    try {
      const data = JSON.parse(raw);
      if (data.type === "message") {
        // Save to NeDB then broadcast
        const msg = {
          id: "msg_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6),
          sender: data.sender || "visitor",
          content: data.content,
          type: data.type || "text",
          createdAt: new Date().toISOString(),
        };

        chatDB.update(
          { _id: convId },
          { $push: { messages: msg }, $set: { updatedAt: msg.createdAt } },
          {},
          (err) => {
            if (err) console.error("WS save error:", err);
            // Broadcast to all clients in this conversation
            const clients = wsClients.get(convId) || new Set();
            const payload = JSON.stringify({ type: "new_message", message: msg });
            clients.forEach((c) => {
              if (c.readyState === WebSocket.OPEN) c.send(payload);
            });
          }
        );
      }
    } catch (e) {
      console.error("WS parse error:", e);
    }
  });

  ws.on("close", () => {
    const clients = wsClients.get(convId);
    if (clients) {
      clients.delete(ws);
      if (clients.size === 0) wsClients.delete(convId);
    }
  });
});

// Global broadcast function (used by REST API routes)
global.wsBroadcast = (convId, data) => {
  const clients = wsClients.get(convId) || new Set();
  const payload = JSON.stringify(data);
  clients.forEach((c) => {
    if (c.readyState === WebSocket.OPEN) c.send(payload);
  });
};

// ==================== Data Directory ====================
const d = path.join(__dirname, "data");
if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });

const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

// ==================== NeDB Databases ====================
const pDB = new Datastore({ filename: path.join(d, "products.db"), autoload: true });
const mDB = new Datastore({ filename: path.join(d, "messages.db"), autoload: true });
const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });
const cfgDB = new Datastore({ filename: path.join(d, "config.db"), autoload: true });
const payDB = new Datastore({ filename: path.join(d, "payments.db"), autoload: true });
const userDB = new Datastore({ filename: path.join(d, "users.db"), autoload: true });
const chatDB = new Datastore({ filename: path.join(d, "chat.db"), autoload: true });
const i18nDB = new Datastore({ filename: path.join(d, "i18n.db"), autoload: true });

// Inject databases into app locals for route modules
app.locals.paymentDB = payDB;
app.locals.userDB = userDB;
app.locals.chatDB = chatDB;

// ==================== Middleware ====================
app.use(cors());
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true, limit: "50mb" }));

// Static files - uploads
app.use("/uploads", express.static(uploadDir));

// Static files - frontend SPA
const frontendDir = path.join(__dirname, "frontend");
if (fs.existsSync(frontendDir)) {
  app.use(express.static(frontendDir, {
    setHeaders: (res, filePath) => {
      if (filePath.endsWith('.js')) {
        res.setHeader('Content-Type', 'application/javascript');
      }
    }
  }));
}

// ==================== Admin ====================
app.get("/admin", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));
app.get("/admin.html", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));

// ==================== API Routes ====================
app.use("/api/payment", paymentRouter);
app.use("/api/auth", authRouter);

// ==================== File Upload ====================
app.post("/api/upload-file", (req, res) => {
  try {
    const { path: filePath, content } = req.body;
    if (!filePath || !content) {
      return res.status(400).json({ ok: false, error: "Missing path or content" });
    }
    const decoded = Buffer.from(content, "base64").toString("utf-8");
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, decoded, "utf-8");
    res.json({ ok: true, size: decoded.length });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, Date.now() + "-" + Math.random().toString(36).substr(2, 9) + ext);
  },
});
const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowed = /jpeg|jpg|png|gif|webp/;
    cb(null, allowed.test(path.extname(file.originalname).toLowerCase()) && allowed.test(file.mimetype));
  },
});

app.post("/api/upload", upload.array("images", 6), (req, res) => {
  if (!req.files || !req.files.length) {
    return res.status(400).json({ error: "没有上传文件" });
  }
  res.json({ urls: req.files.map((f) => "/uploads/" + f.filename) });
});

// ==================== Products API ====================
app.get("/api/products", (req, res) => {
  pDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.get("/api/products/:id", (req, res) => {
  pDB.findOne({ _id: req.params.id }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!doc) return res.status(404).json({ error: "not found" });
    res.json(doc);
  });
});

app.post("/api/products", (req, res) => {
  const p = {
    name: req.body.name,
    category: req.body.category || "整体衣柜",
    price: Number(req.body.price) || 0,
    description: req.body.description || "",
    images: req.body.images || [],
    image: (req.body.images && req.body.images[0]) || req.body.image || "",
    createdAt: new Date().toISOString(),
  };
  pDB.insert(p, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.put("/api/products/:id", (req, res) => {
  const u = {
    name: req.body.name,
    category: req.body.category,
    price: Number(req.body.price) || 0,
    description: req.body.description,
    images: req.body.images || [],
    image: (req.body.images && req.body.images[0]) || req.body.image || "",
  };
  pDB.update({ _id: req.params.id }, { $set: u }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.delete("/api/products/:id", (req, res) => {
  pDB.remove({ _id: req.params.id }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// ==================== Messages API (legacy) ====================
app.get("/api/messages", (req, res) => {
  mDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.post("/api/messages", (req, res) => {
  const m = { ...req.body, createdAt: new Date().toISOString() };
  mDB.insert(m, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.delete("/api/messages/:id", (req, res) => {
  mDB.remove({ _id: req.params.id }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// ==================== Conversations API (NeDB) ====================
app.get("/api/conversations", (req, res) => {
  chatDB.find({}).sort({ updatedAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.get("/api/conversations/:id/messages", (req, res) => {
  chatDB.findOne({ _id: req.params.id }, (err, conv) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!conv) return res.status(404).json({ error: "对话不存在" });
    res.json(conv.messages || []);
  });
});

app.post("/api/conversations", (req, res) => {
  const { visitorId, name, phone } = req.body;
  const now = new Date().toISOString();

  // Check if conversation already exists for this visitor
  if (visitorId) {
    chatDB.findOne({ visitorId }, (err, existing) => {
      if (!err && existing) return res.json(existing);

      chatDB.insert({
        visitorId: visitorId || "visitor_" + Date.now(),
        name: name || "访客",
        phone: phone || "",
        messages: [],
        unread: 0,
        createdAt: now,
        updatedAt: now,
      }, (err, doc) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(doc);
      });
    });
  } else {
    chatDB.insert({
      visitorId: "visitor_" + Date.now(),
      name: name || "访客",
      phone: phone || "",
      messages: [],
      unread: 0,
      createdAt: now,
      updatedAt: now,
    }, (err, doc) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json(doc);
    });
  }
});

app.post("/api/conversations/:id/messages", (req, res) => {
  const convId = req.params.id;
  const { sender, content, type } = req.body;
  if (!content) return res.status(400).json({ error: "消息内容不能为空" });

  const msg = {
    id: "msg_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6),
    sender: sender || "visitor",
    content,
    type: type || "text",
    createdAt: new Date().toISOString(),
  };

  chatDB.update(
    { _id: convId },
    { $push: { messages: msg }, $set: { updatedAt: msg.createdAt, unread: sender === "visitor" ? 1 : 0 } },
    {},
    (err) => {
      if (err) return res.status(500).json({ error: err.message });

      // Broadcast via WebSocket
      global.wsBroadcast(convId, { type: "new_message", message: msg });
      res.json(msg);
    }
  );
});

app.put("/api/conversations/:id/read", (req, res) => {
  chatDB.update({ _id: req.params.id }, { $set: { unread: 0 } }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.delete("/api/conversations/:id", (req, res) => {
  chatDB.remove({ _id: req.params.id }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.get("/api/conversations/:id/poll", (req, res) => {
  const convId = req.params.id;
  const since = req.query.since || "";
  chatDB.findOne({ _id: convId }, (err, conv) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!conv) return res.status(404).json({ error: "对话不存在" });
    const msgs = (conv.messages || []).filter((m) => m.createdAt > since);
    res.json({ messages: msgs, updatedAt: conv.updatedAt });
  });
});

// ==================== Orders API ====================
app.get("/api/orders", (req, res) => {
  oDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.post("/api/orders", (req, res) => {
  const o = { ...req.body, status: "新咨询", createdAt: new Date().toISOString() };
  oDB.insert(o, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.put("/api/orders/:id", (req, res) => {
  oDB.update({ _id: req.params.id }, { $set: req.body }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// ==================== Payment Config API ====================
app.get("/api/payment-config", (req, res) => {
  cfgDB.findOne({ type: "payment" }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc || { type: "payment", wechatQr: "", alipayQr: "", bankInfo: "" });
  });
});

app.post("/api/payment-config", (req, res) => {
  const data = {
    type: "payment",
    wechatQr: req.body.wechatQr || "",
    alipayQr: req.body.alipayQr || "",
    bankInfo: req.body.bankInfo || "",
    updatedAt: new Date().toISOString(),
  };
  cfgDB.update({ type: "payment" }, { $set: data }, { upsert: true }, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true, ...data });
  });
});

app.put("/api/orders/:id/pay", (req, res) => {
  oDB.update({ _id: req.params.id }, { $set: { status: "已付款", paidAt: new Date().toISOString() } }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// ==================== i18n API ====================
app.get("/api/i18n/:lang", (req, res) => {
  i18nDB.findOne({ lang: req.params.lang }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc || { lang: req.params.lang, translations: {} });
  });
});

app.post("/api/i18n/:lang", (req, res) => {
  const lang = req.params.lang;
  const data = { lang, translations: req.body.translations || {}, updatedAt: new Date().toISOString() };
  i18nDB.update({ lang }, { $set: data }, { upsert: true }, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.get("/api/i18n", (req, res) => {
  i18nDB.find({}, (err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs.map((d) => ({ lang: d.lang, updatedAt: d.updatedAt })));
  });
});

// ==================== SMS Config API ====================
app.get("/api/sms-config", (req, res) => {
  try {
    const smsService = require("./sms-service");
    res.json({
      signName: smsService.SMS_CONFIG.signName,
      templateCode: smsService.SMS_CONFIG.templateCode,
      configured: !!(smsService.SMS_CONFIG.accessKeyId && smsService.SMS_CONFIG.accessKeySecret && smsService.SMS_CONFIG.templateCode),
    });
  } catch {
    res.json({ configured: false });
  }
});

app.post("/api/sms-config", (req, res) => {
  try {
    const smsService = require("./sms-service");
    const { accessKeyId, accessKeySecret, signName, templateCode } = req.body;
    smsService.setConfig({
      accessKeyId: accessKeyId || smsService.SMS_CONFIG.accessKeyId,
      accessKeySecret: accessKeySecret || smsService.SMS_CONFIG.accessKeySecret,
      signName: signName || smsService.SMS_CONFIG.signName,
      templateCode: templateCode || smsService.SMS_CONFIG.templateCode,
    });
    res.json({ ok: true, configured: true });
  } catch {
    res.status(500).json({ error: "SMS service not available" });
  }
});

// ==================== Health Check ====================
app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date().toISOString() }));

// ==================== SPA Catch-all ====================
// All non-API, non-admin, non-upload routes serve the SPA index.html
app.use((req, res, next) => {
  if (req.method === 'GET' && !req.path.startsWith('/api/') && !req.path.startsWith('/uploads/') && !req.path.startsWith('/ws/')) {
    const indexPath = path.join(frontendDir, "index.html");
    if (fs.existsSync(indexPath)) {
      return res.sendFile(indexPath);
    }
  }
  next();
});

// ==================== Start Server ====================
server.listen(PORT, () => {
  console.log("Server running on port " + PORT);
  console.log("Admin: http://localhost:" + PORT + "/admin");
  console.log("SPA: http://localhost:" + PORT + "/");
  console.log("WebSocket: ws://localhost:" + PORT + "/ws/chat");
});
