/**
 * Bottom Navigation Component
 */
import { auth } from '../auth.js';

export function renderBottomNav(active = 'home') {
  const items = [
    { key: 'home', icon: '🏠', label: '首页', path: '/home' },
    { key: 'category', icon: '📂', label: '分类', path: '/category' },
    { key: 'chat', icon: '💬', label: '联系', path: '/chat' },
    { key: 'orders', icon: '📦', label: '订单', path: '/orders' },
    { key: 'profile', icon: '👤', label: '我的', path: auth.isLoggedIn() ? '/profile' : '/login' },
  ];

  return `
    <nav class="bottom-nav">
      ${items.map(item => `
        <a href="#${item.path}" class="bottom-nav-item ${active === item.key ? 'active' : ''}">
          <span class="nav-icon">${item.icon}</span>
          <span>${item.label}</span>
        </a>
      `).join('')}
    </nav>
  `;
}
