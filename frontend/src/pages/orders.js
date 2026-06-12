/**
 * Orders Page - 订单列表
 */
import { api } from '../api.js';
import { auth } from '../auth.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { formatPrice, timeAgo } from '../utils.js';

export async function ordersPage() {
  if (!auth.isLoggedIn()) {
    window.location.hash = '#/login';
    return { title: '订单', render: () => '' };
  }

  return {
    title: '我的订单',
    render: async () => {
      let orders = [];
      try {
        const res = await api.get('/payment/list');
        orders = res.data || [];
      } catch (e) { console.error(e); }

      // Filter by current user's phone
      const user = auth.getUser();
      if (user?.phone) {
        orders = orders.filter(o => o.customerPhone === user.phone);
      }

      return `
        <div class="nav-header">
          <button class="nav-back" onclick="history.back()">‹</button>
          <div class="nav-title">我的订单</div>
          <div class="nav-right"></div>
        </div>
        <div class="page-body" style="padding:12px">
          ${orders.length ? orders.map(o => `
            <a href="#/payment/${o.orderId}" class="order-item" style="display:block">
              <div class="order-header">
                <span>${o.orderId}</span>
                <span class="order-status">${o.status}</span>
              </div>
              <div class="order-product">
                <div class="img" style="background:var(--border);display:flex;align-items:center;justify-content:center;font-size:24px">📦</div>
                <div style="flex:1">
                  <div class="name">${o.productName || '定制家具'}</div>
                  <div style="font-size:12px;color:var(--text-muted);margin-top:4px">${o.paymentType === 'deposit' ? '定金' : '全款'} · ${o.paymentMethod === 'wechat' ? '微信支付' : o.paymentMethod === 'alipay' ? '支付宝' : o.paymentMethod}</div>
                </div>
              </div>
              <div class="order-footer">
                <span style="font-size:12px;color:var(--text-muted)">${timeAgo(o.createdAt)}</span>
                <span class="total">¥${o.payAmount}</span>
              </div>
            </a>
          `).join('') : '<div class="empty-state"><div class="empty-icon">📦</div><p>暂无订单</p><a href="#/home" class="btn-primary" style="margin-top:16px">去逛逛</a></div>'}
        </div>
        ${renderBottomNav('orders')}
      `;
    }
  };
}

export function mountOrders() {}
