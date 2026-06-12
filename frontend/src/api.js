/**
 * API Client - 统一请求封装
 */
const API_BASE = '/api';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE;
  }

  _getToken() {
    return localStorage.getItem('auth_token');
  }

  async request(method, path, data = null, options = {}) {
    const url = this.baseURL + path;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = this._getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = { method, headers };
    if (data && method !== 'GET') {
      config.body = JSON.stringify(data);
    }

    try {
      const res = await fetch(url, config);
      const json = await res.json();

      if (!res.ok) {
        const err = new Error(json.error || json.message || '请求失败');
        err.status = res.status;
        err.data = json;
        throw err;
      }

      return json;
    } catch (err) {
      if (err.status === 401 && !options.skipAuthRedirect) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        window.location.hash = '#/login';
      }
      throw err;
    }
  }

  get(path, options) {
    return this.request('GET', path, null, options);
  }

  post(path, data, options) {
    return this.request('POST', path, data, options);
  }

  put(path, data, options) {
    return this.request('PUT', path, data, options);
  }

  delete(path, options) {
    return this.request('DELETE', path, null, options);
  }
}

export const api = new ApiClient();
