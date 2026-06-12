/**
 * Hash-based SPA Router
 * 支持: /home, /category, /product/:id, /login, /chat, /chat/:id, /profile, /orders, /payment/:orderId
 */
export class Router {
  constructor() {
    this.routes = [];
    this.currentRoute = null;
    this.beforeEach = null;
    this.afterEach = null;
    this._onHashChange = this._onHashChange.bind(this);
    window.addEventListener('hashchange', this._onHashChange);
  }

  /**
   * 注册路由
   * @param {string} path - 路径模式, 如 '/product/:id'
   * @param {Function} handler - async (params) => { title, render }
   */
  on(path, handler) {
    const paramNames = [];
    const regexStr = path.replace(/:(\w+)/g, (_, name) => {
      paramNames.push(name);
      return '([^/]+)';
    });
    this.routes.push({
      path,
      regex: new RegExp('^' + regexStr + '$'),
      paramNames,
      handler,
    });
  }

  /**
   * 启动路由
   */
  start() {
    if (!window.location.hash) {
      window.location.hash = '#/home';
    } else {
      this._onHashChange();
    }
  }

  /**
   * 编程式导航
   */
  navigate(path) {
    window.location.hash = '#' + path;
  }

  /**
   * 解析当前 hash
   */
  _parseHash() {
    const hash = window.location.hash.slice(1) || '/home';
    const [path, queryString] = hash.split('?');
    const query = {};
    if (queryString) {
      queryString.split('&').forEach(pair => {
        const [k, v] = pair.split('=');
        query[decodeURIComponent(k)] = decodeURIComponent(v || '');
      });
    }
    return { path, query };
  }

  /**
   * 匹配路由
   */
  _matchRoute(path) {
    for (const route of this.routes) {
      const match = path.match(route.regex);
      if (match) {
        const params = {};
        route.paramNames.forEach((name, i) => {
          params[name] = decodeURIComponent(match[i + 1]);
        });
        return { route, params };
      }
    }
    return null;
  }

  /**
   * hash 变化处理
   */
  async _onHashChange() {
    const { path, query } = this._parseHash();
    const result = this._matchRoute(path);

    if (!result) {
      // 404
      this._render404();
      return;
    }

    const { route, params } = result;

    // beforeEach 守卫
    if (this.beforeEach) {
      const allowed = await this.beforeEach(path, params, query);
      if (allowed === false) return;
    }

    this.currentRoute = { path, params, query };

    try {
      const { title, render } = await route.handler(params, query);
      document.title = title ? `${title} | 卓翌定制` : '卓翌定制';

      const app = document.getElementById('app');
      app.innerHTML = await render();

      // 执行页面挂载后的逻辑
      if (typeof window.__pageMount === 'function') {
        window.__pageMount(params, query);
      }

      // afterEach
      if (this.afterEach) {
        this.afterEach(path, params, query);
      }
    } catch (err) {
      console.error('Route error:', err);
      this._render404();
    }
  }

  _render404() {
    document.getElementById('app').innerHTML = `
      <div class="error-page">
        <div class="error-icon">404</div>
        <h2>页面不存在</h2>
        <a href="#/home" class="btn-primary">返回首页</a>
      </div>
    `;
  }
}

export const router = new Router();
