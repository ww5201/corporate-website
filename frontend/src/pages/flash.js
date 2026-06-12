/**
 * Flash Sale Page - 秒杀/拼团页
 */
import { api } from '../api.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { formatPrice } from '../utils.js';
import { showToast } from '../components/toast.js';

export async function flashPage() {
  return {
    title: '限时秒杀',
    render: async () => {
      let products = [];
      try {
        products = await api.get('/products');
      } catch (e) { console.error(e); }

      // Take first few as "flash sale" items
      const flashItems = products.slice(0, 6);
      const groupItems = products.slice(6, 12);

      return `
        <div class="page-body">
          <!-- 秒杀头部 -->
          <div class="flash-header">
            <h2>⚡ 限时秒杀</h2>
            <div class="flash-countdown">
              <span>距结束</span>
              <span class="cd" id="cdH">00</span>:
              <span class="cd" id="cdM">00</span>:
              <span class="cd" id="cdS">00</span>
            </div>
          </div>

          <!-- 秒杀商品 -->
          <div class="product-grid" style="padding-top:12px">
            ${flashItems.map(p => `
              <a href="#/product/${p._id}" class="product-card">
                <div class="img-wrap" style="position:relative">
                  <img src="${p.image || p.images?.[0] || '/placeholder.png'}" alt="${p.name}" loading="lazy">
                  <div style="position:absolute;top:8px;left:8px;background:var(--danger);color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600">秒杀</div>
                </div>
                <div class="info">
                  <div class="name">${p.name}</div>
                  <div style="display:flex;align-items:baseline;gap:6px">
                    <div class="price">${formatPrice(p.price ? p.price * 0.7 : 0)}</div>
                    <div style="font-size:12px;color:var(--text-muted);text-decoration:line-through">${formatPrice(p.price)}</div>
                  </div>
                </div>
              </a>
            `).join('') || '<div class="empty-state" style="grid-column:1/-1"><div class="empty-icon">⚡</div><p>暂无秒杀商品</p></div>'}
          </div>

          <!-- 万人拼团 -->
          ${groupItems.length ? `
            <div style="padding:16px 12px 8px;display:flex;align-items:center;gap:8px">
              <span style="font-size:24px">🔥</span>
              <h3 style="font-size:16px;flex:1">万人拼团</h3>
              <span style="background:var(--danger);color:#fff;padding:2px 8px;border-radius:4px;font-size:11px">超值低价</span>
            </div>
            <div class="product-grid">
              ${groupItems.map(p => `
                <a href="#/product/${p._id}" class="product-card">
                  <div class="img-wrap" style="position:relative">
                    <img src="${p.image || p.images?.[0] || '/placeholder.png'}" alt="${p.name}" loading="lazy">
                    <div style="position:absolute;top:8px;left:8px;background:#ff7875;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600">拼团</div>
                  </div>
                  <div class="info">
                    <div class="name">${p.name}</div>
                    <div style="display:flex;align-items:baseline;gap:6px">
                      <div class="price">${formatPrice(p.price ? p.price * 0.6 : 0)}</div>
                      <div style="font-size:12px;color:var(--text-muted);text-decoration:line-through">${formatPrice(p.price)}</div>
                    </div>
                    <div style="font-size:11px;color:var(--text-muted);margin-top:4px">${Math.floor(Math.random() * 500 + 100)}人已拼</div>
                  </div>
                </a>
              `).join('')}
            </div>
          ` : ''}
        </div>
        ${renderBottomNav('flash')}
      `;
    }
  };
}

export function mountFlash() {
  // Countdown timer (模拟 2 小时倒计时)
  function updateCountdown() {
    const now = new Date();
    const end = new Date(now);
    end.setHours(23, 59, 59, 999);
    const diff = end - now;

    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);

    const hEl = document.getElementById('cdH');
    const mEl = document.getElementById('cdM');
    const sEl = document.getElementById('cdS');

    if (hEl) hEl.textContent = String(h).padStart(2, '0');
    if (mEl) mEl.textContent = String(m).padStart(2, '0');
    if (sEl) sEl.textContent = String(s).padStart(2, '0');
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);
}
