// 精致奢华企业官网 - JavaScript

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

// 表单提交处理
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('感谢您的留言！我们会尽快与您联系。');
    contactForm.reset();
  });
}

// 滚动淡入效果
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

console.log('✨ Luxury Corporate Website Initialized');
