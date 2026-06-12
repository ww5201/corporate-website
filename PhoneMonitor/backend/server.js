const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 8080;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 连接 MongoDB（可选）
// mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/phone_monitor')
//   .then(() => console.log('MongoDB 连接成功'))
//   .catch(err => console.log('MongoDB 连接失败:', err));

// 内存存储（简单演示）
const dataStore = {
  devices: new Map(),
  history: []
};

// 数据模型验证
function validateMonitorData(data) {
  const required = ['deviceId', 'battery', 'runningApps'];
  return required.every(key => data[key] !== undefined);
}

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    message: '服务器运行正常',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 上传监控数据
app.post('/api/monitor/data', (req, res) => {
  try {
    const data = req.body;

    if (!validateMonitorData(data)) {
      return res.status(400).json({
        success: false,
        message: '数据格式不正确，缺少必要字段'
      });
    }

    // 保存设备信息
    const { deviceId } = data;
    dataStore.devices.set(deviceId, {
      deviceModel: data.deviceModel,
      androidVersion: data.androidVersion,
      lastUpdate: new Date().toISOString(),
      battery: data.battery,
      runningAppsCount: data.runningApps?.length || 0,
      notificationsCount: data.notifications?.length || 0
    });

    // 保存历史数据
    const record = {
      ...data,
      receivedAt: new Date().toISOString(),
      ip: req.ip
    };
    dataStore.history.push(record);

    // 限制历史记录数量
    if (dataStore.history.length > 1000) {
      dataStore.history = dataStore.history.slice(-500);
    }

    console.log(`[收到数据] 设备: ${data.deviceModel} | 电池: ${data.battery.level}% | 运行应用: ${data.runningApps.length}个`);

    res.json({
      success: true,
      message: '数据接收成功',
      data: {
        recordId: dataStore.history.length,
        deviceCount: dataStore.devices.size
      }
    });

  } catch (error) {
    console.error('处理数据失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器内部错误'
    });
  }
});

// 获取所有设备列表
app.get('/api/devices', (req, res) => {
  const devices = [];
  dataStore.devices.forEach((info, deviceId) => {
    devices.push({ deviceId, ...info });
  });

  res.json({
    success: true,
    data: devices
  });
});

// 获取指定设备的最新数据
app.get('/api/devices/:deviceId/latest', (req, res) => {
  const { deviceId } = req.params;
  const deviceData = dataStore.devices.get(deviceId);

  if (!deviceData) {
    return res.status(404).json({
      success: false,
      message: '设备未找到'
    });
  }

  res.json({
    success: true,
    data: { deviceId, ...deviceData }
  });
});

// 获取指定设备的历史数据
app.get('/api/devices/:deviceId/history', (req, res) => {
  const { deviceId } = req.params;
  const limit = parseInt(req.query.limit) || 50;

  const history = dataStore.history
    .filter(record => record.deviceId === deviceId)
    .slice(-limit);

  res.json({
    success: true,
    data: history
  });
});

// 获取统计数据
app.get('/api/stats', (req, res) => {
  const totalRecords = dataStore.history.length;
  const deviceCount = dataStore.devices.size;

  // 电池统计
  const batteryLevels = dataStore.history
    .map(r => r.battery?.level)
    .filter(level => level !== undefined);

  const avgBattery = batteryLevels.length > 0
    ? (batteryLevels.reduce((a, b) => a + b, 0) / batteryLevels.length).toFixed(1)
    : 0;

  res.json({
    success: true,
    data: {
      totalRecords,
      deviceCount,
      averageBattery: parseFloat(avgBattery),
      lastUpdate: dataStore.history.length > 0
        ? dataStore.history[dataStore.history.length - 1].receivedAt
        : null
    }
  });
});

// 清除历史数据
app.delete('/api/history', (req, res) => {
  dataStore.history = [];
  dataStore.devices.clear();

  res.json({
    success: true,
    message: '历史数据已清除'
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════╗
║         📱 手机监控后端服务已启动                 ║
╠══════════════════════════════════════════════════╣
║  端口: ${PORT}                                    ║
║  地址: http://localhost:${PORT}                    ║
║  API:  http://localhost:${PORT}/api                ║
╚══════════════════════════════════════════════════╝
  `);
  console.log('可用接口:');
  console.log('  GET  /api/health          - 健康检查');
  console.log('  POST /api/monitor/data    - 上传监控数据');
  console.log('  GET  /api/devices         - 设备列表');
  console.log('  GET  /api/devices/:id     - 设备详情');
  console.log('  GET  /api/stats           - 统计数据');
  console.log('');
});
