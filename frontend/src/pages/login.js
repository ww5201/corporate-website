/**
 * Login Page - 登录页
 */
import { auth } from '../auth.js';
import { showToast } from '../components/toast.js';

let smsCountdown = 0;
let smsTimer = null;

export async function loginPage() {
  if (auth.isLoggedIn()) {
    window.location.hash = '#/profile';
    return { title: '登录', render: () => '' };
  }

  return {
    title: '登录',
    render: () => `
      <div class="login-page">
        <div class="login-logo">🏠</div>
        <div class="login-title">卓翌定制</div>
        <div class="login-subtitle">高端家居定制平台</div>

        <div class="login-form">
          <div class="form-group">
            <input class="form-input" id="loginPhone" type="tel" placeholder="手机号" maxlength="11">
          </div>
          <div class="form-group">
            <div class="sms-row">
              <input class="form-input" id="loginCode" type="text" placeholder="验证码" maxlength="6">
              <button class="sms-btn" id="smsBtn" onclick="window._sendSms()">获取验证码</button>
            </div>
          </div>
          <button class="btn-primary btn-block btn-lg" onclick="window._doLogin()" style="margin-top:8px;border-radius:var(--radius-sm)">
            登录 / 注册
          </button>

          <div class="login-divider">其他登录方式</div>

          <button class="login-wechat-btn" onclick="window._wechatLogin()">
            <span style="font-size:20px">💚</span>
            微信快捷登录
          </button>
        </div>
      </div>
    `
  };
}

export function mountLogin() {
  window._sendSms = async () => {
    const phone = document.getElementById('loginPhone').value.trim();
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      showToast('请输入正确的手机号', 'error');
      return;
    }

    const btn = document.getElementById('smsBtn');
    btn.disabled = true;

    try {
      const res = await auth.sendSmsCode(phone);
      showToast(res._debugCode ? `验证码: ${res._debugCode}` : '验证码已发送', 'success');
      smsCountdown = 60;
      smsTimer = setInterval(() => {
        smsCountdown--;
        btn.textContent = `${smsCountdown}s`;
        if (smsCountdown <= 0) {
          clearInterval(smsTimer);
          btn.textContent = '获取验证码';
          btn.disabled = false;
        }
      }, 1000);
    } catch (e) {
      showToast(e.message || '发送失败', 'error');
      btn.disabled = false;
    }
  };

  window._doLogin = async () => {
    const phone = document.getElementById('loginPhone').value.trim();
    const code = document.getElementById('loginCode').value.trim();

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      showToast('请输入正确的手机号', 'error');
      return;
    }
    if (!/^\d{4,6}$/.test(code)) {
      showToast('请输入验证码', 'error');
      return;
    }

    try {
      const res = await auth.loginByPhone(phone, code);
      if (res.success) {
        showToast(res.user?.isNew ? '注册成功！' : '登录成功！', 'success');
        setTimeout(() => {
          window.location.hash = '#/profile';
        }, 500);
      }
    } catch (e) {
      showToast(e.message || '登录失败', 'error');
    }
  };

  window._wechatLogin = async () => {
    try {
      const res = await auth.loginByWechat('mock_code_' + Date.now());
      if (res.success) {
        showToast('登录成功！', 'success');
        setTimeout(() => {
          window.location.hash = '#/profile';
        }, 500);
      }
    } catch (e) {
      showToast(e.message || '微信登录失败', 'error');
    }
  };
}
