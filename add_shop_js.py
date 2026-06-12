# Add shop section JS: i18n, loading, category filter, mobile nav active state
import re

with open('src/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add shop i18n keys to each language block
shop_i18n = {
    'zh': """
    'nav.shop': '\u5546\u54c1',
    'shop.title': '\u7cbe\u9009\u5546\u54c1',
    'shop.desc': '\u7504\u9009\u597d\u7269\uff0c\u54c1\u8d28\u751f\u6d3b\u4ece\u8fd9\u91cc\u5f00\u59cb',
    'shop.cat.all': '\u5168\u90e8',
    'shop.cat.cabinet': '\u67dc\u7c7b',
    'shop.cat.wardrobe': '\u8863\u67dc',
    'shop.cat.kitchen': '\u6a71\u67dc',
    'shop.cat.custom': '\u5b9a\u5236',
    'shop.inquire': '\u7acb\u5373\u54a8\u8be2',
    'shop.price': '\u8d77',
    'shop.empty': '\u6682\u65e0\u5546\u54c1',""",
    'en': """
    'nav.shop': 'Shop',
    'shop.title': 'Featured Shop',
    'shop.desc': 'Curated picks for a quality life',
    'shop.cat.all': 'All',
    'shop.cat.cabinet': 'Cabinets',
    'shop.cat.wardrobe': 'Wardrobes',
    'shop.cat.kitchen': 'Kitchen',
    'shop.cat.custom': 'Custom',
    'shop.inquire': 'Inquire',
    'shop.price': 'up',
    'shop.empty': 'No items yet',""",
    'ja': """
    'nav.shop': '\u5546\u54c1',
    'shop.title': '\u304a\u3059\u3059\u3081\u5546\u54c1',
    'shop.desc': '\u53b3\u9078\u3055\u308c\u305f\u9038\u54c1\u3067\u4e0a\u8cea\u306a\u751f\u6d3b\u3092',
    'shop.cat.all': '\u5168\u3066',
    'shop.cat.cabinet': '\u30ad\u30e3\u30d3\u30cd\u30c3\u30c8',
    'shop.cat.wardrobe': '\u30ef\u30fc\u30c9\u30ed\u30fc\u30d6',
    'shop.cat.kitchen': '\u30ad\u30c3\u30c1\u30f3',
    'shop.cat.custom': '\u30aa\u30fc\u30c0\u30fc',
    'shop.inquire': '\u304a\u554f\u3044\u5408\u308f\u305b',
    'shop.price': '\uff5e',
    'shop.empty': '\u5546\u54c1\u304c\u3042\u308a\u307e\u305b\u3093',""",
    'ko': """
    'nav.shop': '\uc0c1\uc810',
    'shop.title': '\ucd94\ucc9c \uc0c1\uc810',
    'shop.desc': '\ud488\uc9c8 \uc788\ub294 \uc0b6\uc744 \uc704\ud55c \uc120\ubcc4\ub41c \uc810',
    'shop.cat.all': '\uc804\uccb4',
    'shop.cat.cabinet': '\uc7a5',
    'shop.cat.wardrobe': '\uc6e8\uc774\ub4dc\ub85c\ube0c',
    'shop.cat.kitchen': '\ud0a4\uce5c',
    'shop.cat.custom': '\ub9de\ucda4',
    'shop.inquire': '\ubb38\uc758',
    'shop.price': '\ubd80\ud130',
    'shop.empty': '\uc0c1\ud488\uc774 \uc5c6\uc2b5\ub2c8\ub2e4',""",
    'th': """
    'nav.shop': '\u0e2a\u0e34\u0e19\u0e04\u0e49\u0e32',
    'shop.title': '\u0e2a\u0e34\u0e19\u0e04\u0e49\u0e32\u0e40\u0e14\u0e48\u0e19',
    'shop.desc': '\u0e04\u0e31\u0e14\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e2a\u0e34\u0e19\u0e04\u0e49\u0e32\u0e14\u0e35\u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e0a\u0e35\u0e27\u0e34\u0e15\u0e17\u0e35\u0e48\u0e14\u0e35\u0e01\u0e27\u0e48\u0e32',
    'shop.cat.all': '\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14',
    'shop.cat.cabinet': '\u0e15\u0e39\u0e49',
    'shop.cat.wardrobe': '\u0e15\u0e39\u0e49\u0e40\u0e2a\u0e37\u0e49\u0e2d\u0e1c\u0e49\u0e32',
    'shop.cat.kitchen': '\u0e04\u0e23\u0e31\u0e27\u0e04\u0e31\u0e27',
    'shop.cat.custom': '\u0e1e\u0e34\u0e40\u0e28\u0e29',
    'shop.inquire': '\u0e2a\u0e2d\u0e1a\u0e16\u0e32\u0e21',
    'shop.price': '\u0e40\u0e23\u0e34\u0e48\u0e21',
    'shop.empty': '\u0e44\u0e21\u0e48\u0e21\u0e35\u0e2a\u0e34\u0e19\u0e04\u0e49\u0e32',""",
    'vi': """
    'nav.shop': 'C\u1eeda h\u00e0ng',
    'shop.title': 'S\u1ea3n ph\u1ea9m n\u1ed5i b\u1eadt',
    'shop.desc': ' Tuy\u1ec3n ch\u1ecdn nh\u1eefng s\u1ea3n ph\u1ea9m t\u1ed1t nh\u1ea5t',
    'shop.cat.all': 'T\u1ea5t c\u1ea3',
    'shop.cat.cabinet': 'T\u1ee7',
    'shop.cat.wardrobe': 'T\u1ee7 qu\u1ea7n \u00e1o',
    'shop.cat.kitchen': 'B\u1ebfp',
    'shop.cat.custom': 'T\u00f9y ch\u1ec9nh',
    'shop.inquire': 'Li\u00ean h\u1ec7',
    'shop.price': 't\u1eeb',
    'shop.empty': 'Ch\u01b0a c\u00f3 s\u1ea3n ph\u1ea9m',""",
    'ms': """
    'nav.shop': 'Kedai',
    'shop.title': 'Barang Pilihan',
    'shop.desc': 'Pilihan terbaik untuk hidup berkualiti',
    'shop.cat.all': 'Semua',
    'shop.cat.cabinet': 'Kabinet',
    'shop.cat.wardrobe': 'Almari',
    'shop.cat.kitchen': 'Dapur',
    'shop.cat.custom': 'Tersuai',
    'shop.inquire': 'Tanya',
    'shop.price': 'dari',
    'shop.empty': 'Tiada barang lagi',""",
}

# For each language, insert shop keys after 'nav.contact' line
for lang, shop_keys in shop_i18n.items():
    # Find the nav.contact line for this language block
    # We look for 'nav.contact' within the lang block and add after it
    pattern = r"('nav\.contact':\s*'[^']*'(?:,)?)"
    
    def replacer(m):
        return m.group(1) + shop_keys
    
    # Only replace within the correct language block
    # Find the language block boundaries
    lang_pattern = rf"({lang}:\s*\{{)"
    lang_match = re.search(lang_pattern, content)
    if not lang_match:
        continue
    
    # Find the start of next language block (or end of translations)
    next_lang_match = re.search(r"\n  \w+:\s*\{{", content[lang_match.end():])
    if next_lang_match:
        block_end = lang_match.end() + next_lang_match.start()
    else:
        block_end = content.find("};\n\nconst langLabels")
    
    block = content[lang_match.start():block_end]
    
    # Insert shop keys after nav.contact in this block
    new_block = re.sub(pattern, replacer, block, count=1)
    content = content[:lang_match.start()] + new_block + content[block_end:]

# 2. Add shop loading function and mobile nav active state before the closing of the file
shop_js = r"""

// ========== 商品商城 ==========
let shopProducts = [];
let currentShopCat = 'all';

// 商品分类映射（根据产品名称自动分类）
function getShopCategory(name) {
  const n = (name || '').toLowerCase();
  if (n.includes('\u9c7c\u7f38') || n.includes('666')) return 'cabinet';
  if (n.includes('\u8863\u5e3d') || n.includes('\u8863\u67dc') || n.includes('\u6574\u4f53\u8863\u67dc')) return 'wardrobe';
  if (n.includes('\u6a71\u67dc') || n.includes('\u53a8')) return 'kitchen';
  return 'custom';
}

async function loadShopProducts() {
  const grid = document.getElementById('shopGrid');
  if (!grid) return;
  try {
    const res = await fetch(`${API_BASE}/products`);
    const products = await res.json();
    shopProducts = products.filter(p => !p.status || p.status === 'active');
    renderShopGrid();
  } catch (e) {
    console.error('\u52a0\u8f7d\u5546\u54c1\u5931\u8d25:', e);
    if (grid) grid.innerHTML = `<div class="shop-empty">${translations[currentLang]?.['shop.empty'] || '\u6682\u65e0\u5546\u54c1'}</div>`;
  }
}

function renderShopGrid() {
  const grid = document.getElementById('shopGrid');
  if (!grid) return;
  const t = translations[currentLang] || translations.zh;
  
  let filtered = shopProducts;
  if (currentShopCat !== 'all') {
    filtered = shopProducts.filter(p => getShopCategory(p.name) === currentShopCat);
  }
  
  if (filtered.length === 0) {
    grid.innerHTML = `<div class="shop-empty">${t['shop.empty'] || '\u6682\u65e0\u5546\u54c1'}</div>`;
    return;
  }
  
  grid.innerHTML = filtered.map((p, i) => {
    const img = p.images && p.images.length > 0 ? p.images[0] : null;
    const realIdx = shopProducts.indexOf(p);
    return `
      <div class="shop-card" data-shop-index="${realIdx}">
        <div class="shop-card-image">
          ${img 
            ? `<img src="${img}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=image-placeholder>\u6682\u65e0\u56fe\u7247</div>'">`
            : '<div class="image-placeholder">\u6682\u65e0\u56fe\u7247</div>'}
          ${p.price ? `<span class="shop-card-badge">HOT</span>` : ''}
        </div>
        <div class="shop-card-body">
          <h4>${trProductName(p.name)}</h4>
          <p class="shop-card-desc">${trProductDesc(p.name) || p.description || ''}</p>
          <div class="shop-card-footer">
            ${p.price 
              ? `<span class="shop-card-price">\xa5 ${Number(p.price).toLocaleString()} <small>${t['shop.price'] || '\u8d77'}</small></span>`
              : '<span></span>'}
            <button class="shop-card-btn" data-shop-index="${realIdx}">${t['shop.inquire'] || '\u7acb\u5373\u54a8\u8be2'}</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// 分类筛选
document.addEventListener('click', e => {
  const catBtn = e.target.closest('.shop-cat-btn');
  if (catBtn) {
    currentShopCat = catBtn.dataset.cat;
    document.querySelectorAll('.shop-cat-btn').forEach(b => b.classList.remove('active'));
    catBtn.classList.add('active');
    renderShopGrid();
  }
  
  // 商品卡片点击 -> 打开产品详情弹窗
  const shopCard = e.target.closest('.shop-card');
  const shopBtn = e.target.closest('.shop-card-btn');
  if (shopBtn || shopCard) {
    const idx = parseInt((shopBtn || shopCard).dataset.shopIndex);
    if (!isNaN(idx) && shopProducts[idx]) {
      showProductModal(shopProducts[idx]);
    }
  }
});

// ========== 底部导航高亮 ==========
function updateMobileNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.mobile-nav-inner a');
  let current = '';
  
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top <= 150) {
      current = section.id;
    }
  });
  
  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) {
      link.classList.add('active');
    }
  });
}

window.addEventListener('scroll', updateMobileNav);

// ========== 初始化 ==========
"""

# Replace the existing DOMContentLoaded init to also load shop
old_init = """document.addEventListener('DOMContentLoaded', () => {
  applyLang(currentLang);
  console.log('\u2728 \u5353\u7ffc\u5b9a\u5236\u5b98\u7f51\u5df2\u52a0\u8f7d | API: ' + API_BASE);
});"""

new_init = """document.addEventListener('DOMContentLoaded', () => {
  applyLang(currentLang);
  loadShopProducts();
  updateMobileNav();
  console.log('\u2728 \u5353\u7ffc\u5b9a\u5236\u5b98\u7f51\u5df2\u52a0\u8f7d | API: ' + API_BASE);
});"""

content = content.replace(old_init, new_init)

# Append shop JS before the DOMContentLoaded block
# Find the DOMContentLoaded and insert shop code before it
content = content.replace(
    "// ========== \u521d\u59cb\u5316 ==========\ndocument.addEventListener('DOMContentLoaded'",
    shop_js + "\ndocument.addEventListener('DOMContentLoaded'"
)

# Also make loadProducts called in applyLang also trigger shop re-render
# Add renderShopGrid call in applyLang after loadProducts
content = content.replace(
    "  // \u91cd\u65b0\u52a0\u8f7d\u4ea7\u54c1\uff08\u4ef7\u683c\u6587\u5b57\u9700\u8981\u7ffb\u8bd1\uff09\n  loadProducts();",
    "  // \u91cd\u65b0\u52a0\u8f7d\u4ea7\u54c1\uff08\u4ef7\u683c\u6587\u5b57\u9700\u8981\u7ffb\u8bd1\uff09\n  loadProducts();\n  renderShopGrid();"
)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Shop JS added successfully!')
