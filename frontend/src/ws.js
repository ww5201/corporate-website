/**
 * WebSocket Manager - 实时聊天连接管理
 */
class WSManager {
  constructor() {
    this.ws = null;
    this.listeners = new Map();
    this.reconnectTimer = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 1000;
    this.convId = null;
    this.isConnected = false;
  }

  /**
   * 连接到聊天 WebSocket
   */
  connect(convId) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN && this.convId === convId) {
      return; // 已连接到同一对话
    }

    this.disconnect();
    this.convId = convId;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/chat?convId=${convId}`;

    try {
      this.ws = new WebSocket(wsUrl);
    } catch (e) {
      console.warn('WebSocket connection failed, falling back to polling');
      this._emit('fallback', { type: 'polling' });
      return;
    }

    this.ws.onopen = () => {
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this._emit('connected', {});
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this._emit('message', data);
      } catch (e) {
        console.error('WS parse error:', e);
      }
    };

    this.ws.onclose = () => {
      this.isConnected = false;
      this._emit('disconnected', {});
      this._scheduleReconnect();
    };

    this.ws.onerror = (err) => {
      console.warn('WebSocket error:', err);
      this.isConnected = false;
    };
  }

  /**
   * 发送消息
   */
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
      return true;
    }
    return false;
  }

  /**
   * 断开连接
   */
  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.onclose = null;
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
    this.convId = null;
    this.reconnectAttempts = 0;
  }

  /**
   * 注册事件监听
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
    return () => {
      const arr = this.listeners.get(event);
      const idx = arr.indexOf(callback);
      if (idx > -1) arr.splice(idx, 1);
    };
  }

  _emit(event, data) {
    const cbs = this.listeners.get(event) || [];
    cbs.forEach(cb => cb(data));
  }

  _scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this._emit('fallback', { type: 'polling' });
      return;
    }
    const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts);
    this.reconnectAttempts++;
    this.reconnectTimer = setTimeout(() => {
      if (this.convId) {
        this.connect(this.convId);
      }
    }, delay);
  }
}

export const ws = new WSManager();
