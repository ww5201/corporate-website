// 阿卡网络科技 - 企业官网 JavaScript
// 后端 API 地址
const API_BASE = 'http://8.138.218.146:3000/api';

// 导航栏滚动效果
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.style.background = 'rgba(15, 15, 18, 0.98)';
    navbar.style.padding = '1rem 0';
  } else {
    navbar.style.background = 'rgba(15, 15, 18, 0.95)';
    navbar.style.padding = '1.5rem 0';
  }
});

// ========== 联系表单 - 提交到后端 ==========
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = contactForm.querySelector('input[type="text"]').value.trim();
    const email = contactForm.querySelector('input[type="email"]').value.trim();
    const message = contactForm.querySelector('textarea').value.trim();
    
    if (!name || !email || !message) {
      alert('请填写完整信息！');
      return;
    }
    
    const submitBtn = contactForm.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '发送中...';
    submitBtn.disabled = true;
    
    try {
      const response = await fetch(`${API_BASE}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message })
      });
      
      if (response.ok) {
        alert('感谢您的留言！我们会尽快与您联系。');
        contactForm.reset();
      } else {
        alert('发送失败，请稍后重试或直接电话联系我们。');
      }
    } catch (error) {
      console.error('提交失败:', error);
      alert('网络错误，请稍后重试或直接电话联系我们：18977122166');
    } finally {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

// ========== 产品展示 - 从后端动态加载 ==========
async function loadProducts() {
  const productsGrid = document.querySelector('.products-grid');
  if (!productsGrid) return;
  
  try {
    const response = await fetch(`${API_BASE}/products`);
    if (!response.ok) return;
    
    const products = await response.json();
    
    // 如果后端有产品数据，动态渲染
    if (products && products.length > 0) {
      productsGrid.innerHTML = products.map(product => `
        <div class="product-card">
          <div class="product-image" style="${product.image ? `background-image:url(${product.image})` : ''}"></div>
          <div class="product-info">
            <h4>${product.name}</h4>
            <p>${product.description || ''}</p>
            ${product.price ? `<span class="product-price">¥ ${product.price.toLocaleString()} 起</span>` : ''}
            <button class="product-btn" onclick="window.location.href='#contact'">立即咨询</button>
          </div>
        </div>
      `).join('');
    }
  } catch (error) {
    console.log('使用静态产品数据（后端未连接）');
  }
}

// ========== 滚动淡入效果 ==========
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// 观察所有卡片
document.querySelectorAll('.service-card, .portfolio-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// 页面初始化
document.addEventListener('DOMContentLoaded', () => {
  loadProducts();
  console.log('✨ 阿卡网络科技官网已加载 | API: ' + API_BASE);
});
