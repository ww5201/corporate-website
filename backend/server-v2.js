const express = require("express");
const cors = require("cors");
const path = require("path");
const Datastore = require("nedb");
const fs = require("fs");
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const d = path.join(__dirname, "data");
if (!fs.existsSync(d)) fs.mkdirSync(d);

const pDB = new Datastore({ filename: path.join(d, "products.db"), autoload: true });
const mDB = new Datastore({ filename: path.join(d, "messages.db"), autoload: true });
const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });

// API: 产品
app.get("/api/products", (req, res) => { pDB.find({}, (e, r) => res.json(r || [])); });
app.post("/api/products", (req, res) => { pDB.insert({...req.body, createdAt: new Date()}, (e, r) => res.json(r)); });
app.put("/api/products/:id", (req, res) => { pDB.update({_id: req.params.id}, {$set: req.body}, {}, (e, r) => res.json({ok:1})); });
app.delete("/api/products/:id", (req, res) => { pDB.remove({_id: req.params.id}, {}, (e, r) => res.json({ok:1})); });

// API: 留言
app.get("/api/messages", (req, res) => { mDB.find({}).sort({createdAt:-1}).exec((e, r) => res.json(r || [])); });
app.post("/api/messages", (req, res) => { mDB.insert({...req.body, createdAt: new Date(), read: false}, (e, r) => res.json(r)); });
app.put("/api/messages/:id", (req, res) => { mDB.update({_id: req.params.id}, {$set: req.body}, {}, (e, r) => res.json({ok:1})); });
app.delete("/api/messages/:id", (req, res) => { mDB.remove({_id: req.params.id}, {}, (e, r) => res.json({ok:1})); });

// API: 订单
app.get("/api/orders", (req, res) => { oDB.find({}).sort({createdAt:-1}).exec((e, r) => res.json(r || [])); });
app.post("/api/orders", (req, res) => { oDB.insert({...req.body, createdAt: new Date(), status: "pending"}, (e, r) => res.json(r)); });
app.put("/api/orders/:id", (req, res) => { oDB.update({_id: req.params.id}, {$set: req.body}, {}, (e, r) => res.json({ok:1})); });
app.delete("/api/orders/:id", (req, res) => { oDB.remove({_id: req.params.id}, {}, (e, r) => res.json({ok:1})); });

// 健康检查
app.get("/api/health", (req, res) => res.json({status: "ok"}));

// 管理后台
app.get("/admin.html", (req, res) => { res.sendFile(path.join(__dirname, "admin.html")); });
app.get("/admin", (req, res) => { res.sendFile(path.join(__dirname, "admin.html")); });

app.listen(PORT, "0.0.0.0", () => console.log("Server running on port " + PORT));
