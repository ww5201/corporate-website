const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  phone: {
    type: String,
    unique: true,
    sparse: true,
    trim: true,
  },
  nickname: {
    type: String,
    default: '',
  },
  avatar: {
    type: String,
    default: '',
  },
  wechatOpenId: {
    type: String,
    unique: true,
    sparse: true,
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user',
  },
  lastLogin: {
    type: Date,
    default: Date.now,
  },
}, {
  timestamps: true,
});

module.exports = mongoose.model('User', userSchema);
