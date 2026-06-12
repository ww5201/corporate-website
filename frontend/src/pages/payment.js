/**
 * Payment Page - 支付页面
 */
import { api } from '../api.js';
import { showToast } from '../components/toast.js';

export async function paymentPage(params) {
  const orderId = params.orderId;

  return {
    title: '支付结果',
    render: async () => {
      let order = null;
      try {
        order = await api.get(`/payment/status/${orderId}`);
      } catch (e) {
        return `
          <div class="pay-result">
            <div class="icon">❌</div>
            <h2>订单不存在</h2>
            <p class="desc">请检查订单号是否正确</p>
            <div class="actions">
              <a href="#/home" class="btn-primary">返回首页</a>
            </div>
          </div>
        `;
      }

      const isPaid = order.status === '已支付';
      const isPending = order.status === '待支付';

      return `
        <div class="nav-header">
          <button class="nav-back" onclick="window.location.hash='#/orders'">‹</button>
          <div class="nav-title">支付结果</div>
          <div class="nav-right"></div>
        </div>
        <div class="page-body">
          <div class="pay-result">
            <div class="icon">${isPaid ? '✅' : isPending ? '⏳' : '❌'}</div>
            <h2>${isPaid ? '支付成功' : isPending ? '等待确认' : order.status}</h2>
            <p class="desc">${isPaid ? '您的付款已确认，我们将尽快安排生产！' : isPending ? '请完成支付，我们将在确认收款后通知您。' : ''}</p>
            <div class="order-id">订单号: ${orderId}</div>

            ${isPending ? `
              <div class="pay-section" style="width:100%;max-width:400px;text-align:left">
                <div class="pay-section-title">订单详情</div>
                <div class="row"><span style="color:var(--text-muted)">支付金额</span><span style="color:var(--danger);font-weight:600">¥${order.payAmount}</span></div>
                <div class="row"><span style="color:var(--text-muted)">支付方式</span><span>${order.paymentMethod === 'wechat' ? '微信支付' : order.paymentMethod === 'alipay' ? '支付宝' : order.paymentMethod}</span></div>
                <div class="row"><span style="color:var(--text-muted)">订单状态</span><span style="color:var(--warning)">${order.status}</span></div>
              </div>

              <div class="actions" style="margin-top:16px">
                <button class="btn-primary" onclick="window._mockPay('${orderId}')">模拟支付完成</button>
                <a href="#/home" class="btn-outline">返回首页</a>
              </div>
            ` : `
              <div class="actions">
                <a href="#/orders" class="btn-primary">查看订单</a>
                <a href="#/home" class="btn-outline">返回首页</a>
              </div>
            `}
          </div>
        </div>
      `;
    }
  };
}

export function mountPayment(params) {
  window._mockPay = async (orderId) => {
    try {
      const res = await api.post('/payment/mock-confirm', { orderId });
      if (res.ok) {
        showToast('支付成功！', 'success');
        setTimeout(() => {
          window.location.hash = `#/payment/${orderId}`;
        }, 500);
      }
    } catch (e) {
      showToast('支付失败', 'error');
    }
  };
}
