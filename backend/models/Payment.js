const mongoose = require('mongoose');

const paymentSchema = new mongoose.Schema({
  orderId: {
    type: String,
    unique: true,
    required: true,
    index: true,
  },
  productId: {
    type: String,
    default: '',
  },
  productName: {
    type: String,
    default: '',
  },
  amount: {
    type: Number,
    required: true,
  },
  payAmount: {
    type: String,
    default: '0.00',
  },
  paymentMethod: {
    type: String,
    enum: ['wechat', 'alipay'],
    default: 'wechat',
  },
  paymentType: {
    type: String,
    enum: ['full', 'deposit'],
    default: 'full',
  },
  customerName: {
    type: String,
    required: true,
  },
  customerPhone: {
    type: String,
    required: true,
  },
  customerEmail: {
    type: String,
    default: '',
  },
  remark: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    enum: ['待支付', '已支付', '已取消', '已退款'],
    default: '待支付',
  },
  tradeNo: {
    type: String,
    default: '',
  },
  paidAt: {
    type: Date,
  },
}, {
  timestamps: true,
});

module.exports = mongoose.model('Payment', paymentSchema);
