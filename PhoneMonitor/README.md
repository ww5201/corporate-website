# 📱 PhoneMonitor - 手机监控器

一个 Android 应用，可以监控手机的电池状态、运行中应用、通知信息，并将数据上传到后端服务器。

## ✨ 功能特性

### Android 端
- 🔋 **电池监控** - 实时监控电量、充电状态、温度、电压等
- 📊 **运行应用监控** - 追踪后台运行的应用及其资源使用
- 🔔 **通知收集** - 拦截并记录所有应用通知
- 📦 **应用列表** - 获取已安装应用信息
- 🔄 **后台服务** - 前台服务持续运行，支持开机自启
- 📡 **自动上传** - 每5分钟自动上传数据到服务器

### 后端服务
- 🌐 RESTful API 接口
- 📈 数据统计和历史记录
- 📱 多设备支持
- 🔄 实时数据接收

## 📁 项目结构

```
PhoneMonitor/
├── app/                          # Android 应用
│   ├── build.gradle.kts         # 应用构建配置
│   └── src/main/
│       ├── AndroidManifest.xml  # 应用清单
│       ├── java/com/example/phonemonitor/
│       │   ├── MainActivity.kt           # 主界面
│       │   ├── PhoneMonitorApp.kt        # Application 类
│       │   ├── api/                      # 网络请求
│       │   │   ├── ApiService.kt
│       │   │   └── RetrofitClient.kt
│       │   ├── model/                    # 数据模型
│       │   │   └── Models.kt
│       │   ├── service/                  # 后台服务
│       │   │   ├── MonitorService.kt
│       │   │   └── NotificationCollectorService.kt
│       │   ├── receiver/                 # 广播接收器
│       │   │   └── BootReceiver.kt
│       │   └── util/                     # 工具类
│       │       ├── DataCollector.kt
│       │       ├── DataUploader.kt
│       │       └── NetworkUtil.kt
│       └── res/                          # 资源文件
│           ├── layout/
│           │   └── activity_main.xml
│           └── values/
├── backend/                      # 后端服务
│   ├── server.js                 # Express 服务器
│   ├── package.json
│   └── README.md
├── build.gradle.kts              # 项目构建配置
├── settings.gradle.kts
└── README.md
```

## 🚀 快速开始

### 前置要求

- Android Studio (推荐 2023.1+)
- JDK 17+
- Node.js 18+ (用于后端)
- Android 手机或模拟器

### 1. 克隆项目

```bash
git clone <repository-url>
cd PhoneMonitor
```

### 2. 配置 Android 项目

1. 用 Android Studio 打开 `PhoneMonitor` 目录
2. 等待 Gradle 同步完成
3. 修改服务器地址（根据你的环境）:
   - 打开 `app/src/main/java/com/example/phonemonitor/api/RetrofitClient.kt`
   - 修改 `DEFAULT_SERVER_URL` 为你的服务器地址

```kotlin
private const val DEFAULT_SERVER_URL = "http://10.0.2.2:8080/"
```

### 3. 启动后端服务

```bash
cd backend
npm install
npm start
```

服务器将在 `http://localhost:8080` 启动

### 4. 运行 Android 应用

1. 连接 Android 手机或启动模拟器
2. 点击 Android Studio 中的 ▶️ 运行按钮
3. 应用将安装并启动

### 5. 授权权限

首次运行时，应用会请求以下权限：

1. **通知监听权限** - 点击「通知监听权限」按钮，在设置中开启
2. **使用情况访问权限** - 点击「使用情况访问权限」按钮，在设置中开启
3. **通知权限** - 允许应用发送通知（用于前台服务）

### 6. 启动监控

1. 点击「启动监控」按钮
2. 应用将开始收集数据并上传到服务器
3. 可以点击「测试连接」验证服务器连接

## 🔧 配置说明

### 服务器地址配置

根据你的部署方式，修改服务器地址：

| 环境 | 地址 |
|------|------|
| Android 模拟器 | `http://10.0.2.2:8080/` |
| 本地真机（同一网络） | `http://你电脑的IP:8080/` |
| 云服务器 | `http://你的服务器IP:8080/` |

### 获取电脑 IP 地址

**Windows:**
```cmd
ipconfig
```

**macOS/Linux:**
```bash
ifconfig
# 或
ip addr
```

## 📡 API 接口

### 健康检查
```
GET /api/health
```

### 上传监控数据
```
POST /api/monitor/data
```

### 获取设备列表
```
GET /api/devices
```

### 获取设备详情
```
GET /api/devices/:deviceId/latest
```

### 获取统计数据
```
GET /api/stats
```

详细 API 文档请查看 `backend/README.md`

## 🛠️ 技术栈

### Android 端
- **语言**: Kotlin
- **最低 SDK**: Android 8.0 (API 26)
- **目标 SDK**: Android 14 (API 34)
- **架构**: Service + Repository
- **网络**: Retrofit 2 + OkHttp
- **异步**: Kotlin Coroutines
- **UI**: Material Design 3

### 后端
- **运行时**: Node.js
- **框架**: Express.js
- **存储**: 内存（可扩展为 MongoDB）

## 🔒 权限说明

| 权限 | 用途 |
|------|------|
| `INTERNET` | 上传数据到服务器 |
| `FOREGROUND_SERVICE` | 运行后台监控服务 |
| `POST_NOTIFICATIONS` | 显示服务通知 |
| `PACKAGE_USAGE_STATS` | 获取应用使用统计 |
| `BIND_NOTIFICATION_LISTENER_SERVICE` | 收集应用通知 |
| `RECEIVE_BOOT_COMPLETED` | 开机自启动 |
| `QUERY_ALL_PACKAGES` | 获取已安装应用列表 |

## ⚠️ 注意事项

1. **电池优化** - 建议在系统设置中关闭此应用的电池优化，以确保后台服务稳定运行
2. **网络要求** - 手机需要能访问到后端服务器
3. **隐私安全** - 此应用会收集设备信息，请确保在合法合规的场景下使用
4. **通知权限** - Android 13+ 需要额外的通知权限

## 🐛 常见问题

### Q: 后台服务被杀死？
A: 
- 关闭应用的电池优化
- 在最近任务中锁定应用
- 检查是否有其他省电工具阻止后台运行

### Q: 无法获取通知？
A: 
- 确保已开启通知监听权限
- 检查 Android 设置 → 通知 → 通知访问权限

### Q: 无法获取应用使用情况？
A: 
- 确保已开启使用情况访问权限
- 检查 Android 设置 → 安全 → 有使用权限的应用

### Q: 无法连接服务器？
A: 
- 检查服务器地址是否正确
- 确保手机和服务器在同一网络
- 检查防火墙设置
- 尝试使用 `ping` 或 `curl` 测试连接

## 📝 开发说明

### 添加新功能

1. 在 `model/Models.kt` 中添加数据模型
2. 在 `api/ApiService.kt` 中添加 API 接口
3. 在 `util/DataCollector.kt` 中添加数据收集逻辑
4. 在 `service/MonitorService.kt` 中集成到监控流程

### 调试技巧

- 使用 `adb logcat` 查看应用日志
- 使用 Postman 测试后端 API
- 检查 `backend/server.js` 中的控制台输出

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
