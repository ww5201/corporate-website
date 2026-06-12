# 手机监控后端服务

一个简单的 Node.js 后端服务，用于接收和存储 Android 手机监控数据。

## 功能特性

- 📱 接收手机电池信息
- 📊 接收运行中应用列表
- 🔔 接收通知信息
- 📈 数据统计和历史记录
- 🌐 CORS 支持（跨域请求）

## 快速开始

### 1. 安装依赖

```bash
cd backend
npm install
```

### 2. 启动服务

```bash
# 开发模式（自动重启）
npm run dev

# 生产模式
npm start
```

### 3. 服务地址

服务器默认运行在 `http://localhost:8080`

## API 接口

### 健康检查

```
GET /api/health
```

响应：
```json
{
  "success": true,
  "message": "服务器运行正常",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 123.456
}
```

### 上传监控数据

```
POST /api/monitor/data
Content-Type: application/json

{
  "deviceId": "设备唯一ID",
  "deviceModel": "Samsung Galaxy S21",
  "androidVersion": "Android 12 (API 31)",
  "battery": {
    "level": 85,
    "statusText": "充电中",
    "temperature": 25.5,
    "voltage": 4200,
    "technology": "Li-ion"
  },
  "runningApps": [
    {
      "packageName": "com.example.app",
      "appName": "示例应用",
      "memoryUsage": 12345
    }
  ],
  "notifications": [
    {
      "packageName": "com.example.app",
      "title": "新消息",
      "text": "你有一条新消息"
    }
  ],
  "installedApps": []
}
```

响应：
```json
{
  "success": true,
  "message": "数据接收成功",
  "data": {
    "recordId": 1,
    "deviceCount": 1
  }
}
```

### 获取设备列表

```
GET /api/devices
```

### 获取设备详情

```
GET /api/devices/:deviceId/latest
```

### 获取设备历史数据

```
GET /api/devices/:deviceId/history?limit=50
```

### 获取统计数据

```
GET /api/stats
```

## Android 配置

在 Android 应用中，将服务器地址配置为：

```
http://你的服务器IP:8080/
```

**注意：**
- 本地开发时使用 `http://10.0.2.2:8080/`（模拟器）
- 真机测试需要使用电脑的实际 IP 地址
- 确保手机和电脑在同一网络下

## 部署建议

### 使用 PM2 部署

```bash
npm install -g pm2
pm2 start server.js --name phone-monitor
pm2 save
pm2 startup
```

### Docker 部署

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 8080
CMD ["node", "server.js"]
```

```bash
docker build -t phone-monitor-backend .
docker run -p 8080:8080 phone-monitor-backend
```

## 扩展功能

可以添加的功能：
- MongoDB 持久化存储
- WebSocket 实时推送
- 用户认证
- 数据可视化仪表板
- 告警通知（邮件/Webhook）
