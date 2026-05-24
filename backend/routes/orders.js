const express = require('express');
const router = express.Router();
const Order = require('../models/Order');

// 获取所有订单
router.get('/', async (req, res) => {
  try {
    const orders = await Order.find().sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 获取单个订单
router.get('/:id', async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);
    if (!order) return res.status(404).json({ error: '订单不存在' });
    res.json(order);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 创建订单 (客户下单)
router.post('/', async (req, res) => {
  try {
    const order = new Order(req.body);
    await order.save();
    res.status(201).json(order);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 更新订单状态
router.put('/:id', async (req, res) => {
  try {
    const order = await Order.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );
    if (!order) return res.status(404).json({ error: '订单不存在' });
    res.json(order);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 删除订单
router.delete('/:id', async (req, res) => {
  try {
    const order = await Order.findByIdAndDelete(req.params.id);
    if (!order) return res.status(404).json({ error: '订单不存在' });
    res.json({ message: '订单已删除' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
