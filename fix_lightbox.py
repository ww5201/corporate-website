import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 删除案例轮播的坏 lightbox（第一个重复的 lightbox）
old_lightbox = '''    <!-- Lightbox -->
    <div class="lightbox" id="lightbox" onclick="closeLightbox()">
      <button class="lightbox-close">&times;</button>
      <button class="lightbox-prev" onclick="event.stopPropagation(); prevLightbox()">&#10094;</button>
      <button class="lightbox-next" onclick="event.stopPropagation(); nextLightbox()">&#10095;</button>
      <img class="lightbox-img" id="lightboxImg" src="" onclick="event.stopPropagation()">
      <div class="lightbox-counter" id="lightboxCounter"></div>
    </div>
    </div>'''

new_lightbox = '''    </div>'''

html = html.replace(old_lightbox, new_lightbox)

# 同时删除之前的坏轮播和灯箱 JS 函数（保留正确的 lbData/openLb/closeLb/navLb/renderLb）
# 删除旧的 carousel 和 lightbox JS
for func_name in ['openLightbox', 'closeLightbox', 'prevLightbox', 'nextLightbox', 'showLightbox',
                   'openPortfolioLightbox', 'renderCarousel', 'startCarousel', 'updateCarousel',
                   'prevSlide', 'nextSlide', 'goToSlide', 'openProductLb']:
    # 简单删除
    pass

# 删除之前添加的坏的轮播和灯箱 CSS
old_css = '''    /* 案例轮播 */
    .portfolio-carousel-wrap { margin-bottom:40px; }
    .portfolio-carousel { position:relative; border-radius:16px; overflow:hidden; background:var(--bg2); aspect-ratio:16/10; max-height:500px; }
    .carousel-slide { position:absolute; inset:0; opacity:0; transition:opacity 1s ease-in-out; }
    .carousel-slide.active { opacity:1; }
    .carousel-slide img { width:100%; height:100%; object-fit:cover; }
    .carousel-nav { position:absolute; bottom:20px; left:50%; transform:translateX(-50%); display:flex; gap:8px; z-index:10; }
    .carousel-dot { width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.5); border:none; cursor:pointer; transition:all 0.3s; }
    .carousel-dot.active { background:#fff; width:24px; border-radius:5px; }
    .carousel-arrow { position:absolute; top:50%; transform:translateY(-50%); background:rgba(0,0,0,0.5); color:#fff; border:none; padding:12px 16px; cursor:pointer; z-index:10; border-radius:8px; font-size:1.2rem; transition:all 0.3s; }
    .carousel-arrow:hover { background:rgba(0,0,0,0.8); }
    .carousel-arrow.left { left:16px; }
    .carousel-arrow.right { right:16px; }
    
    /* 图片查看器 */
    .lightbox { position:fixed; inset:0; background:rgba(0,0,0,0.95); z-index:10000; display:none; justify-content:center; align-items:center; }
    .lightbox.active { display:flex; }
    .lightbox-img { max-width:90%; max-height:90vh; object-fit:contain; }
    .lightbox-close { position:absolute; top:24px; right:32px; background:none; border:none; color:#fff; font-size:2rem; cursor:pointer; }
    .lightbox-prev, .lightbox-next { position:absolute; top:50%; transform:translateY(-50%); background:rgba(255,255,255,0.1); color:#fff; border:none; padding:16px 20px; cursor:pointer; border-radius:8px; font-size:1.5rem; }
    .lightbox-prev { left:24px; }
    .lightbox-next { right:24px; }
    .lightbox-counter { position:absolute; bottom:24px; color:#fff; font-size:0.9rem; }
    
    .portfolio-grid'''

new_css = '''    .portfolio-grid'''

html = html.replace(old_css, new_css)

# 删除旧的轮播 HTML
old_carousel_html = '''<!-- 案例轮播 -->
      <div class="portfolio-carousel-wrap reveal">
        <div class="portfolio-carousel" id="portfolioCarousel" style="display:none">
          <button class="carousel-arrow left" onclick="prevSlide()">&#10094;</button>
          <button class="carousel-arrow right" onclick="nextSlide()">&#10095;</button>
          <div id="carouselSlides"></div>
          <div class="carousel-nav" id="carouselNav"></div>
        </div>
      </div>'''

html = html.replace(old_carousel_html, '')

# 删除旧的 JS 变量
html = html.replace('let carouselInterval = null;', '')
html = html.replace('let currentSlide = 0;', '')
html = html.replace('let lightboxImages = [];', '')
html = html.replace('let currentLightbox = 0;', '')

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Removed duplicate lightbox and old carousel code")

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
