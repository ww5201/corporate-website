const express = require('express');
const router = express.Router();
const Message = require('../models/Message');

// 获取所有留言
router.get('/', async (req, res) => {
  try {
    const messages = await Message.find().sort({ createdAt: -1 });
    res.json(messages);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 创建留言 (客户提交)
router.post('/', async (req, res) => {
  try {
    const message = new Message(req.body);
    await message.save();
    res.status(201).json(message);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 标记为已读并回复
router.put('/:id', async (req, res) => {
  try {
    const message = await Message.findByIdAndUpdate(
      req.params.id,
      { 
        isRead: true,
        reply: req.body.reply 
      },
      { new: true }
    );
    if (!message) return res.status(404).json({ error: '留言不存在' });
    res.json(message);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 删除留言
router.delete('/:id', async (req, res) => {
  try {
    const message = await Message.findByIdAndDelete(req.params.id);
    if (!message) return res.status(404).json({ error: '留言不存在' });
    res.json({ message: '留言已删除' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
