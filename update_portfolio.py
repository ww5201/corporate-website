import paramiko, time

# ===== 1. 上传后端 =====
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\server-v4.js', '/root/backend/server-v4.js')
print("Backend uploaded")

# 重启后端
stdin, stdout, stderr = ssh.exec_command("pkill -f 'node server' 2>/dev/null; sleep 1; cd /root/backend && nohup node server-v4.js > /tmp/server.log 2>&1 &")
time.sleep(3)
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
print(f"Health: {stdout.read().decode().strip()}")

# ===== 2. 修改前端 HTML =====
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 添加轮播 CSS
old_css = '.portfolio-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:24px; }'
new_css = '''/* 案例轮播 */
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
    
    .portfolio-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:24px; }'''

html = html.replace(old_css, new_css)

# 添加轮播 HTML 和 lightbox
old_portfolio = '<div class="portfolio-grid" id="portfolioGrid"></div>'
new_portfolio = '''<!-- 案例轮播 -->
      <div class="portfolio-carousel-wrap reveal">
        <div class="portfolio-carousel" id="portfolioCarousel" style="display:none">
          <button class="carousel-arrow left" onclick="prevSlide()">&#10094;</button>
          <button class="carousel-arrow right" onclick="nextSlide()">&#10095;</button>
          <div id="carouselSlides"></div>
          <div class="carousel-nav" id="carouselNav"></div>
        </div>
      </div>
      <div class="portfolio-grid" id="portfolioGrid"></div>
    
    <!-- Lightbox -->
    <div class="lightbox" id="lightbox" onclick="closeLightbox()">
      <button class="lightbox-close">&times;</button>
      <button class="lightbox-prev" onclick="event.stopPropagation(); prevLightbox()">&#10094;</button>
      <button class="lightbox-next" onclick="event.stopPropagation(); nextLightbox()">&#10095;</button>
      <img class="lightbox-img" id="lightboxImg" src="" onclick="event.stopPropagation()">
      <div class="lightbox-counter" id="lightboxCounter"></div>
    </div>'''

html = html.replace(old_portfolio, new_portfolio)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated")

# 上传前端
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
print("Frontend uploaded")

# nginx reload
ssh.exec_command("nginx -s reload")

ssh.close()
print("Done! Refresh page to see changes")
