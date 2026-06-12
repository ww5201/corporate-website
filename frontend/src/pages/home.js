/**
 * Home Page - 首页
 */
import { api } from '../api.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { formatPriceRange } from '../utils.js';

let bannerIndex = 0;
let bannerTimer = null;

export async function homePage() {
  return {
    title: '首页',
    render: async () => {
      let products = [];
      try {
        products = await api.get('/products');
      } catch (e) { console.error(e); }

      const banners = [
        { bg: 'linear-gradient(135deg, #e74c3c, #ff6b6b)', title: '全屋定制 工厂直供', desc: '品质家居 · 低至3折起', tag: '限时特惠' },
        { bg: 'linear-gradient(135deg, #f39c12, #e67e22)', title: '新品上市 橱柜系列', desc: '设计师联名 · 限量特惠', tag: '新品首发' },
        { bg: 'linear-gradient(135deg, #8e44ad, #9b59b6)', title: '拼团更优惠', desc: '万人团购 · 价格直降到底', tag: '万人团' },
      ];

      const categories = [
        { icon: '🏠', name: '全部', path: '/category' },
        { icon: '🗄️', name: '柜类', path: '/category?cat=cabinet' },
        { icon: '👔', name: '衣柜', path: '/category?cat=wardrobe' },
        { icon: '🍳', name: '橱柜', path: '/category?cat=kitchen' },
        { icon: '✨', name: '定制', path: '/category?cat=custom' },
        { icon: '⚡', name: '秒杀', path: '/flash' },
        { icon: '🔥', name: '拼团', path: '/flash#group' },
        { icon: '💬', name: '联系', path: '/chat' },
      ];

      const productCards = products.slice(0, 10).map(p => `
        <a href="#/product/${p._id}" class="product-card">
          <div class="img-wrap">
            <img src="${p.image || p.images?.[0] || '/placeholder.png'}" alt="${p.name}" loading="lazy">
          </div>
          <div class="info">
            <div class="name">${p.name}</div>
            <div class="price">${formatPriceRange(p.price)}</div>
          </div>
        </a>
      `).join('');

      return `
        <div class="page-body">
          <!-- Banner -->
          <div class="banner" id="homeBanner">
            <div class="banner-track" id="bannerTrack" style="transform: translateX(0)">
              ${banners.map(b => `
                <div class="banner-slide" style="background: ${b.bg}">
                  <h2>${b.title}</h2>
                  <p>${b.desc}</p>
                  <span class="tag">${b.tag}</span>
                </div>
              `).join('')}
            </div>
            <div class="banner-dots">
              ${banners.map((_, i) => `<span class="banner-dot ${i === 0 ? 'active' : ''}" data-i="${i}"></span>`).join('')}
            </div>
          </div>

          <!-- Categories -->
          <div class="cat-grid">
            ${categories.map(c => `
              <a href="#${c.path}" class="cat-icon-item">
                <span class="icon">${c.icon}</span>
                <span class="name">${c.name}</span>
              </a>
            `).join('')}
          </div>

          <!-- Products -->
          <div style="padding: 0 12px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
              <h3 style="font-size:16px">💎 为你推荐</h3>
              <a href="#/category" style="font-size:13px;color:var(--primary)">更多 ›</a>
            </div>
          </div>
          <div class="product-grid">
            ${productCards || '<div class="empty-state"><div class="empty-icon">📦</div><p>暂无商品</p></div>'}
          </div>
        </div>
        ${renderBottomNav('home')}
      `;
    }
  };
}

export function mountHome() {
  // Banner auto-slide
  const track = document.getElementById('bannerTrack');
  const dots = document.querySelectorAll('.banner-dot');
  if (!track) return;

  const total = dots.length;
  if (total <= 1) return;

  bannerIndex = 0;
  clearInterval(bannerTimer);
  bannerTimer = setInterval(() => {
    bannerIndex = (bannerIndex + 1) % total;
    track.style.transform = `translateX(-${bannerIndex * 100}%)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === bannerIndex));
  }, 3500);

  dots.forEach(d => {
    d.addEventListener('click', () => {
      bannerIndex = parseInt(d.dataset.i);
      track.style.transform = `translateX(-${bannerIndex * 100}%)`;
      dots.forEach((dd, i) => dd.classList.toggle('active', i === bannerIndex));
    });
  });
}
