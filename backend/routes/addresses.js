const express = require('express');
const router = express.Router();

// Address management API - uses NeDB
// Requires auth middleware from auth.js
const { authMiddleware } = require('./auth');

// Get all addresses for current user
router.get('/', authMiddleware, (req, res) => {
  const addressDB = req.app.locals.addressDB;
  if (!addressDB) return res.status(500).json({ error: '地址服务不可用' });

  addressDB.find({ userId: req.user.id }, (err, addresses) => {
    if (err) return res.status(500).json({ error: err.message });
    // Sort: default first, then by createdAt desc
    addresses.sort((a, b) => {
      if (a.isDefault && !b.isDefault) return -1;
      if (!a.isDefault && b.isDefault) return 1;
      return new Date(b.createdAt) - new Date(a.createdAt);
    });
    res.json({ success: true, addresses: addresses || [] });
  });
});

// Create new address
router.post('/', authMiddleware, (req, res) => {
  const addressDB = req.app.locals.addressDB;
  if (!addressDB) return res.status(500).json({ error: '地址服务不可用' });

  const { name, phone, province, city, district, detail, isDefault } = req.body;

  if (!name || !phone || !province || !city || !detail) {
    return res.status(400).json({ error: '请填写完整的地址信息' });
  }

  const newAddr = {
    userId: req.user.id,
    name,
    phone,
    province,
    city,
    district: district || '',
    detail,
    isDefault: isDefault || false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  const doInsert = () => {
    addressDB.insert(newAddr, (err, doc) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ success: true, address: doc });
    });
  };

  // If setting as default, clear other defaults first
  if (newAddr.isDefault) {
    addressDB.update(
      { userId: req.user.id, isDefault: true },
      { $set: { isDefault: false } },
      { multi: true },
      () => doInsert()
    );
  } else {
    // If this is the first address, make it default
    addressDB.count({ userId: req.user.id }, (err, count) => {
      if (count === 0) newAddr.isDefault = true;
      doInsert();
    });
  }
});

// Update address
router.put('/:id', authMiddleware, (req, res) => {
  const addressDB = req.app.locals.addressDB;
  if (!addressDB) return res.status(500).json({ error: '地址服务不可用' });

  const { name, phone, province, city, district, detail, isDefault } = req.body;
  const updates = { updatedAt: new Date().toISOString() };

  if (name !== undefined) updates.name = name;
  if (phone !== undefined) updates.phone = phone;
  if (province !== undefined) updates.province = province;
  if (city !== undefined) updates.city = city;
  if (district !== undefined) updates.district = district;
  if (detail !== undefined) updates.detail = detail;
  if (isDefault !== undefined) updates.isDefault = isDefault;

  const doUpdate = () => {
    addressDB.update(
      { _id: req.params.id, userId: req.user.id },
      { $set: updates },
      {},
      (err, numReplaced) => {
        if (err) return res.status(500).json({ error: err.message });
        if (numReplaced === 0) return res.status(404).json({ error: '地址不存在' });
        addressDB.findOne({ _id: req.params.id }, (err, doc) => {
          if (err) return res.status(500).json({ error: err.message });
          res.json({ success: true, address: doc });
        });
      }
    );
  };

  // If setting as default, clear other defaults first
  if (isDefault) {
    addressDB.update(
      { userId: req.user.id, isDefault: true, _id: { $ne: req.params.id } },
      { $set: { isDefault: false } },
      { multi: true },
      () => doUpdate()
    );
  } else {
    doUpdate();
  }
});

// Delete address
router.delete('/:id', authMiddleware, (req, res) => {
  const addressDB = req.app.locals.addressDB;
  if (!addressDB) return res.status(500).json({ error: '地址服务不可用' });

  addressDB.remove({ _id: req.params.id, userId: req.user.id }, {}, (err, numRemoved) => {
    if (err) return res.status(500).json({ error: err.message });
    if (numRemoved === 0) return res.status(404).json({ error: '地址不存在' });
    res.json({ success: true });
  });
});

module.exports = router;
