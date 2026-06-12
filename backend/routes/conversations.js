const express = require('express');
const Conversation = require('../models/Conversation');

const router = express.Router();

// 获取所有对话列表
router.get('/', async (req, res) => {
  try {
    const conversations = await Conversation.find()
      .sort({ updatedAt: -1 })
      .limit(50);
    res.json(conversations);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 创建对话
router.post('/', async (req, res) => {
  try {
    const { visitorId, name, phone } = req.body;
    if (!visitorId) {
      return res.status(400).json({ error: '缺少 visitorId' });
    }

    // 查找已有对话
    let conv = await Conversation.findOne({ visitorId });
    if (conv) {
      return res.json(conv);
    }

    conv = new Conversation({
      visitorId,
      name: name || '访客',
      phone: phone || '',
      messages: [],
    });
    await conv.save();
    res.status(201).json(conv);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 获取对话的消息
router.get('/:id/messages', async (req, res) => {
  try {
    const conv = await Conversation.findById(req.params.id);
    if (!conv) {
      return res.status(404).json({ error: '对话不存在' });
    }
    res.json(conv.messages);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 发送消息到对话
router.post('/:id/messages', async (req, res) => {
  try {
    const { sender, content, type } = req.body;
    if (!content) {
      return res.status(400).json({ error: '消息不能为空' });
    }

    const conv = await Conversation.findById(req.params.id);
    if (!conv) {
      return res.status(404).json({ error: '对话不存在' });
    }

    const message = {
      sender: sender || 'visitor',
      content,
      type: type || 'text',
    };

    conv.messages.push(message);
    if (sender === 'visitor') {
      conv.unread += 1;
    }
    await conv.save();

    // 获取刚保存的消息 (带 _id 和 createdAt)
    const savedMsg = conv.messages[conv.messages.length - 1];

    // 通知 WebSocket 广播
    if (global.wsBroadcast) {
      global.wsBroadcast(req.params.id, {
        type: 'new_message',
        message: savedMsg,
      });
    }

    res.status(201).json(savedMsg);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 轮询新消息
router.get('/:id/poll', async (req, res) => {
  try {
    const { since } = req.query;
    const conv = await Conversation.findById(req.params.id);
    if (!conv) {
      return res.status(404).json({ error: '对话不存在' });
    }

    let messages = conv.messages;
    if (since) {
      const sinceDate = new Date(since);
      messages = messages.filter(m => new Date(m.createdAt) > sinceDate);
    }

    res.json({ messages });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
