const express = require('express');

const router = express.Router();

function generateOrderId() {
  const now = new Date();
  const pad = (n, l = 2) => String(n).padStart(l, '0');
  const rand = Math.random().toString(36).slice(2, 8).toUpperCase();
  return `ZY${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}${rand}`;
}

// Create payment order
router.post('/create', (req, res) => {
  const payDB = req.app.locals.paymentDB;
  const {
    productId, productName, amount, paymentMethod, paymentType,
    customerName, customerPhone, customerEmail, remark,
  } = req.body;

  if (!customerName || !customerPhone) {
    return res.status(400).json({ error: '请填写姓名和电话', ok: false });
  }
  if (!amount || amount <= 0) {
    return res.status(400).json({ error: '支付金额无效', ok: false });
  }

  const orderId = generateOrderId();

  payDB.insert({
    orderId,
    productId: productId || '',
    productName: productName || '定制家具',
    amount,
    payAmount: amount.toFixed(2),
    paymentMethod: paymentMethod || 'wechat',
    paymentType: paymentType || 'full',
    customerName,
    customerPhone,
    customerEmail: customerEmail || '',
    remark: remark || '',
    status: '待支付',
    createdAt: new Date().toISOString(),
  }, (err, doc) => {
    if (err) {
      console.error('Payment create error:', err);
      return res.status(500).json({ ok: false, error: err.message });
    }
    res.json({ ok: true, orderId, payUrl: '' });
  });
});

// Query payment status
router.get('/status/:orderId', (req, res) => {
  const payDB = req.app.locals.paymentDB;
  payDB.findOne({ orderId: req.params.orderId }, (err, payment) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!payment) return res.status(404).json({ error: '订单不存在' });

    res.json({
      orderId: payment.orderId,
      status: payment.status,
      payAmount: payment.payAmount,
      paymentMethod: payment.paymentMethod,
      productName: payment.productName,
      createdAt: payment.createdAt,
      paidAt: payment.paidAt,
    });
  });
});

// List orders (with optional phone filter)
router.get('/list', (req, res) => {
  const payDB = req.app.locals.paymentDB;
  const { phone, limit = 50 } = req.query;
  const filter = {};
  if (phone) filter.customerPhone = phone;

  payDB.find(filter).sort({ createdAt: -1 }).limit(Number(limit)).exec((err, docs) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ data: docs });
  });
});

// Mock payment confirmation (dev/test only)
router.post('/mock-confirm', (req, res) => {
  const payDB = req.app.locals.paymentDB;
  const { orderId } = req.body;
  if (!orderId) {
    return res.status(400).json({ ok: false, error: '缺少订单号' });
  }

  payDB.findOne({ orderId }, (err, payment) => {
    if (err) return res.status(500).json({ ok: false, error: err.message });
    if (!payment) return res.status(404).json({ ok: false, error: '订单不存在' });

    payDB.update(
      { _id: payment._id },
      { $set: { status: '已支付', paidAt: new Date().toISOString(), tradeNo: 'MOCK' + Date.now() } },
      {},
      (err) => {
        if (err) return res.status(500).json({ ok: false, error: err.message });
        res.json({ ok: true, orderId, status: '已支付' });
      }
    );
  });
});

// WeChat pay callback (TODO: real integration)
router.post('/wechat/notify', (req, res) => {
  res.json({ code: 'SUCCESS', message: '成功' });
});

// Alipay callback (TODO: real integration)
router.post('/alipay/notify', (req, res) => {
  res.send('success');
});

module.exports = router;
