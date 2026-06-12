const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const https = require('https');

const JWT_SECRET = process.env.JWT_SECRET || 'luxury-co-secret-key-2026';

// ====== WeChat Open Platform Config ======
const WECHAT = {
  appId: process.env.WECHAT_APP_ID || 'wx187d6ca3a6da9ca3',
  appSecret: process.env.WECHAT_APP_SECRET || 'fbb6ed4e1276bf5141a0cf64393e0a23',
};

// ====== WeChat Pay Config (fill in when merchant account ready) ======
const WXPAY = {
  mchId: process.env.WXPAY_MCH_ID || '',
  apiKey: process.env.WXPAY_API_KEY || '',
  notifyUrl: process.env.WXPAY_NOTIFY_URL || 'https://www.wgh2026.top/api/payment/wxpay/notify',
};

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: '\u672a\u767b\u5f55' });
  }
  try {
    req.user = jwt.verify(authHeader.slice(7), JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: '\u767b\u5f55\u5df2\u8fc7\u671f' });
  }
}

function adminMiddleware(req, res, next) {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: '\u65e0\u6743\u9650' });
  }
  next();
}

const router = express.Router();

// ========== Helper: HTTP GET request ==========
function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 10000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject).on('timeout', () => reject(new Error('timeout')));
  });
}

// ========== Helper: HTTP POST request (for WeChat Pay) ==========
function httpsPost(url, postData) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(postData),
      },
      timeout: 15000,
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(postData);
    req.end();
  });
}

// ========== SMS code store (in-memory, use Redis in production) ==========
const smsStore = new Map();

// Send SMS verification code
router.post('/sms/send', (req, res) => {
  try {
    const { phone } = req.body;
    if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
      return res.status(400).json({ error: '\u8bf7\u8f93\u5165\u6b63\u786e\u7684\u624b\u673a\u53f7' });
    }

    const existing = smsStore.get(phone);
    if (existing && Date.now() - existing.sentAt < 60000) {
      return res.status(429).json({ error: '\u53d1\u9002\u8fc7\u4e8e\u9891\u7e01\uff0c\u8bf760\u79d2\u540e\u91cd\u8bd5' });
    }

    const code = String(Math.floor(100000 + Math.random() * 900000));
    smsStore.set(phone, { code, sentAt: Date.now(), attempts: 0 });

    try {
      const smsService = require('../sms-service');
      smsService.sendSms(phone, code).catch(e => console.warn('SMS send failed:', e.message));
    } catch (e) {
      console.warn('SMS service not available, using debug code');
    }

    res.json({
      success: true,
      message: '\u9a8c\u8bc1\u7801\u5df2\u53d1\u9001',
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
    return res.status(400).json({ error: '\u8bf7\u586b\u5199\u624b\u673a\u53f7\u548c\u9a8c\u8bc1\u7801' });
  }
  if (!/^1[3-9]\d{9}$/.test(phone)) {
    return res.status(400).json({ error: '\u624b\u673a\u53f7\u683c\u5f0f\u4e0d\u6b63\u786e' });
  }

  const stored = smsStore.get(phone);
  if (!stored || stored.code !== code) {
    return res.status(400).json({ error: '\u9a8c\u8bc1\u7801\u9519\u8bef\u6216\u5df2\u8fc7\u671f' });
  }
  if (Date.now() - stored.sentAt > 300000) {
    smsStore.delete(phone);
    return res.status(400).json({ error: '\u9a8c\u8bc1\u7801\u5df2\u8fc7\u671f\uff0c\u8bf7\u91cd\u65b0\u83b7\u53d6' });
  }
  if ((stored.attempts || 0) >= 5) {
    return res.status(429).json({ error: '\u9a8c\u8bc1\u7801\u5c1d\u8bd5\u6b21\u6570\u8fc7\u591a' });
  }
  stored.attempts = (stored.attempts || 0) + 1;

  userDB.findOne({ phone }, (err, user) => {
    if (err) return res.status(500).json({ error: err.message });

    let isNew = false;
    const proceed = (userData) => {
      smsStore.delete(phone);
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
          nickname: userData.nickname || '',
          avatar: userData.avatar || '',
          isNew,
        },
      });
    };

    if (!user) {
      isNew = true;
      userDB.insert({
        phone,
        nickname: '\u7528\u6237' + phone.slice(-4),
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

// ========== WeChat Login (Real OAuth2) ==========
// Flow: APP/Mini-program -> wx.login() gets code -> backend exchanges for openid
router.post('/wechat/login', async (req, res) => {
  const userDB = req.app.locals.userDB;
  const { code, nickname, avatar } = req.body;

  if (!code) {
    return res.status(400).json({ error: '\u5fae\u4fe1\u6388\u6743\u5931\u8d25\uff0c\u7f3a\u5c11code' });
  }

  try {
    // Step 1: Exchange code for access_token + openid via WeChat Open Platform API
    // For APP login: https://api.weixin.qq.com/sns/oauth2/access_token
    // For Mini-program: https://api.weixin.qq.com/sns/jscode2session
    // We support both modes
    const url = `https://api.weixin.qq.com/sns/oauth2/access_token?appid=${WECHAT.appId}&secret=${WECHAT.appSecret}&code=${code}&grant_type=authorization_code`;

    let wxRes;
    try {
      wxRes = await httpsGet(url);
    } catch (e) {
      // Fallback to jscode2session (mini-program style)
      const fallbackUrl = `https://api.weixin.qq.com/sns/jscode2session?appid=${WECHAT.appId}&secret=${WECHAT.appSecret}&js_code=${code}&grant_type=authorization_code`;
      wxRes = await httpsGet(fallbackUrl);
    }

    console.log('[WeChat Login] API response:', JSON.stringify(wxRes));

    if (wxRes.errcode && wxRes.errcode !== 0) {
      console.error('[WeChat Login] Error:', wxRes.errcode, wxRes.errmsg);
      return res.status(400).json({
        error: `\u5fae\u4fe1\u6388\u6743\u5931\u8d25: ${wxRes.errmsg || '\u672a\u77e5\u9519\u8bef'}`,
        errcode: wxRes.errcode,
      });
    }

    const openid = wxRes.openid;
    const unionid = wxRes.unionid || null;

    if (!openid) {
      return res.status(400).json({ error: '\u83b7\u53d6\u5fae\u4fe1openid\u5931\u8d25' });
    }

    // Step 2: Find or create user by openid
    userDB.findOne({ wechatOpenId: openid }, (err, user) => {
      if (err) return res.status(500).json({ error: err.message });

      let isNew = false;
      const proceed = (userData) => {
        const token = jwt.sign(
          { id: userData._id, phone: userData.phone || '', role: userData.role || 'user' },
          JWT_SECRET,
          { expiresIn: '30d' }
        );

        res.json({
          success: true,
          token,
          user: {
            id: userData._id,
            phone: userData.phone || '',
            nickname: userData.nickname || '',
            avatar: userData.avatar || '',
            isNew,
          },
        });
      };

      if (!user) {
        isNew = true;
        const newUser = {
          wechatOpenId: openid,
          unionId: unionid,
          nickname: nickname || '\u5fae\u4fe1\u7528\u6237',
          avatar: avatar || '',
          role: 'user',
          lastLogin: new Date().toISOString(),
          createdAt: new Date().toISOString(),
        };
        userDB.insert(newUser, (err, inserted) => {
          if (err) return res.status(500).json({ error: err.message });
          proceed(inserted);
        });
      } else {
        // Update nickname/avatar if provided
        const updates = { lastLogin: new Date().toISOString() };
        if (nickname) updates.nickname = nickname;
        if (avatar) updates.avatar = avatar;
        userDB.update({ _id: user._id }, { $set: updates }, {}, () => {
          proceed(user);
        });
      }
    });
  } catch (err) {
    console.error('[WeChat Login] Exception:', err);
    res.status(500).json({ error: `\u5fae\u4fe1\u767b\u5f55\u5f02\u5e38: ${err.message}` });
  }
});

// ========== WeChat Pay - Create Order ==========
router.post('/payment/wxpay/create', authMiddleware, async (req, res) => {
  const { orderId, amount, description, clientIp } = req.body;

  if (!orderId || !amount || amount <= 0) {
    return res.status(400).json({ error: '\u53c2\u6570\u9519\u8bef' });
  }

  if (!WXPAY.mchId || !WXPAY.apiKey) {
    return res.status(503).json({
      error: '\u5fae\u4fe1\u652f\u4ed8\u672a\u914d\u7f6e\u5546\u6237\u53f7',
      _debug: 'Please set WXPAY_MCH_ID and WXPAY_API_KEY env vars',
    });
  }

  try {
    // V3 API - unified order
    const nonceStr = crypto.randomBytes(16).toString('hex');
    const timestamp = Math.floor(Date.now() / 1000).toString();

    const body = {
      appid: WECHAT.appId,
      mch_id: WXPAY.mchId,
      description: description || '\u5353\u7fcc\u5b9a\u5236-\u8ba2\u5355' + orderId,
      out_trade_no: orderId,
      notify_url: WXPAY.notifyUrl,
      amount: { total: Math.round(amount * 100), currency: 'CNY' },
      payer: { openid: req.body.openid || '' },
    };

    // TODO: Sign with API v3 key and call WeChat Pay API
    // This requires merchant certificate setup
    res.json({
      success: false,
      error: '\u5fae\u4fe1\u652f\u4ed8V3 API \u9700\u8981\u5546\u6237\u8bc1\u4e66\u914d\u7f6e\uff0c\u8bf7\u5148\u5728\u5fae\u4fe1\u5546\u6237\u5e73\u53f0\u7533\u8bf7\u652f\u4ed8\u8d44\u683c',
      _debugOrder: body,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ========== WeChat Pay - Notify Callback ==========
router.post('/payment/wxpay/notify', (req, res) => {
  // TODO: Verify signature and update order status
  console.log('[WxPay Notify] Received:', JSON.stringify(req.body).slice(0, 500));
  res.json({ code: 'SUCCESS', message: '\u6210\u529f' });
});

// ========== Get current user ==========
router.get('/me', authMiddleware, (req, res) => {
  const userDB = req.app.locals.userDB;
  userDB.findOne({ _id: req.user.id }, (err, user) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!user) return res.status(404).json({ error: '\u7528\u6237\u4e0d\u5b58\u5728' });

    res.json({
      success: true,
      user: {
        id: user._id,
        phone: user.phone || '',
        nickname: user.nickname,
        avatar: user.avatar || '',
        role: user.role || 'user',
      },
    });
  });
});

// ========== Logout ==========
router.post('/logout', (req, res) => {
  res.json({ success: true, message: '\u5df2\u9000\u51fa\u767b\u5f55' });
});

module.exports = { router, authMiddleware, adminMiddleware };
