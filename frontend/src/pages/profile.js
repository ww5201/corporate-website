/**
 * Profile Page - 个人中心
 */
import { auth } from '../auth.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { showToast } from '../components/toast.js';

export async function profilePage() {
  if (!auth.isLoggedIn()) {
    window.location.hash = '#/login';
    return { title: '我的', render: () => '' };
  }

  // Refresh user data
  await auth.fetchMe();
  const user = auth.getUser();

  return {
    title: '我的',
    render: () => `
      <div class="page-body">
        <div class="profile-header">
          <div class="profile-avatar">${user?.nickname?.charAt(0) || '?'}</div>
          <div class="profile-name">${user?.nickname || '未登录'}</div>
          <div class="profile-phone">${user?.phone ? user.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2') : ''}</div>
        </div>

        <div class="profile-menu">
          <a href="#/orders" class="profile-menu-item">
            <span class="icon">📦</span>
            <span class="text">我的订单</span>
            <span class="arrow">›</span>
          </a>
          <div class="profile-menu-item" onclick="window._editProfile()">
            <span class="icon">✏️</span>
            <span class="text">编辑资料</span>
            <span class="arrow">›</span>
          </div>
          <a href="#/chat" class="profile-menu-item">
            <span class="icon">💬</span>
            <span class="text">联系客服</span>
            <span class="arrow">›</span>
          </a>
        </div>

        <div class="profile-menu">
          <div class="profile-menu-item" onclick="window._showAbout()">
            <span class="icon">ℹ️</span>
            <span class="text">关于我们</span>
            <span class="arrow">›</span>
          </div>
          <a href="#/privacy" class="profile-menu-item">
            <span class="icon">🔒</span>
            <span class="text">隐私政策</span>
            <span class="arrow">›</span>
          </a>
        </div>

        <div style="padding:20px;text-align:center">
          <button onclick="window._logout()" class="btn-outline" style="color:var(--danger);border-color:var(--danger);width:100%">
            退出登录
          </button>
        </div>
      </div>
      ${renderBottomNav('profile')}

      <!-- 编辑资料弹窗 -->
      <div id="editModal" style="display:none;position:fixed;inset:0;z-index:200">
        <div style="position:absolute;inset:0;background:rgba(0,0,0,0.5)" onclick="window._hideEditModal()"></div>
        <div style="position:absolute;bottom:0;left:0;right:0;background:var(--card-bg);border-radius:16px 16px 0 0;padding:20px">
          <h3 style="font-size:16px;margin-bottom:16px">编辑资料</h3>
          <div class="form-group">
            <label class="form-label">昵称</label>
            <input class="form-input" id="editNickname" value="${user?.nickname || ''}" placeholder="请输入昵称">
          </div>
          <button class="btn-primary btn-block" onclick="window._saveProfile()" style="border-radius:var(--radius-sm)">保存</button>
        </div>
      </div>
    `
  };
}

export function mountProfile() {
  window._logout = () => {
    auth.logout();
    showToast('已退出登录', 'success');
    window.location.hash = '#/home';
  };

  window._editProfile = () => {
    document.getElementById('editModal').style.display = 'block';
  };
  window._hideEditModal = () => {
    document.getElementById('editModal').style.display = 'none';
  };
  window._saveProfile = async () => {
    const nickname = document.getElementById('editNickname').value.trim();
    if (!nickname) {
      showToast('昵称不能为空', 'error');
      return;
    }
    try {
      await auth.updateProfile({ nickname });
      showToast('保存成功', 'success');
      window._hideEditModal();
      // Refresh page
      window.location.hash = '#/profile';
    } catch (e) {
      showToast(e.message || '保存失败', 'error');
    }
  };

  window._showAbout = () => {
    showToast('卓翌定制 v2.0', 'info');
  };
}
