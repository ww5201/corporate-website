/**
 * Product Detail Page - 商品详情页
 */
import { api } from '../api.js';
import { formatPrice } from '../utils.js';
import { showToast } from '../components/toast.js';
import { auth } from '../auth.js';

export async function productPage(params) {
  return {
    title: '商品详情',
    render: async () => {
      let product = null;
      try {
        product = await api.get(`/products/${params.id}`);
      } catch (e) {
        return `<div class="error-page"><div class="error-icon">📦</div><h2>商品不存在</h2><a href="#/home" class="btn-primary">返回首页</a></div>`;
      }

      const images = product.images?.length ? product.images : [product.image || '/placeholder.png'];

      return `
        <div class="nav-header">
          <button class="nav-back" onclick="history.back()">‹</button>
          <div class="nav-title">商品详情</div>
          <div class="nav-right"></div>
        </div>
        <div class="page-body">
          <!-- 商品图片 -->
          <div id="productSlider" style="position:relative;overflow:hidden;background:#f5f5f5">
            <div style="display:flex;transition:transform 0.3s" id="sliderTrack">
              ${images.map(img => `
                <div style="min-width:100%;aspect-ratio:1">
                  <img src="${img}" style="width:100%;height:100%;object-fit:cover" alt="${product.name}">
                </div>
              `).join('')}
            </div>
            ${images.length > 1 ? `
              <div style="position:absolute;bottom:12px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.5);color:#fff;padding:3px 10px;border-radius:10px;font-size:12px">
                <span id="sliderIdx">1</span> / ${images.length}
              </div>
            ` : ''}
          </div>

          <!-- 商品信息 -->
          <div class="card" style="margin:12px;border-radius:var(--radius)">
            <div style="padding:16px">
              <div style="font-size:20px;font-weight:700;color:var(--danger);margin-bottom:8px">
                ${formatPrice(product.price)}
              </div>
              <h1 style="font-size:16px;line-height:1.5;margin-bottom:8px">${product.name}</h1>
              <div style="font-size:13px;color:var(--text-muted)">
                分类: ${product.category || '定制家具'}
              </div>
            </div>
          </div>

          <!-- 商品描述 -->
          ${product.description ? `
            <div class="card" style="margin:0 12px 12px;border-radius:var(--radius)">
              <div style="padding:16px">
                <div style="font-size:14px;font-weight:600;margin-bottom:8px">商品详情</div>
                <div style="font-size:13px;color:var(--text-secondary);line-height:1.8;white-space:pre-wrap">${product.description}</div>
              </div>
            </div>
          ` : ''}

          <!-- 底部操作栏 -->
          <div style="position:fixed;bottom:0;left:0;right:0;display:flex;gap:8px;padding:10px 16px;background:var(--card-bg);border-top:1px solid var(--border);z-index:100">
            <a href="#/chat" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:50px;font-size:11px;color:var(--text-muted)">
              <span style="font-size:20px">💬</span>
              客服
            </a>
            <button onclick="window._showPayModal()" class="btn-primary btn-block btn-lg" style="border-radius:var(--radius-sm)">
              立即购买
            </button>
          </div>
        </div>

        <!-- 支付弹窗 -->
        <div id="payModal" style="display:none;position:fixed;inset:0;z-index:200">
          <div style="position:absolute;inset:0;background:rgba(0,0,0,0.5)" onclick="window._hidePayModal()"></div>
          <div style="position:absolute;bottom:0;left:0;right:0;background:var(--card-bg);border-radius:16px 16px 0 0;padding:20px;max-height:80vh;overflow-y:auto">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
              <h3 style="font-size:16px">确认订单</h3>
              <button onclick="window._hidePayModal()" style="background:none;border:none;font-size:24px;color:var(--text-muted)">×</button>
            </div>

            <div class="pay-section">
              <div class="pay-section-title">商品信息</div>
              <div style="display:flex;gap:10px">
                <img src="${images[0]}" style="width:60px;height:60px;border-radius:8px;object-fit:cover">
                <div>
                  <div style="font-size:14px;font-weight:500">${product.name}</div>
                  <div style="color:var(--danger);font-size:15px;font-weight:600;margin-top:4px">${formatPrice(product.price)}</div>
                </div>
              </div>
            </div>

            <div class="pay-section">
              <div class="pay-section-title">支付方式</div>
              <div class="pay-method selected" data-method="wechat" onclick="window._selectPayMethod(this)">
                <span class="icon">💚</span>
                <div><div class="name">微信支付</div><div class="desc">推荐</div></div>
                <div class="check"></div>
              </div>
              <div class="pay-method" data-method="alipay" onclick="window._selectPayMethod(this)">
                <span class="icon">💙</span>
                <div><div class="name">支付宝</div><div class="desc">快捷支付</div></div>
                <div class="check"></div>
              </div>
            </div>

            <div class="pay-section">
              <div class="pay-section-title">联系信息</div>
              <div class="form-group">
                <input class="form-input" id="payName" placeholder="您的姓名" required>
              </div>
              <div class="form-group">
                <input class="form-input" id="payPhone" placeholder="联系电话" required>
              </div>
              <div class="form-group">
                <input class="form-input" id="payAddr" placeholder="收货地址">
              </div>
            </div>

            <div class="pay-summary">
              <div class="row"><span>商品金额</span><span>${formatPrice(product.price)}</span></div>
              <div class="row"><span>运费</span><span style="color:var(--success)">免运费</span></div>
              <div class="row total"><span>实付金额</span><span>${formatPrice(product.price)}</span></div>
            </div>

            <button id="paySubmitBtn" onclick="window._submitPay('${product._id}','${product.name.replace(/'/g, "\\'")}',${product.price || 0})" class="btn-primary btn-block btn-lg" style="margin-top:16px;border-radius:var(--radius-sm)">
              提交订单
            </button>
          </div>
        </div>
      `;
    }
  };
}

export function mountProduct(params) {
  // Image slider
  const track = document.getElementById('sliderTrack');
  const idxEl = document.getElementById('sliderIdx');
  if (track && idxEl) {
    let current = 0;
    const total = track.children.length;
    let startX = 0;

    const slider = document.getElementById('productSlider');
    slider.addEventListener('touchstart', e => { startX = e.touches[0].clientX; });
    slider.addEventListener('touchend', e => {
      const diff = e.changedTouches[0].clientX - startX;
      if (Math.abs(diff) > 50) {
        current = diff > 0 ? Math.max(0, current - 1) : Math.min(total - 1, current + 1);
        track.style.transform = `translateX(-${current * 100}%)`;
        idxEl.textContent = current + 1;
      }
    });
  }

  // Payment modal functions
  window._showPayModal = () => {
    document.getElementById('payModal').style.display = 'block';
  };
  window._hidePayModal = () => {
    document.getElementById('payModal').style.display = 'none';
  };
  window._selectPayMethod = (el) => {
    document.querySelectorAll('.pay-method').forEach(m => m.classList.remove('selected'));
    el.classList.add('selected');
  };
  window._submitPay = async (productId, productName, price) => {
    const name = document.getElementById('payName').value.trim();
    const phone = document.getElementById('payPhone').value.trim();
    const addr = document.getElementById('payAddr').value.trim();
    const method = document.querySelector('.pay-method.selected')?.dataset.method || 'wechat';

    if (!name || !phone) {
      showToast('请填写姓名和电话', 'error');
      return;
    }

    const btn = document.getElementById('paySubmitBtn');
    btn.disabled = true;
    btn.textContent = '提交中...';

    try {
      const res = await api.post('/payment/create', {
        productId,
        productName,
        amount: price,
        paymentMethod: method,
        paymentType: 'full',
        customerName: name,
        customerPhone: phone,
        customerEmail: '',
        remark: addr ? `收货地址: ${addr}` : '',
      });

      if (res.ok) {
        window._hidePayModal();
        window.location.hash = `#/payment/${res.orderId}`;
      } else {
        showToast(res.error || '下单失败', 'error');
      }
    } catch (e) {
      showToast('网络错误，请重试', 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '提交订单';
    }
  };
}
