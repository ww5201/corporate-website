/**
 * Category Page - 分类页
 */
import { api } from '../api.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { formatPriceRange } from '../utils.js';

const CATEGORIES = [
  { key: 'all', icon: '📦', name: '全部' },
  { key: 'cabinet', icon: '🗄️', name: '柜类' },
  { key: 'wardrobe', icon: '👔', name: '衣柜' },
  { key: 'kitchen', icon: '🍳', name: '橱柜' },
  { key: 'custom', icon: '✨', name: '定制' },
];

export async function categoryPage(params, query) {
  const activeCat = query?.cat || 'all';

  return {
    title: '分类',
    render: async () => {
      let products = [];
      try {
        products = await api.get('/products');
      } catch (e) { console.error(e); }

      const filtered = activeCat === 'all'
        ? products
        : products.filter(p => (p.category || '').includes(CATEGORIES.find(c => c.key === activeCat)?.name || ''));

      return `
        <div class="nav-header">
          <div class="nav-title">商品分类</div>
        </div>
        <div class="page-body cat-layout">
          <div class="cat-sidebar">
            ${CATEGORIES.map(c => `
              <div class="cat-sidebar-item ${activeCat === c.key ? 'active' : ''}" data-cat="${c.key}">
                <span class="icon">${c.icon}</span>
                <span>${c.name}</span>
              </div>
            `).join('')}
          </div>
          <div class="cat-content">
            <div class="filter-tabs">
              <button class="filter-tab active" data-sort="default">综合</button>
              <button class="filter-tab" data-sort="price-asc">价格↑</button>
              <button class="filter-tab" data-sort="price-desc">价格↓</button>
              <button class="filter-tab" data-sort="newest">最新</button>
            </div>
            <div class="product-grid" id="catProducts">
              ${filtered.map(p => `
                <a href="#/product/${p._id}" class="product-card">
                  <div class="img-wrap">
                    <img src="${p.image || p.images?.[0] || '/placeholder.png'}" alt="${p.name}" loading="lazy">
                  </div>
                  <div class="info">
                    <div class="name">${p.name}</div>
                    <div class="price">${formatPriceRange(p.price)}</div>
                  </div>
                </a>
              `).join('') || '<div class="empty-state" style="grid-column:1/-1"><div class="empty-icon">📦</div><p>该分类暂无商品</p></div>'}
            </div>
          </div>
        </div>
        ${renderBottomNav('category')}
      `;
    }
  };
}

export function mountCategory() {
  // Sidebar click
  document.querySelectorAll('.cat-sidebar-item').forEach(item => {
    item.addEventListener('click', () => {
      const cat = item.dataset.cat;
      window.location.hash = cat === 'all' ? '#/category' : `#/category?cat=${cat}`;
    });
  });
}
