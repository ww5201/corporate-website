import paramiko

# ===== 修改后端 server-v4.js =====
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 读取后端文件
stdin, stdout, stderr = ssh.exec_command("cat /root/backend/server-v4.js")
server = stdout.read().decode('utf-8')

# 添加案例数据库
server = server.replace(
    'const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });',
    'const oDB = new Datastore({ filename: path.join(d, "orders.db"), autoload: true });\nconst cDB = new Datastore({ filename: path.join(d, "cases.db"), autoload: true });'
)

# 添加案例上传路由 (20 张图)
upload_code = '''app.post("/api/upload", upload.array("images", 20), (req, res) => {
  const urls = req.files.map(f => `/uploads/${f.filename}`);
  res.json({ urls });
});'''

new_upload = '''// 案例上传
app.post("/api/cases/upload", upload.array("images", 20), (req, res) => {
  const urls = req.files.map(f => `/uploads/${f.filename}`);
  res.json({ urls });
});'''

server = server.replace(upload_code, new_upload)

# 添加案例 API
cases_api = '''
// ===== 案例 API =====
app.get("/api/cases", (req, res) => {
  cDB.find({}).sort({ createdAt: -1 }).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(docs);
  });
});

app.post("/api/cases", (req, res) => {
  const { name, description, images } = req.body;
  const doc = { name, description, images, createdAt: new Date() };
  cDB.insert(doc, (err, newDoc) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(newDoc);
  });
});

app.delete("/api/cases/:id", (req, res) => {
  cDB.remove({ _id: req.params.id }, {}, (err, num) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ deleted: num });
  });
});
'''

# 在健康检查后添加案例 API
server = server.replace(
    'app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date().toISOString() }));',
    'app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date().toISOString() }));' + cases_api
)

# 保存回服务器
sftp = ssh.open_sftp()
sftp.put('/tmp/server-new.js', '/root/backend/server-v4.js')
sftp.close()

ssh.close()
print("Backend updated")
