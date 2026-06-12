# Append shop section and mobile-nav CSS styles
css_content = r"""
/* ===== 移动端底部导航 ===== */
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: rgba(250, 249, 247, 0.98);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--border-color);
  padding: 6px 0 env(safe-area-inset-bottom, 6px);
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.06);
}
.mobile-nav-inner {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.mobile-nav-inner a {
  flex: 1;
  text-align: center;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.72rem;
  font-weight: 500;
  padding: 6px 2px;
  transition: color 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.mobile-nav-inner a.active,
.mobile-nav-inner a:hover {
  color: var(--accent-gold);
}

@media (max-width: 768px) {
  .mobile-nav {
    display: block;
  }
  body {
    padding-bottom: 60px;
  }
}

/* ===== 商品商城 ===== */
.shop {
  padding: 6rem 0;
  background: var(--bg-secondary);
}
.section-desc {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: 0.5rem;
}
.shop-categories {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin: 2rem 0 2.5rem;
}
.shop-cat-btn {
  padding: 8px 24px;
  border: 1px solid var(--border-color);
  border-radius: 30px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  font-family: inherit;
}
.shop-cat-btn:hover,
.shop-cat-btn.active {
  background: var(--accent-gold);
  color: #fff;
  border-color: var(--accent-gold);
}
.shop-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2rem;
}
.shop-card {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: var(--transition);
  cursor: pointer;
}
.shop-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}
.shop-card-image {
  width: 100%;
  height: 220px;
  overflow: hidden;
  position: relative;
  background: var(--bg-secondary);
}
.shop-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.shop-card:hover .shop-card-image img {
  transform: scale(1.08);
}
.shop-card-image .image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
}
.shop-card-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--accent-gold);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
}
.shop-card-body {
  padding: 1.2rem;
}
.shop-card-body h4 {
  font-size: 1.05rem;
  margin-bottom: 0.4rem;
  color: var(--text-primary);
}
.shop-card-body .shop-card-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.8rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.shop-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.shop-card-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--accent-gold);
}
.shop-card-price small {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-secondary);
}
.shop-card-btn {
  padding: 6px 16px;
  border: 1px solid var(--accent-gold);
  border-radius: 20px;
  background: transparent;
  color: var(--accent-gold);
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  font-family: inherit;
}
.shop-card-btn:hover {
  background: var(--accent-gold);
  color: #fff;
}
.shop-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1rem;
}

@media (max-width: 768px) {
  .shop-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  .shop-card-image {
    height: 160px;
  }
  .shop-card-body {
    padding: 0.8rem;
  }
  .shop-card-body h4 {
    font-size: 0.92rem;
  }
  .shop-card-price {
    font-size: 1rem;
  }
  .shop-categories {
    gap: 8px;
    margin: 1.5rem 0 1.5rem;
  }
  .shop-cat-btn {
    padding: 6px 16px;
    font-size: 0.8rem;
  }
}
"""

with open('src/style.css', 'a', encoding='utf-8') as f:
    f.write(css_content)

print('CSS styles appended successfully!')
