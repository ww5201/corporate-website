/**
 * 卓翌定制 - 后端服务 v5
 * 新增: WebSocket 实时聊天 + SPA 静态文件服务
 */
const express = require("express");
const cors = require("cors");
const path = require("path");
const Datastore = require("nedb");
const fs = require("fs");
const http = require("http");
const { WebSocketServer } = require("ws");
const multer = require("multer");
const paymentRouter = require("./routes/payment");
const authRouter = require("./routes/auth");

const app = express();
const PORT = process.env.PORT || 3000;

// ============ 数据目录 ============
const d = path.join(__dirname, "data");
if (!fs.existsSync(d)) fs.mkdirSync(d);

const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);

// ============ 数据库 ============
const pDB = new Datastore({ filename: path.join(d, "products.db"), autoload: true });
const mDB = new Datastore({ filename: path.join(d, "messages.db"), autoload: true });
const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });
const cfgDB = new Datastore({ filename: path.join(d, "config.db"), autoload: true });
const payDB = new Datastore({ filename: path.join(d, "payments.db"), autoload: true });
const userDB = new Datastore({ filename: path.join(d, "users.db"), autoload: true });
const chatDB = new Datastore({ filename: path.join(d, "chat.db"), autoload: true });

app.locals.paymentDB = payDB;
app.locals.userDB = userDB;

// ============ 中间件 ============
app.use(cors());
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true, limit: "50mb" }));

// ============ SPA 静态文件 ============
const frontendDir = path.join(__dirname, "..", "frontend");
app.use(express.static(frontendDir));

// 图片上传
app.use("/uploads", express.static(uploadDir));

// multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, Date.now() + "-" + Math.random().toString(36).substr(2, 9) + ext);
  }
});
const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowed = /jpeg|jpg|png|gif|webp/;
    cb(null, allowed.test(path.extname(file.originalname).toLowerCase()) && allowed.test(file.mimetype));
  }
});

// ============ 管理后台（保留旧路由） ============
app.get("/admin", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));
app.get("/admin.html", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));

// ============ API 路由 ============
app.use("/api/payment", paymentRouter);
app.use("/payment", paymentRouter);
app.use("/api/auth", authRouter);

// 图片上传
app.post("/api/upload", upload.array("images", 6), (req, res) => {
  if (!req.files || !req.files.length) return res.status(400).json({ error: "没有上传文件" });
  res.json({ urls: req.files.map(f => "/uploads/" + f.filename) });
});

// 产品 API
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
    createdAt: new Date().toISOString()
  };
  pDB.insert(p, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.put("/api/products/:id", (req, res) => {
  const u = {
    name: req.body.name, category: req.body.category,
    price: Number(req.body.price) || 0, description: req.body.description,
    images: req.body.images || [],
    image: (req.body.images && req.body.images[0]) || req.body.image || ""
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

// 留言 API
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

// ============ 对话聊天 API ============
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
  const conv = {
    visitorId: visitorId || "visitor_" + Date.now(),
    name: name || "访客",
    phone: phone || "",
    messages: [],
    unread: 0,
    createdAt: now,
    updatedAt: now
  };
  chatDB.insert(conv, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc);
  });
});

app.post("/api/conversations/:id/messages", (req, res) => {
  const { sender, content, type } = req.body;
  if (!content) return res.status(400).json({ error: "消息内容不能为空" });

  const msg = {
    id: "msg_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6),
    sender: sender || "visitor",
    content,
    type: type || "text",
    createdAt: new Date().toISOString()
  };

  chatDB.update(
    { _id: req.params.id },
    { $push: { messages: msg }, $set: { updatedAt: msg.createdAt, unread: sender === "visitor" ? 1 : 0 } },
    {},
    (err) => {
      if (err) return res.status(500).json({ error: err.message });
      // 通过 WebSocket 广播
      broadcastToConv(req.params.id, { type: "new_message", message: msg });
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

app.get("/api/conversations/:id/poll", (req, res) => {
  const since = req.query.since || "";
  chatDB.findOne({ _id: req.params.id }, (err, conv) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!conv) return res.status(404).json({ error: "对话不存在" });
    res.json({ messages: (conv.messages || []).filter(m => m.createdAt > since), updatedAt: conv.updatedAt });
  });
});

// ============ 订单 API ============
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

app.put("/api/orders/:id/pay", (req, res) => {
  oDB.update({ _id: req.params.id }, { $set: { status: "已付款", paidAt: new Date().toISOString() } }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// ============ 配置 API ============
app.get("/api/payment-config", (req, res) => {
  cfgDB.findOne({ type: "payment" }, (err, doc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(doc || { type: "payment", wechatQr: "", alipayQr: "", bankInfo: "" });
  });
});

app.post("/api/payment-config", (req, res) => {
  const data = { type: "payment", ...req.body, updatedAt: new Date().toISOString() };
  cfgDB.update({ type: "payment" }, { $set: data }, { upsert: true }, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true, ...data });
  });
});

// 健康检查
app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date().toISOString() }));

// ============ SPA 回退路由 ============
// 使用中间件处理 SPA 回退（Express 5 不支持 * 通配符）
app.use((req, res, next) => {
  // 只处理 GET 请求，排除 API 和静态资源
  if (req.method !== "GET") return next();
  if (req.path.startsWith("/api") || req.path.startsWith("/admin") || req.path.startsWith("/uploads")) return next();
  if (req.path.includes(".")) return next(); // 有扩展名的请求跳过（静态文件）
  res.sendFile(path.join(frontendDir, "index.html"));
});

// ============ HTTP + WebSocket 服务器 ============
const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: "/ws/chat" });

// WebSocket 连接管理: convId -> Set<ws>
const convClients = new Map();

wss.on("connection", (ws, req) => {
  const url = new URL(req.url, "http://localhost");
  const convId = url.searchParams.get("convId");

  if (!convId) {
    ws.close(1008, "Missing convId");
    return;
  }

  // 加入对话房间
  if (!convClients.has(convId)) {
    convClients.set(convId, new Set());
  }
  convClients.get(convId).add(ws);

  console.log(`[WS] Client connected to conv ${convId} (total: ${convClients.get(convId).size})`);

  ws.on("message", async (data) => {
    try {
      const msg = JSON.parse(data);

      if (msg.type === "message" && msg.content) {
        // 保存消息到数据库
        const chatMsg = {
          id: "msg_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6),
          sender: msg.sender || "visitor",
          content: msg.content,
          type: msg.type || "text",
          createdAt: new Date().toISOString()
        };

        chatDB.update(
          { _id: convId },
          { $push: { messages: chatMsg }, $set: { updatedAt: chatMsg.createdAt, unread: 1 } },
          {},
          (err) => {
            if (err) {
              console.error("[WS] DB error:", err);
              return;
            }
            // 广播给所有连接到此对话的客户端
            broadcastToConv(convId, { type: "new_message", message: chatMsg });
          }
        );
      }
    } catch (e) {
      console.error("[WS] Message error:", e);
    }
  });

  ws.on("close", () => {
    const clients = convClients.get(convId);
    if (clients) {
      clients.delete(ws);
      if (clients.size === 0) convClients.delete(convId);
    }
    console.log(`[WS] Client disconnected from conv ${convId}`);
  });

  ws.on("error", (err) => {
    console.error("[WS] Error:", err.message);
  });
});

function broadcastToConv(convId, data) {
  const clients = convClients.get(convId);
  if (!clients) return;
  const payload = JSON.stringify(data);
  clients.forEach(ws => {
    if (ws.readyState === 1) { // WebSocket.OPEN
      ws.send(payload);
    }
  });
}

// ============ 启动 ============
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Admin: http://localhost:${PORT}/admin.html`);
  console.log(`Frontend: http://localhost:${PORT}/`);
  console.log(`WebSocket: ws://localhost:${PORT}/ws/chat`);
});
