import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

def run(cmd, label=""):
    if label:
        print(f"\n=== {label} ===")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print(out[:5000])
    if err: print("ERR:", err[:1000])
    return out, err

# ============================================================
# 1. NEW HOMEPAGE - Mobile-first design matching shop.html
# ============================================================
print("=" * 60)
print("STEP 1: Create new homepage (index.html)")
print("=" * 60)

new_index_html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>卓翌定制 | 高端家居定制</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #1677ff;
      --primary-light: #4096ff;
      --primary-bg: #e6f4ff;
      --gold: #c9a96e;
      --gold-light: #e8d5b0;
      --dark: #1a1a1a;
      --text: #333;
      --text-2: #666;
      --text-3: #999;
      --bg: #f5f5f5;
      --card: #fff;
      --border: #f0f0f0;
      --radius: 12px;
      --danger: #ff4d4f;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding-bottom: 70px;
    }
    a { color: inherit; text-decoration: none; }

    /* ===== Top Bar ===== */
    .top-bar {
      position: sticky; top: 0; z-index: 100;
      background: rgba(255,255,255,0.95);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 8px 12px;
      display: flex; align-items: center; gap: 10px;
      border-bottom: 1px solid var(--border);
    }
    .logo {
      font-size: 18px; font-weight: 900; white-space: nowrap;
      color: var(--dark);
    }
    .logo span { color: var(--gold); }
    .search-box {
      flex: 1; display: flex; align-items: center;
      background: var(--bg); border-radius: 20px;
      padding: 6px 14px; gap: 6px;
    }
    .search-box input {
      flex: 1; border: none; background: transparent;
      font-size: 14px; outline: none; font-family: inherit;
    }
    .search-icon { font-size: 16px; color: var(--text-3); }
    .top-actions { display: flex; gap: 4px; }
    .top-btn {
      width: 36px; height: 36px; border: none; background: transparent;
      font-size: 20px; cursor: pointer; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      transition: background 0.2s;
    }
    .top-btn:active { background: var(--bg); }

    /* ===== Hero Banner ===== */
    .hero-banner {
      margin: 12px;
      border-radius: 16px;
      overflow: hidden;
      position: relative;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 180px;
    }
    .hero-content {
      padding: 28px 24px;
      color: #fff;
      position: relative;
      z-index: 2;
    }
    .hero-badge {
      display: inline-block;
      background: rgba(201,169,110,0.2);
      color: var(--gold);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 12px;
      border: 1px solid rgba(201,169,110,0.3);
    }
    .hero-title {
      font-size: 24px;
      font-weight: 900;
      line-height: 1.3;
      margin-bottom: 8px;
    }
    .hero-title em {
      font-style: normal;
      color: var(--gold);
    }
    .hero-desc {
      font-size: 13px;
      color: rgba(255,255,255,0.7);
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .hero-cta {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(135deg, var(--gold) 0%, #d4b577 100%);
      color: #1a1a1a;
      padding: 10px 24px;
      border-radius: 24px;
      font-size: 14px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .hero-cta:active { transform: scale(0.97); }
    .hero-decor {
      position: absolute;
      right: -20px; top: -20px;
      width: 160px; height: 160px;
      background: radial-gradient(circle, rgba(201,169,110,0.15) 0%, transparent 70%);
      border-radius: 50%;
    }
    .hero-decor2 {
      position: absolute;
      right: 40px; bottom: -30px;
      width: 100px; height: 100px;
      background: radial-gradient(circle, rgba(22,119,255,0.1) 0%, transparent 70%);
      border-radius: 50%;
    }

    /* ===== Quick Entry ===== */
    .quick-entry {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      padding: 16px 12px 8px;
    }
    .quick-item {
      display: flex; flex-direction: column; align-items: center;
      gap: 6px; cursor: pointer;
      padding: 10px 4px;
      border-radius: 12px;
      transition: background 0.2s;
    }
    .quick-item:active { background: var(--primary-bg); }
    .quick-icon {
      width: 48px; height: 48px;
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px;
      background: linear-gradient(135deg, var(--primary-bg) 0%, #dbeafe 100%);
    }
    .quick-icon.gold { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); }
    .quick-icon.green { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); }
    .quick-icon.purple { background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); }
    .quick-item span {
      font-size: 12px; color: var(--text-2); font-weight: 500;
    }

    /* ===== Stats Bar ===== */
    .stats-bar {
      display: flex;
      margin: 8px 12px 16px;
      background: #fff;
      border-radius: 12px;
      padding: 14px 8px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .stat-item {
      flex: 1; text-align: center;
      position: relative;
    }
    .stat-item:not(:last-child)::after {
      content: '';
      position: absolute;
      right: 0; top: 20%; height: 60%;
      width: 1px;
      background: var(--border);
    }
    .stat-num {
      font-size: 20px; font-weight: 900; color: var(--primary);
    }
    .stat-label {
      font-size: 11px; color: var(--text-3); margin-top: 2px;
    }

    /* ===== Section Header ===== */
    .section-hdr {
      display: flex; align-items: center; justify-content: space-between;
      padding: 16px 12px 10px;
    }
    .section-hdr h3 {
      font-size: 17px; font-weight: 800;
    }
    .section-hdr a {
      font-size: 13px; color: var(--primary); font-weight: 500;
    }

    /* ===== Service Cards (horizontal scroll) ===== */
    .svc-scroll {
      display: flex; gap: 10px;
      padding: 0 12px 12px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .svc-scroll::-webkit-scrollbar { display: none; }
    .svc-card {
      flex-shrink: 0;
      width: 140px;
      background: #fff;
      border-radius: 14px;
      padding: 16px 14px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      transition: transform 0.2s;
    }
    .svc-card:active { transform: scale(0.97); }
    .svc-icon {
      width: 40px; height: 40px;
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px;
      margin-bottom: 10px;
    }
    .svc-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
    .svc-card p { font-size: 11px; color: var(--text-3); line-height: 1.4; }

    /* ===== Product Waterfall ===== */
    .product-waterfall {
      display: flex; gap: 8px;
      padding: 0 12px;
    }
    .waterfall-col { flex: 1; display: flex; flex-direction: column; gap: 8px; }
    .p-card {
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 1px 6px rgba(0,0,0,0.06);
      transition: transform 0.2s;
      cursor: pointer;
    }
    .p-card:active { transform: scale(0.98); }
    .p-card-img {
      position: relative;
      width: 100%;
      aspect-ratio: 1;
      background: #f0f0f0;
      overflow: hidden;
    }
    .p-card-img img {
      width: 100%; height: 100%;
      object-fit: cover;
    }
    .p-card-img .badge {
      position: absolute; top: 8px; left: 8px;
      background: rgba(0,0,0,0.5);
      color: #fff;
      font-size: 10px;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .p-card-body { padding: 10px; }
    .p-card-title {
      font-size: 13px; font-weight: 600; line-height: 1.4;
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
      overflow: hidden;
      margin-bottom: 6px;
    }
    .p-card-title .tag {
      display: inline-block;
      background: var(--primary-bg);
      color: var(--primary);
      font-size: 10px;
      padding: 1px 6px;
      border-radius: 3px;
      margin-right: 4px;
      font-weight: 500;
    }
    .p-card-price {
      display: flex; align-items: baseline; gap: 2px;
    }
    .p-card-price .cur { font-size: 12px; color: var(--danger); font-weight: 700; }
    .p-card-price .num { font-size: 18px; color: var(--danger); font-weight: 900; }
    .p-card-price .orig {
      font-size: 11px; color: var(--text-3);
      text-decoration: line-through; margin-left: 6px;
    }
    .p-card-sales {
      font-size: 11px; color: var(--text-3); margin-top: 4px;
    }
    .p-card-action {
      margin-top: 8px;
    }
    .p-card-action button {
      width: 100%;
      padding: 7px;
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
    }
    .p-card-action button:active { opacity: 0.85; }

    /* ===== Contact Section ===== */
    .contact-section {
      margin: 16px 12px;
      background: #fff;
      border-radius: 16px;
      padding: 20px 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .contact-section h3 {
      font-size: 17px; font-weight: 800; margin-bottom: 14px;
    }
    .contact-row {
      display: flex; align-items: flex-start; gap: 10px;
      padding: 10px 0;
      border-bottom: 1px solid var(--border);
    }
    .contact-row:last-of-type { border-bottom: none; }
    .contact-icon {
      width: 36px; height: 36px;
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 18px;
      background: var(--primary-bg);
      flex-shrink: 0;
    }
    .contact-label { font-size: 12px; color: var(--text-3); }
    .contact-value { font-size: 14px; font-weight: 500; margin-top: 2px; }
    .contact-form { margin-top: 16px; }
    .contact-form input,
    .contact-form textarea {
      width: 100%;
      padding: 12px 14px;
      border: 1.5px solid var(--border);
      border-radius: 10px;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      background: var(--bg);
      margin-bottom: 10px;
      transition: border-color 0.2s;
    }
    .contact-form input:focus,
    .contact-form textarea:focus { border-color: var(--primary); background: #fff; }
    .contact-form textarea { min-height: 80px; resize: vertical; }
    .contact-form button {
      width: 100%;
      padding: 12px;
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
      color: #fff;
      border: none;
      border-radius: 24px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
    }
    .contact-form button:active { opacity: 0.85; }

    /* ===== Bottom Nav ===== */
    .bottom-nav {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: #fff;
      border-top: 1px solid var(--border);
      display: flex; z-index: 100;
      padding-bottom: env(safe-area-inset-bottom, 0);
    }
    .nav-item {
      flex: 1; display: flex; flex-direction: column;
      align-items: center; padding: 6px 0 8px;
      text-decoration: none; cursor: pointer;
    }
    .nav-icon { font-size: 22px; margin-bottom: 2px; }
    .nav-label { font-size: 10px; color: var(--text-3); }
    .nav-item.active .nav-label { color: var(--primary); font-weight: 600; }

    /* ===== Loading / Empty ===== */
    .loading-box {
      text-align: center; padding: 40px;
      color: var(--text-3); font-size: 14px;
    }
    .spinner {
      width: 28px; height: 28px;
      border: 3px solid #eee;
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      margin: 0 auto 10px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .empty-box {
      text-align: center; padding: 60px 20px; color: var(--text-3);
    }
    .empty-box .icon { font-size: 48px; margin-bottom: 12px; }

    /* ===== Toast ===== */
    .toast {
      position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0,0,0,0.75);
      color: #fff; padding: 10px 24px;
      border-radius: 8px; font-size: 14px;
      z-index: 999; opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
    }
    .toast.show { opacity: 1; }

    /* ===== Detail Overlay ===== */
    .detail-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.5);
      z-index: 200;
      display: none;
      align-items: flex-end;
    }
    .detail-overlay.show { display: flex; }
    .detail-sheet {
      width: 100%;
      max-height: 85vh;
      background: #fff;
      border-radius: 20px 20px 0 0;
      overflow-y: auto;
      position: relative;
      animation: slideUp 0.3s ease;
    }
    @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
    .detail-close {
      position: sticky; top: 12px; left: calc(100% - 44px);
      width: 36px; height: 36px;
      border-radius: 50%; border: none;
      background: rgba(0,0,0,0.06);
      font-size: 22px; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      z-index: 10;
    }
    .detail-imgs {
      position: relative;
      width: 100%; aspect-ratio: 1;
      background: #f5f5f5;
      overflow: hidden;
    }
    .detail-imgs img {
      width: 100%; height: 100%; object-fit: cover;
    }
    .detail-img-nav {
      position: absolute; top: 50%; transform: translateY(-50%);
      width: 36px; height: 36px;
      border-radius: 50%; border: none;
      background: rgba(255,255,255,0.8);
      font-size: 20px; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
    }
    .detail-img-nav.prev { left: 10px; }
    .detail-img-nav.next { right: 10px; }
    .detail-dots {
      position: absolute; bottom: 10px; left: 50%;
      transform: translateX(-50%);
      display: flex; gap: 6px;
    }
    .detail-dots span {
      width: 6px; height: 6px; border-radius: 50%;
      background: rgba(255,255,255,0.5);
      cursor: pointer;
    }
    .detail-dots span.active { background: #fff; width: 16px; border-radius: 3px; }
    .detail-info { padding: 16px 20px 100px; }
    .detail-name { font-size: 18px; font-weight: 800; margin-bottom: 8px; }
    .detail-price {
      font-size: 24px; font-weight: 900; color: var(--danger);
      margin-bottom: 8px;
    }
    .detail-price small { font-size: 14px; }
    .detail-desc {
      font-size: 14px; color: var(--text-2); line-height: 1.6;
      margin-bottom: 16px;
    }
    .detail-actions {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: #fff; padding: 12px 16px;
      display: flex; gap: 10px;
      border-top: 1px solid var(--border);
      z-index: 210;
    }
    .detail-actions button {
      flex: 1; padding: 12px;
      border-radius: 24px; border: none;
      font-size: 15px; font-weight: 700;
      cursor: pointer; font-family: inherit;
    }
    .btn-chat {
      background: var(--primary-bg); color: var(--primary);
    }
    .btn-buy {
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
      color: #fff;
    }

    /* ===== Language Switcher ===== */
    .lang-float {
      position: fixed;
      bottom: 80px; right: 12px;
      z-index: 90;
    }
    .lang-float-btn {
      width: 44px; height: 44px;
      border-radius: 50%;
      background: #fff;
      border: none;
      box-shadow: 0 2px 12px rgba(0,0,0,0.15);
      font-size: 22px;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
    }
    .lang-float-menu {
      position: absolute;
      bottom: 52px; right: 0;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      padding: 6px 0;
      min-width: 130px;
      display: none;
    }
    .lang-float-menu.show { display: block; }
    .lang-opt {
      padding: 8px 16px;
      font-size: 13px;
      cursor: pointer;
      display: flex; align-items: center; gap: 8px;
    }
    .lang-opt:active { background: var(--bg); }
    .lang-opt.active { color: var(--primary); font-weight: 600; }

    @media (min-width: 768px) {
      .quick-entry { grid-template-columns: repeat(8, 1fr); }
      .hero-banner { margin: 16px; min-height: 220px; }
      .hero-title { font-size: 28px; }
    }
  </style>
</head>
<body>

  <!-- Top Bar -->
  <div class="top-bar">
    <div class="logo">卓翌<span>定制</span></div>
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="搜索商品、品类..." oninput="doSearch()">
    </div>
    <div class="top-actions">
      <button class="top-btn" onclick="location.href='/login.html'" title="我的">👤</button>
    </div>
  </div>

  <!-- Hero Banner -->
  <div class="hero-banner">
    <div class="hero-content">
      <div class="hero-badge">✨ 高端定制 · 匠心品质</div>
      <div class="hero-title">追求卓越<br><em>定义奢华</em></div>
      <div class="hero-desc">二十年行业沉淀，为高端客户打造极致家居体验</div>
      <a href="/shop.html" class="hero-cta">🛍️ 浏览商品 →</a>
    </div>
    <div class="hero-decor"></div>
    <div class="hero-decor2"></div>
  </div>

  <!-- Stats Bar -->
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-num">20+</div>
      <div class="stat-label">行业经验</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">500+</div>
      <div class="stat-label">成功案例</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">98%</div>
      <div class="stat-label">满意度</div>
    </div>
  </div>

  <!-- Quick Entry -->
  <div class="quick-entry" id="quickEntry">
    <a class="quick-item" href="/shop.html">
      <div class="quick-icon">🛍️</div>
      <span>全部商品</span>
    </a>
    <a class="quick-item" href="/shop.html">
      <div class="quick-icon gold">👔</div>
      <span>整体衣柜</span>
    </a>
    <a class="quick-item" href="/shop.html">
      <div class="quick-icon green">🍳</div>
      <span>定制橱柜</span>
    </a>
    <a class="quick-item" href="/payment.html">
      <div class="quick-icon purple">💳</div>
      <span>在线支付</span>
    </a>
  </div>

  <!-- Services -->
  <div class="section-hdr">
    <h3>我们的服务</h3>
    <a href="#contact">了解更多 ›</a>
  </div>
  <div class="svc-scroll">
    <div class="svc-card">
      <div class="svc-icon" style="background:var(--primary-bg)">✦</div>
      <h4>高端定制</h4>
      <p>量身定制专属方案，满足独特需求</p>
    </div>
    <div class="svc-card">
      <div class="svc-icon" style="background:#fef3c7">✦</div>
      <h4>品质管理</h4>
      <p>严格质量管控，每处细节完美</p>
    </div>
    <div class="svc-card">
      <div class="svc-icon" style="background:#d1fae5">✦</div>
      <h4>专属顾问</h4>
      <p>一对一专业顾问，全程陪伴</p>
    </div>
    <div class="svc-card">
      <div class="svc-icon" style="background:#ede9fe">✦</div>
      <h4>售后保障</h4>
      <p>完善售后体系，无后顾之忧</p>
    </div>
  </div>

  <!-- Products -->
  <div class="section-hdr" id="productsSection">
    <h3>精选推荐</h3>
    <a href="/shop.html">查看全部 ›</a>
  </div>
  <div class="product-waterfall" id="waterfall">
    <div class="waterfall-col" id="colL"></div>
    <div class="waterfall-col" id="colR"></div>
  </div>
  <div class="loading-box" id="loadingBox">
    <div class="spinner"></div>加载中...
  </div>

  <!-- Contact -->
  <div id="contact" class="contact-section">
    <h3>联系我们</h3>
    <div class="contact-row">
      <div class="contact-icon">📍</div>
      <div>
        <div class="contact-label">地址</div>
        <div class="contact-value">广西壮族自治区南宁市江南区那洪大道留村路 1-2 号</div>
      </div>
    </div>
    <div class="contact-row">
      <div class="contact-icon">📞</div>
      <div>
        <div class="contact-label">电话</div>
        <div class="contact-value">18977122166</div>
      </div>
    </div>
    <div class="contact-row">
      <div class="contact-icon">📧</div>
      <div>
        <div class="contact-label">邮箱</div>
        <div class="contact-value">2841327487@qq.com</div>
      </div>
    </div>
    <div class="contact-form">
      <input type="text" id="cfName" placeholder="您的姓名">
      <input type="tel" id="cfPhone" placeholder="联系电话">
      <textarea id="cfMsg" placeholder="请输入您的需求或留言..."></textarea>
      <button onclick="submitContact()">发送留言</button>
    </div>
  </div>

  <!-- Bottom Nav -->
  <div class="bottom-nav">
    <a class="nav-item active" href="/">
      <span class="nav-icon">🏠</span>
      <span class="nav-label">首页</span>
    </a>
    <a class="nav-item" href="/shop.html">
      <span class="nav-icon">🛍️</span>
      <span class="nav-label">商品</span>
    </a>
    <a class="nav-item" href="/payment.html">
      <span class="nav-icon">💳</span>
      <span class="nav-label">支付</span>
    </a>
    <a class="nav-item" href="/login.html">
      <span class="nav-icon">👤</span>
      <span class="nav-label">我的</span>
    </a>
  </div>

  <!-- Language Switcher -->
  <div class="lang-float">
    <button class="lang-float-btn" onclick="toggleLangMenu()">🌐</button>
    <div class="lang-float-menu" id="langMenu">
      <div class="lang-opt active" onclick="setLang('zh')">🇨🇳 中文</div>
      <div class="lang-opt" onclick="setLang('en')">🇺🇸 English</div>
      <div class="lang-opt" onclick="setLang('ja')">🇯🇵 日本語</div>
      <div class="lang-opt" onclick="setLang('ko')">🇰🇷 한국어</div>
      <div class="lang-opt" onclick="setLang('th')">🇹🇭 ไทย</div>
      <div class="lang-opt" onclick="setLang('vi')">🇻🇳 Tiếng Việt</div>
    </div>
  </div>

  <!-- Detail Overlay -->
  <div class="detail-overlay" id="detailOverlay" onclick="if(event.target===this)closeDetail()">
    <div class="detail-sheet" id="detailSheet">
      <button class="detail-close" onclick="closeDetail()">&times;</button>
      <div class="detail-imgs" id="detailImgs"></div>
      <div class="detail-info" id="detailInfo"></div>
    </div>
  </div>

  <!-- Toast -->
  <div class="toast" id="toast"></div>

<script>
const API = '';
let allProducts = [];
let currentImgIdx = 0;
let currentImages = [];

// ===== Load Products =====
async function loadProducts() {
  try {
    const res = await fetch(API + '/api/products');
    const data = await res.json();
    allProducts = Array.isArray(data) ? data : (data.data || []);
    document.getElementById('loadingBox').style.display = 'none';
    renderWaterfall(allProducts.slice(0, 10));
  } catch(e) {
    document.getElementById('loadingBox').innerHTML =
      '<div class="empty-box"><div class="icon">😵</div><p>加载失败，请下拉刷新</p></div>';
  }
}

// ===== Search =====
function doSearch() {
  const q = document.getElementById('searchInput').value.trim().toLowerCase();
  if (!q) { renderWaterfall(allProducts.slice(0, 10)); return; }
  const filtered = allProducts.filter(p =>
    (p.name || '').toLowerCase().includes(q) ||
    (p.description || '').toLowerCase().includes(q) ||
    (p.category || '').toLowerCase().includes(q)
  );
  renderWaterfall(filtered);
}

// ===== Render Waterfall =====
function renderWaterfall(products) {
  const colL = document.getElementById('colL');
  const colR = document.getElementById('colR');
  colL.innerHTML = '';
  colR.innerHTML = '';

  if (!products.length) {
    colL.innerHTML = '<div class="empty-box" style="width:100%"><div class="icon">📭</div><p>暂无商品</p></div>';
    return;
  }

  products.forEach((p, i) => {
    const idx = allProducts.indexOf(p);
    const origPrice = Math.round((p.price||0) * (1.3 + Math.random()*0.5));
    const card = document.createElement('div');
    card.className = 'p-card';
    card.onclick = () => openDetail(idx);
    card.innerHTML = `
      <div class="p-card-img">
        ${p.image || (p.images && p.images.length)
          ? `<img src="${p.image || p.images[0]}" alt="${p.name}" loading="lazy">`
          : '<div style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;font-size:40px;color:#ddd">📦</div>'}
        ${p.category ? `<span class="badge">${p.category}</span>` : ''}
      </div>
      <div class="p-card-body">
        <div class="p-card-title">
          ${p.category ? `<span class="tag">${p.category}</span>` : ''}
          ${p.name || '未命名商品'}
        </div>
        <div class="p-card-price">
          <span class="cur">¥</span>
          <span class="num">${(p.price||0).toLocaleString()}</span>
          <span class="orig">¥${origPrice.toLocaleString()}</span>
        </div>
        <div class="p-card-sales">已售 ${Math.floor(Math.random()*200+10)}件</div>
        <div class="p-card-action">
          <button onclick="event.stopPropagation();goPay(${idx})">立即下单</button>
        </div>
      </div>`;
    if (i % 2 === 0) colL.appendChild(card);
    else colR.appendChild(card);
  });
}

// ===== Product Detail =====
function openDetail(idx) {
  const p = allProducts[idx];
  if (!p) return;
  currentImages = (p.images && p.images.length) ? p.images : (p.image ? [p.image] : []);
  currentImgIdx = 0;

  const imgsEl = document.getElementById('detailImgs');
  if (currentImages.length) {
    imgsEl.innerHTML = `
      <img id="dImg" src="${currentImages[0]}" alt="${p.name}">
      ${currentImages.length > 1 ? `
        <button class="detail-img-nav prev" onclick="navDImg(-1)">&lsaquo;</button>
        <button class="detail-img-nav next" onclick="navDImg(1)">&rsaquo;</button>
        <div class="detail-dots">${currentImages.map((_,i) => `<span class="${i===0?'active':''}" onclick="goDImg(${i})"></span>`).join('')}</div>
      ` : ''}`;
  } else {
    imgsEl.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;font-size:80px;color:#ddd">📦</div>';
  }

  const origPrice = Math.round((p.price||0) * (1.3 + Math.random()*0.5));
  document.getElementById('detailInfo').innerHTML = `
    <div class="detail-name">${p.name || '未命名商品'}</div>
    <div class="detail-price"><small>¥</small>${(p.price||0).toLocaleString()} <span style="font-size:14px;color:var(--text-3);text-decoration:line-through;font-weight:400">¥${origPrice.toLocaleString()}</span></div>
    <div class="detail-desc">${p.description || '暂无详细描述'}</div>
    <div class="detail-actions">
      <button class="btn-chat" onclick="window.open('/payment.html?product=' + encodeURIComponent('${p.name||''}'),'_blank')">💬 咨询客服</button>
      <button class="btn-buy" onclick="goPay(${idx})">🛒 立即下单</button>
    </div>`;

  document.getElementById('detailOverlay').classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeDetail() {
  document.getElementById('detailOverlay').classList.remove('show');
  document.body.style.overflow = '';
}

function navDImg(dir) {
  currentImgIdx = (currentImgIdx + dir + currentImages.length) % currentImages.length;
  document.getElementById('dImg').src = currentImages[currentImgIdx];
  updateDots();
}
function goDImg(i) { currentImgIdx = i; document.getElementById('dImg').src = currentImages[i]; updateDots(); }
function updateDots() {
  document.querySelectorAll('.detail-dots span').forEach((d,i) => d.classList.toggle('active', i===currentImgIdx));
}

// ===== Go Pay =====
function goPay(idx) {
  const p = allProducts[idx];
  if (!p) return;
  window.open('/payment.html?product=' + encodeURIComponent(p.name) + '&price=' + (p.price||0), '_blank');
}

// ===== Contact Form =====
async function submitContact() {
  const name = document.getElementById('cfName').value.trim();
  const phone = document.getElementById('cfPhone').value.trim();
  const msg = document.getElementById('cfMsg').value.trim();
  if (!name || !phone) return showToast('请填写姓名和电话');

  try {
    const res = await fetch(API + '/api/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, phone, content: msg || name + ' 提交了留言' }),
    });
    if (res.ok) {
      showToast('留言已提交，我们会尽快联系您！');
      document.getElementById('cfName').value = '';
      document.getElementById('cfPhone').value = '';
      document.getElementById('cfMsg').value = '';
    } else {
      showToast('提交失败，请稍后重试');
    }
  } catch(e) {
    showToast('网络错误');
  }
}

// ===== Language =====
function toggleLangMenu() {
  document.getElementById('langMenu').classList.toggle('show');
}
function setLang(lang) {
  document.getElementById('langMenu').classList.remove('show');
  showToast('语言已切换');
  // Store preference
  localStorage.setItem('lang', lang);
}
document.addEventListener('click', (e) => {
  if (!e.target.closest('.lang-float')) {
    document.getElementById('langMenu').classList.remove('show');
  }
});

// ===== Toast =====
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

// ===== Init =====
loadProducts();
</script>
</body>
</html>'''

# Write new index.html to frontend
sftp = client.open_sftp()
with sftp.file('/var/www/frontend/index.html', 'w') as f:
    f.write(new_index_html)
print("✅ New index.html written to /var/www/frontend/")
sftp.close()

# ============================================================
# 2. FIX LOGIN SYSTEM
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Fix login.html deployment")
print("=" * 60)

# Copy login.html to frontend
run("cp /root/backend/login.html /var/www/frontend/login.html", "Copy login.html to frontend")

# Add login.html route to server-v4.js (before the SPA catch-all)
# Check current state
out, _ = run("grep -n 'login.html' /root/backend/server-v4.js", "Check existing login routes")

if 'login.html' not in out:
    # Add login.html route before the SPA catch-all
    patch_cmd = r"""
python3 -c "
import re
with open('/root/backend/server-v4.js', 'r') as f:
    content = f.read()

# Add login.html route before payment.html route
login_route = '''app.get(\"/login.html\", (req, res) => {
  const loginPath = path.join(__dirname, \"login.html\");
  if (fs.existsSync(loginPath)) return res.sendFile(loginPath);
  res.sendFile(path.join(frontendDir, \"index.html\"));
});
'''

# Insert before shop.html route
if '/login.html' not in content:
    content = content.replace(
        'app.get(\"/shop.html\"',
        login_route + 'app.get(\"/shop.html\"'
    )

with open('/root/backend/server-v4.js', 'w') as f:
    f.write(content)
print('login.html route added')
"
"""
    run(patch_cmd, "Add login.html route to server-v4.js")
else:
    print("login.html route already exists")

# Also add logout route to auth.js if missing
out, _ = run("grep -n 'logout' /root/backend/routes/auth.js", "Check auth logout route")
if 'logout' not in out:
    logout_patch = r"""
python3 -c "
with open('/root/backend/routes/auth.js', 'r') as f:
    content = f.read()

# Add logout route before module.exports
logout_route = '''
// Logout (client just clears token, this is for completeness)
router.post('/logout', (req, res) => {
  res.json({ success: true, message: '已退出登录' });
});

'''

if '/logout' not in content:
    content = content.replace('module.exports = router;', logout_route + 'module.exports = router;')

with open('/root/backend/routes/auth.js', 'w') as f:
    f.write(content)
print('logout route added')
"
"""
    run(logout_patch, "Add logout route to auth.js")
else:
    print("logout route already exists")

# ============================================================
# 3. UPDATE NGINX
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Update nginx config")
print("=" * 60)

# Add login.html to site.conf nginx
nginx_patch = r"""
python3 -c "
with open('/etc/nginx/conf.d/site.conf', 'r') as f:
    content = f.read()

if 'login.html' not in content:
    # Add login.html location block before payment.html
    login_block = '''    location = /login.html {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
'''
    content = content.replace(
        '    location = /payment.html',
        login_block + '    location = /payment.html'
    )
    with open('/etc/nginx/conf.d/site.conf', 'w') as f:
        f.write(content)
    print('login.html added to nginx site.conf')
else:
    print('login.html already in nginx')
"
"""
run(nginx_patch, "Update nginx config")

# ============================================================
# 4. RESTART & VERIFY
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Restart services and verify")
print("=" * 60)

run("nginx -t 2>&1", "Test nginx config")
run("nginx -s reload 2>&1", "Reload nginx")
run("pm2 restart tokai-backend 2>&1", "Restart backend")
run("sleep 2", "Wait for restart")

# Verify
run("curl -sI http://localhost/ 2>/dev/null | head -5", "Verify homepage")
run("curl -sI http://localhost/shop.html 2>/dev/null | head -5", "Verify shop")
run("curl -sI http://localhost/payment.html 2>/dev/null | head -5", "Verify payment")
run("curl -sI http://localhost/login.html 2>/dev/null | head -5", "Verify login")
run("curl -s http://localhost/api/health 2>/dev/null", "Verify API health")
run("curl -s http://localhost/login.html 2>/dev/null | head -8", "Verify login.html content")
run("curl -s http://localhost/ 2>/dev/null | head -8", "Verify homepage content")

# Check file sizes
run("ls -la /var/www/frontend/", "Frontend files")

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)

client.close()
