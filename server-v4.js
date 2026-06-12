const express = require("express");
const cors = require("cors");
const path = require("path");
const Datastore = require("nedb");
const fs = require("fs");
const multer = require("multer");

const app = express();
const PORT = 3000;

// 数据目录
const d = path.join(__dirname, "data");
if (!fs.existsSync(d)) fs.mkdirSync(d);

// 上传目录
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);

// 数据库
const pDB = new Datastore({ filename: path.join(d, "products.db"), autoload: true });
const mDB = new Datastore({ filename: path.join(d, "messages.db"), autoload: true });
const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });
const cDB = new Datastore({ filename: path.join(d, "cases.db"), autoload: true });
const cfgDB = new Datastore({ filename: path.join(d, "config.db"), autoload: true });

// 中间件
app.use(cors());
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true, limit: "50mb" }));

// 静态文件 - 图片
app.use("/uploads", express.static(uploadDir));

// multer 配置
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    const name = Date.now() + "-" + Math.random().toString(36).substr(2, 9) + ext;
    cb(null, name);
  }
});
const upload = multer({ 
  storage,
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowed = /jpeg|jpg|png|gif|webp/;
    const ext = allowed.test(path.extname(file.originalname).toLowerCase());
    const mime = allowed.test(file.mimetype);
    cb(null, ext && mime);
  }
});

// 管理后台
app.get("/admin", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));
app.get("/admin.html", (req, res) => res.sendFile(path.join(__dirname, "admin.html")));

// ===== 图片上传 =====
app.post("/api/upload", upload.array("images", 20), (req, res) => {
  if (!req.files || !req.files.length) {
    return res.status(400).json({ error: "没有上传文件" });
  }
  const urls = req.files.map(f => "/uploads/" + f.filename);
  res.json({ urls });
});

// ===== 产品 API =====
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
    name: req.body.name,
    category: req.body.category,
    price: Number(req.body.price) || 0,
    description: req.body.description,
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

// ===== 留言 API =====
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

// ===== 订单 API =====
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

// ===== 支付配置 API =====
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
    updatedAt: new Date().toISOString()
  };
  cfgDB.update({ type: "payment" }, { $set: data }, { upsert: true }, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true, ...data });
  });
});

// ===== 订单状态更新 =====
app.put("/api/orders/:id/pay", (req, res) => {
  oDB.update({ _id: req.params.id }, { $set: { status: "已付款", paidAt: new Date().toISOString() } }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// 健康检查
app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date().toISOString() }));

// ===== 案例 API =====
app.get("/api/cases", (req, res) => {
  cDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.post("/api/cases", (req, res) => {
  const doc = { ...req.body, createdAt: new Date().toISOString() };
  cDB.insert(doc, (err, newDoc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(newDoc);
  });
});

app.put("/api/cases/:id", (req, res) => {
  cDB.update({ _id: req.params.id }, { $set: req.body }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.delete("/api/cases/:id", (req, res) => {
  cDB.remove({ _id: req.params.id }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

// 启动
app.listen(PORT, () => {
  console.log("Server running on port " + PORT);
  console.log("Admin: http://localhost:" + PORT + "/admin.html");
});
