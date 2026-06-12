import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 添加 JS 变量和函数
old_js = "let currentLang = localStorage.getItem('lang') || 'zh';"
new_js = """let currentLang = localStorage.getItem('lang') || 'zh';
    let cases = [];
    let carouselInterval = null;
    let currentSlide = 0;
    let lightboxImages = [];
    let currentLightbox = 0;"""

html = html.replace(old_js, new_js)

# 添加加载案例和轮播函数
old_load = "// ===== 启动 ====="
new_load = """// ===== 启动 =====
    loadCases();"""

html = html.replace(old_load, new_load)

# 在 loadData() 后添加 loadCases 函数
old_func = "async function loadData() {"
new_func = """async function loadCases() {
  try {
    const r = await fetch(API + '/cases');
    cases = await r.json();
    if (cases.length > 0) {
      renderCarousel(cases[0]);
    }
    renderPortfolio();
  } catch (e) {
    console.error('Load cases failed:', e);
  }
}

function renderCarousel(firstCase) {
  const container = document.getElementById('portfolioCarousel');
  const slides = document.getElementById('carouselSlides');
  const nav = document.getElementById('carouselNav');
  if (!firstCase.images || firstCase.images.length === 0) {
    container.style.display = 'none';
    return;
  }
  container.style.display = 'block';
  slides.innerHTML = firstCase.images.map((img, i) => 
    `<div class="carousel-slide ${i === 0 ? 'active' : ''}" onclick="openLightbox('${img}', ${i})">
      <img src="${IMG + img}" alt="案例${i+1}">
    </div>`
  ).join('');
  nav.innerHTML = firstCase.images.map((_, i) => 
    `<button class="carousel-dot ${i === 0 ? 'active' : ''}" onclick="goToSlide(${i})"></button>`
  ).join('');
  startCarousel(firstCase.images.length);
}

function startCarousel(len) {
  if (carouselInterval) clearInterval(carouselInterval);
  carouselInterval = setInterval(() => {
    currentSlide = (currentSlide + 1) % len;
    updateCarousel(len);
  }, 3000);
}

function updateCarousel(len) {
  document.querySelectorAll('.carousel-slide').forEach((s, i) => {
    s.classList.toggle('active', i === currentSlide);
  });
  document.querySelectorAll('.carousel-dot').forEach((d, i) => {
    d.classList.toggle('active', i === currentSlide);
  });
}

function prevSlide() {
  const len = document.querySelectorAll('.carousel-slide').length;
  currentSlide = (currentSlide - 1 + len) % len;
  updateCarousel(len);
  if (carouselInterval) { clearInterval(carouselInterval); startCarousel(len); }
}

function nextSlide() {
  const len = document.querySelectorAll('.carousel-slide').length;
  currentSlide = (currentSlide + 1) % len;
  updateCarousel(len);
  if (carouselInterval) { clearInterval(carouselInterval); startCarousel(len); }
}

function goToSlide(i) {
  const len = document.querySelectorAll('.carousel-slide').length;
  currentSlide = i;
  updateCarousel(len);
  if (carouselInterval) { clearInterval(carouselInterval); startCarousel(len); }
}

function renderPortfolio() {
  const grid = document.getElementById('portfolioGrid');
  if (cases.length <= 1) {
    grid.innerHTML = '';
    return;
  }
  grid.innerHTML = cases.slice(1).map(c => {
    const img = c.images && c.images[0] ? IMG + c.images[0] : '';
    return `<div class="portfolio-item" onclick="openPortfolioLightbox('${c._id}')">
      <img src="${img}" alt="${c.name || '案例'}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 400 250%22%3E%3Crect fill=%22%23f0f0f0%22 width=%22400%22 height=%22250%22/%3E%3Ctext fill=%22%23999%22 x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22%3E 暂无图片%3C/text%3E%3C/svg%3E'">
      <div class="portfolio-overlay">
        <div class="portfolio-title">${c.name || '精选案例'}</div>
        <div class="portfolio-desc">${c.description || ''}</div>
      </div>
    </div>`;
  }).join('');
}

function openPortfolioLightbox(id) {
  const c = cases.find(x => x._id === id);
  if (!c || !c.images || c.images.length === 0) return;
  lightboxImages = c.images.map(img => IMG + img);
  currentLightbox = 0;
  showLightbox();
}

function openLightbox(img, idx) {
  const c = cases[0];
  if (!c || !c.images) return;
  lightboxImages = c.images.map(i => IMG + i);
  currentLightbox = idx;
  showLightbox();
}

function showLightbox() {
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightboxImg');
  const counter = document.getElementById('lightboxCounter');
  img.src = lightboxImages[currentLightbox];
  counter.textContent = `${currentLightbox + 1} / ${lightboxImages.length}`;
  lb.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  lb.classList.remove('active');
  document.body.style.overflow = '';
}

function prevLightbox() {
  currentLightbox = (currentLightbox - 1 + lightboxImages.length) % lightboxImages.length;
  showLightbox();
}

function nextLightbox() {
  currentLightbox = (currentLightbox + 1) % lightboxImages.length;
  showLightbox();
}

document.addEventListener('keydown', (e) => {
  const lb = document.getElementById('lightbox');
  if (!lb.classList.contains('active')) return;
  if (e.key === 'ArrowLeft') prevLightbox();
  if (e.key === 'ArrowRight') nextLightbox();
  if (e.key === 'Escape') closeLightbox();
});

async function loadData() {"""

html = html.replace(old_func, new_func)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("JS added")

# 上传
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()
ssh.exec_command("nginx -s reload")
ssh.close()
print("Uploaded!")
