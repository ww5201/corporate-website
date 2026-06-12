import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# Read current index.html
f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Save local copy for debugging
with open("D:/tokai/frontend_index_v2.html", "w", encoding="utf-8") as lf:
    lf.write(data)

# 1. Remove the entire shop section (<section id="shop" ...> ... </section>)
import re
data = re.sub(
    r'\s*<section id="shop"[^>]*>.*?</section>',
    '', data, flags=re.DOTALL
)

# 2. Replace with a shop entry banner/CTA section
shop_entry = '''
    <!-- 商品入口 -->
    <section class="shop-entry">
      <a href="/shop.html" target="_blank" class="shop-entry-link">
        <div class="shop-entry-icon">🛍️</div>
        <div class="shop-entry-text">
          <h2>精选商品</h2>
          <p>浏览全部商品，品质生活从这里开始</p>
        </div>
        <div class="shop-entry-arrow">&rarr;</div>
      </a>
    </section>
'''

# Insert before the contact section
data = data.replace(
    '<section id="contact"',
    shop_entry + '\n    <section id="contact"'
)

# 3. Add inline styles for the shop entry
style_tag = """<style>
  .shop-entry {
    padding: 2rem 1rem;
    max-width: 900px;
    margin: 0 auto;
  }
  .shop-entry-link {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
    text-decoration: none;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(26,26,46,0.2);
  }
  .shop-entry-link:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(26,26,46,0.35);
  }
  .shop-entry-icon {
    font-size: 3rem;
    flex-shrink: 0;
  }
  .shop-entry-text h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
    color: #c9a96e;
  }
  .shop-entry-text p {
    font-size: 0.95rem;
    color: #e8d5b0;
    margin: 0;
  }
  .shop-entry-arrow {
    font-size: 2rem;
    color: #c9a96e;
    margin-left: auto;
    transition: transform 0.3s;
  }
  .shop-entry-link:hover .shop-entry-arrow {
    transform: translateX(6px);
  }
  @media (max-width: 600px) {
    .shop-entry-link { padding: 1.5rem; gap: 1rem; }
    .shop-entry-icon { font-size: 2.2rem; }
    .shop-entry-text h2 { font-size: 1.2rem; }
    .shop-entry-text p { font-size: 0.85rem; }
  }
</style>"""

# Insert style before </head>
data = data.replace('</head>', style_tag + '\n</head>')

# Write back
f = s.open("/var/www/frontend/index.html", "w")
f.write(data)
f.close()

# Verify
f = s.open("/var/www/frontend/index.html")
verify = f.read().decode("utf-8", "replace")
f.close()

print("[OK] index.html updated")
print("Shop section removed:", 'id="shop"' not in verify)
print("Shop entry added:", 'shop-entry' in verify)
print("Shop link present:", '/shop.html' in verify)

s.close()
c.close()
