/**
 * Auth Manager - 用户认证状态管理
 */
import { api } from './api.js';

class AuthManager {
  constructor() {
    this.user = null;
    this.token = null;
    this._loadFromStorage();
  }

  _loadFromStorage() {
    try {
      const token = localStorage.getItem('auth_token');
      const userStr = localStorage.getItem('auth_user');
      if (token && userStr) {
        this.token = token;
        this.user = JSON.parse(userStr);
      }
    } catch {}
  }

  isLoggedIn() {
    return !!this.token && !!this.user;
  }

  getUser() {
    return this.user;
  }

  getToken() {
    return this.token;
  }

  /**
   * 手机号 + 验证码登录
   */
  async loginByPhone(phone, code) {
    const res = await api.post('/auth/phone/login', { phone, code });
    if (res.success) {
      this._setAuth(res.token, res.user);
    }
    return res;
  }

  /**
   * 发送短信验证码
   */
  async sendSmsCode(phone) {
    return api.post('/auth/sms/send', { phone });
  }

  /**
   * 微信登录
   */
  async loginByWechat(code, nickname, avatar) {
    const res = await api.post('/auth/wechat/login', { code, nickname, avatar });
    if (res.success) {
      this._setAuth(res.token, res.user);
    }
    return res;
  }

  /**
   * 获取当前用户信息
   */
  async fetchMe() {
    if (!this.token) return null;
    try {
      const res = await api.get('/auth/me');
      if (res.success) {
        this.user = res.user;
        localStorage.setItem('auth_user', JSON.stringify(res.user));
      }
      return res.user;
    } catch {
      this.logout();
      return null;
    }
  }

  /**
   * 更新用户信息
   */
  async updateProfile(data) {
    const res = await api.put('/auth/me', data);
    if (res.success) {
      await this.fetchMe();
    }
    return res;
  }

  /**
   * 退出登录
   */
  logout() {
    this.user = null;
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  }

  _setAuth(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem('auth_token', token);
    localStorage.setItem('auth_user', JSON.stringify(user));
  }
}

export const auth = new AuthManager();
