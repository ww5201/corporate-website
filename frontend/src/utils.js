/**
 * Utility Functions
 */

export function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const now = new Date();
  const diff = now - d;

  if (diff < 60000) return '刚刚';
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
  if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';

  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

export function formatPrice(price) {
  if (price === undefined || price === null) return '面议';
  return '¥' + Number(price).toFixed(2);
}

export function formatPriceRange(price) {
  if (!price) return '面议';
  return '¥' + Number(price).toFixed(0) + '起';
}

export function getInitial(name) {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
}

export function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

export function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 6);
}

export function timeAgo(dateStr) {
  const now = new Date();
  const d = new Date(dateStr);
  const sec = Math.floor((now - d) / 1000);
  if (sec < 60) return '刚刚';
  if (sec < 3600) return Math.floor(sec / 60) + '分钟前';
  if (sec < 86400) return Math.floor(sec / 3600) + '小时前';
  return Math.floor(sec / 86400) + '天前';
}
