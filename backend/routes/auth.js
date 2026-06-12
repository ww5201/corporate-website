const express = require('express');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'luxury-co-secret-key-2026';

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: '未登录' });
  }
  try {
    req.user = jwt.verify(authHeader.slice(7), JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: '登录已过期' });
  }
}

function adminMiddleware(req, res, next) {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: '无权限' });
  }
  next();
}

const router = express.Router();

// SMS code store (in-memory, use Redis in production)
const smsStore = new Map();

// Send SMS verification code
router.post('/sms/send', (req, res) => {
  try {
    const { phone } = req.body;
    if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
      return res.status(400).json({ error: '请输入正确的手机号' });
    }

    const existing = smsStore.get(phone);
    if (existing && Date.now() - existing.sentAt < 60000) {
      return res.status(429).json({ error: '发送过于频繁，请60秒后重试' });
    }

    const code = String(Math.floor(100000 + Math.random() * 900000));
    smsStore.set(phone, { code, sentAt: Date.now(), attempts: 0 });

    // Try to send via Aliyun SMS
    try {
      const smsService = require('../sms-service');
      smsService.sendSms(phone, code).catch(e => console.warn('SMS send failed:', e.message));
    } catch (e) {
      console.warn('SMS service not available, using debug code');
    }

    res.json({
      success: true,
      message: '验证码已发送',
      _debugCode: code,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Phone + code login (auto-register)
router.post('/phone/login', (req, res) => {
  const userDB = req.app.locals.userDB;
  const { phone, code } = req.body;

  if (!phone || !code) {
    return res.status(400).json({ error: '请输入手机号和验证码' });
  }

  const smsData = smsStore.get(phone);
  if (!smsData) {
    return res.status(400).json({ error: '请先获取验证码' });
  }
  if (smsData.code !== code) {
    smsData.attempts++;
    if (smsData.attempts >= 5) {
      smsStore.delete(phone);
      return res.status(400).json({ error: '验证码错误次数过多' });
    }
    return res.status(400).json({ error: '验证码错误' });
  }
  if (Date.now() - smsData.sentAt > 300000) {
    smsStore.delete(phone);
    return res.status(400).json({ error: '验证码已过期' });
  }
  smsStore.delete(phone);

  userDB.findOne({ phone }, (err, user) => {
    if (err) return res.status(500).json({ error: err.message });

    let isNew = false;
    const proceed = (userData) => {
      const token = jwt.sign(
        { id: userData._id, phone: userData.phone, role: userData.role || 'user' },
        JWT_SECRET,
        { expiresIn: '30d' }
      );

      res.json({
        success: true,
        token,
        user: {
          id: userData._id,
          phone: userData.phone,
          nickname: userData.nickname,
          avatar: userData.avatar || '',
          isNew,
        },
      });
    };

    if (!user) {
      isNew = true;
      userDB.insert({
        phone,
        nickname: '用户' + phone.slice(-4),
        avatar: '',
        role: 'user',
        lastLogin: new Date().toISOString(),
        createdAt: new Date().toISOString(),
      }, (err, newUser) => {
        if (err) return res.status(500).json({ error: err.message });
        proceed(newUser);
      });
    } else {
      userDB.update({ _id: user._id }, { $set: { lastLogin: new Date().toISOString() } }, {}, () => {
        proceed(user);
      });
    }
  });
});

// WeChat login (Mock)
router.post('/wechat/login', (req, res) => {
  const userDB = req.app.locals.userDB;
  const { code, nickname, avatar } = req.body;
  if (!code) {
    return res.status(400).json({ error: '微信授权失败' });
  }

  const mockOpenId = 'wx_' + code.slice(0, 16);

  userDB.findOne({ wechatOpenId: mockOpenId }, (err, user) => {
    if (err) return res.status(500).json({ error: err.message });

    let isNew = false;
    const proceed = (userData) => {
      const token = jwt.sign(
        { id: userData._id, phone: userData.phone, role: userData.role || 'user' },
        JWT_SECRET,
        { expiresIn: '30d' }
      );

      res.json({
        success: true,
        token,
        user: {
          id: userData._id,
          phone: userData.phone || '',
          nickname: userData.nickname,
          avatar: userData.avatar || '',
          isNew,
        },
      });
    };

    if (!user) {
      isNew = true;
      userDB.insert({
        wechatOpenId: mockOpenId,
        nickname: nickname || '微信用户',
        avatar: avatar || '',
        role: 'user',
        lastLogin: new Date().toISOString(),
        createdAt: new Date().toISOString(),
      }, (err, newUser) => {
        if (err) return res.status(500).json({ error: err.message });
        proceed(newUser);
      });
    } else {
      userDB.update({ _id: user._id }, { $set: { lastLogin: new Date().toISOString() } }, {}, () => {
        proceed(user);
      });
    }
  });
});

// Get current user
router.get('/me', authMiddleware, (req, res) => {
  const userDB = req.app.locals.userDB;
  userDB.findOne({ _id: req.user.id }, (err, user) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!user) return res.status(404).json({ error: '用户不存在' });

    res.json({
      success: true,
      user: {
        id: user._id,
        phone: user.phone || '',
        nickname: user.nickname,
        avatar: user.avatar || '',
        role: user.role,
      },
    });
  });
});

// Update user profile
router.put('/me', authMiddleware, (req, res) => {
  const userDB = req.app.locals.userDB;
  const { nickname, avatar } = req.body;

  const updates = {};
  if (nickname !== undefined) updates.nickname = nickname;
  if (avatar !== undefined) updates.avatar = avatar;

  userDB.update({ _id: req.user.id }, { $set: updates }, {}, (err) => {
    if (err) return res.status(500).json({ error: err.message });

    userDB.findOne({ _id: req.user.id }, (err, user) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json({
        success: true,
        user: {
          id: user._id,
          phone: user.phone || '',
          nickname: user.nickname,
          avatar: user.avatar || '',
        },
      });
    });
  });
});

module.exports = router;
module.exports.authMiddleware = authMiddleware;
module.exports.adminMiddleware = adminMiddleware;
module.exports.JWT_SECRET = JWT_SECRET;
