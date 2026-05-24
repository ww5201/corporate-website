# 阿卡网络科技 - 后台管理系统

##  项目结构

```
backend/
├── server.js              # 主服务器文件
├── models/                # 数据模型
│   ├── Product.js        # 产品模型
│   ├── Order.js          # 订单模型
│   └── Message.js        # 留言模型
├── routes/                # API 路由
│   ├── products.js       # 产品路由
│   ├── orders.js         # 订单路由
│   ── messages.js       # 留言路由
├── admin.html            # 后台管理界面
├── .env                  # 环境变量配置
├── .env.example          # 环境变量示例
└── vercel.json           # Vercel 部署配置
```

##  快速开始

### 1. 注册 MongoDB Atlas (免费)

1. 访问 https://www.mongodb.com/cloud/atlas
2. 注册免费账号
3. 创建免费集群 (M0)
4. 获取连接字符串

### 2. 配置环境变量

编辑 `.env` 文件，填入你的 MongoDB 连接字符串：

```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/luxury-co
```

### 3. 本地运行

```bash
# 启动开发服务器 (自动热重载)
npm run dev

# 或启动生产服务器
npm start
```

访问 http://localhost:3000 查看 API

### 4. 打开后台管理界面

在浏览器中打开 `admin.html` 文件

##  API 接口

### 产品管理
- `GET /api/products` - 获取所有产品
- `POST /api/products` - 创建产品
- `PUT /api/products/:id` - 更新产品
- `DELETE /api/products/:id` - 删除产品

### 订单管理
- `GET /api/orders` - 获取所有订单
- `POST /api/orders` - 创建订单
- `PUT /api/orders/:id` - 更新订单
- `DELETE /api/orders/:id` - 删除订单

### 客户留言
- `GET /api/messages` - 获取所有留言
- `POST /api/messages` - 创建留言
- `PUT /api/messages/:id` - 回复留言
- `DELETE /api/messages/:id` - 删除留言

##  部署到 Vercel (免费)

### 1. 安装 Vercel CLI

```bash
npm install -g vercel
```

### 2. 部署

```bash
cd backend
vercel login
vercel
```

### 3. 配置生产环境变量

在 Vercel 控制台添加环境变量 `MONGODB_URI`

##  默认管理员账号

```
用户名：admin
密码：admin123
```

**⚠️ 首次部署后请修改密码！**

##  技术栈

- **后端**: Node.js + Express
- **数据库**: MongoDB Atlas (云数据库)
- **ORM**: Mongoose
- **部署**: Vercel Serverless
