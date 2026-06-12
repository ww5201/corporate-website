/**
 * 卓翌定制 - SPA 主入口
 * 路由: hash-based SPA (#/home, #/product/:id, #/login, #/chat/:id 等)
 */
import { router } from './router.js';
import { auth } from './auth.js';

// 页面导入
import { homePage, mountHome } from './pages/home.js';
import { categoryPage, mountCategory } from './pages/category.js';
import { productPage, mountProduct } from './pages/product.js';
import { loginPage, mountLogin } from './pages/login.js';
import { profilePage, mountProfile } from './pages/profile.js';
import { chatListPage, chatRoomPage, mountChatRoom, mountChatList } from './pages/chat.js';
import { paymentPage, mountPayment } from './pages/payment.js';
import { ordersPage, mountOrders } from './pages/orders.js';
import { flashPage, mountFlash } from './pages/flash.js';
import { privacyPage, mountPrivacy } from './pages/privacy.js';

// ==================== 路由注册 ====================

router.on('/home', () => homePage());
router.on('/category', (p, q) => categoryPage(p, q));
router.on('/product/:id', (params) => productPage(params));
router.on('/login', () => loginPage());
router.on('/profile', () => profilePage());
router.on('/chat', () => chatListPage());
router.on('/chat/:id', (params) => chatRoomPage(params));
router.on('/orders', () => ordersPage());
router.on('/payment/:orderId', (params) => paymentPage(params));
router.on('/flash', () => flashPage());
router.on('/privacy', () => privacyPage());

// ==================== 路由守卫 ====================

router.beforeEach = async (path) => {
  // 需要登录的页面
  const authRequired = ['/profile', '/orders'];
  if (authRequired.includes(path) && !auth.isLoggedIn()) {
    window.location.hash = '#/login';
    return false;
  }
  return true;
};

// 全局挂载函数 - 供各页面 mount 使用
window.__pageMount = (params, query) => {
  const path = router.currentRoute?.path;
  if (!path) return;

  switch (true) {
    case path === '/home':
      mountHome();
      break;
    case path === '/category':
      mountCategory();
      break;
    case path.startsWith('/product/'):
      mountProduct(params);
      break;
    case path === '/login':
      mountLogin();
      break;
    case path === '/profile':
      mountProfile();
      break;
    case path === '/chat' && !params.id:
      mountChatList();
      break;
    case path.startsWith('/chat/') && params.id:
      mountChatRoom(params);
      break;
    case path.startsWith('/payment/'):
      mountPayment(params);
      break;
    case path === '/orders':
      mountOrders();
      break;
    case path === '/flash':
      mountFlash();
      break;
    case path === '/privacy':
      mountPrivacy();
      break;
  }
};

// ==================== 启动 ====================

// 恢复登录状态
auth.fetchMe();

// 启动路由
router.start();

console.log('🏠 卓翌定制 SPA 已启动');
