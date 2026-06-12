const mongoose = require('mongoose');

const chatMessageSchema = new mongoose.Schema({
  sender: {
    type: String,
    enum: ['visitor', 'admin'],
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    enum: ['text', 'image', 'order'],
    default: 'text',
  },
}, {
  timestamps: true,
});

const conversationSchema = new mongoose.Schema({
  visitorId: {
    type: String,
    required: true,
    index: true,
  },
  name: {
    type: String,
    default: '访客',
  },
  phone: {
    type: String,
    default: '',
  },
  messages: [chatMessageSchema],
  unread: {
    type: Number,
    default: 0,
  },
  status: {
    type: String,
    enum: ['open', 'closed'],
    default: 'open',
  },
}, {
  timestamps: true,
});

module.exports = mongoose.model('Conversation', conversationSchema);
