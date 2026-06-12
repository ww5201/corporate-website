/**
 * Chat Page - 聊天页面
 */
import { api } from '../api.js';
import { auth } from '../auth.js';
import { ws } from '../ws.js';
import { showToast } from '../components/toast.js';
import { renderBottomNav } from '../components/bottom-nav.js';
import { timeAgo } from '../utils.js';

let pollTimer = null;

export async function chatListPage() {
  return {
    title: '消息',
    render: async () => {
      let conversations = [];
      try {
        conversations = await api.get('/conversations');
      } catch (e) { console.error(e); }

      // If no conversations, create one automatically
      if (conversations.length === 0) {
        try {
          const user = auth.getUser();
          const res = await api.post('/conversations', {
            visitorId: user?.id || 'visitor_' + Date.now(),
            name: user?.nickname || '访客',
            phone: user?.phone || '',
          });
          conversations = [res];
        } catch (e) { console.error(e); }
      }

      return `
        <div class="nav-header">
          <div class="nav-title">消息</div>
        </div>
        <div class="page-body">
          <div class="conv-list">
            ${conversations.map(conv => `
              <a href="#/chat/${conv._id}" class="conv-item">
                <div class="conv-avatar">${(conv.name || '?').charAt(0)}</div>
                <div class="conv-info">
                  <div class="conv-name">${conv.name || '访客'}</div>
                  <div class="conv-last">${conv.messages?.length ? conv.messages[conv.messages.length - 1].content : '暂无消息'}</div>
                </div>
                <div class="conv-time">${conv.updatedAt ? timeAgo(conv.updatedAt) : ''}</div>
                ${conv.unread > 0 ? '<div class="conv-badge"></div>' : ''}
              </a>
            `).join('') || '<div class="empty-state"><div class="empty-icon">💬</div><p>暂无对话</p></div>'}
          </div>
        </div>
        ${renderBottomNav('chat')}
      `;
    }
  };
}

export async function chatRoomPage(params) {
  const convId = params.id;

  return {
    title: '客服聊天',
    render: async () => {
      let messages = [];
      try {
        messages = await api.get(`/conversations/${convId}/messages`);
      } catch (e) { console.error(e); }

      return `
        <div class="chat-page">
          <div class="chat-header">
            <button class="back" onclick="window.location.hash='#/chat'">‹</button>
            <div class="title">客服</div>
            <div style="min-width:50px;text-align:right;font-size:12px;color:var(--text-muted)" id="wsStatus">连接中...</div>
          </div>
          <div class="chat-messages" id="chatMessages">
            ${messages.map(m => `
              <div class="chat-msg ${m.sender === 'visitor' ? 'visitor' : 'admin'}">
                <div>${m.content}</div>
                <div class="time">${timeAgo(m.createdAt)}</div>
              </div>
            `).join('') || '<div class="empty-state" style="flex:1"><div class="empty-icon">💬</div><p>开始聊天吧</p></div>'}
          </div>
          <div class="chat-input-bar">
            <input type="text" id="chatInput" placeholder="输入消息..." onkeydown="if(event.key==='Enter')window._sendMsg()">
            <button class="chat-send-btn" onclick="window._sendMsg()">发送</button>
          </div>
        </div>
      `;
    }
  };
}

export function mountChatRoom(params) {
  const convId = params.id;
  let lastMsgTime = '';
  let usePolling = false;

  // Scroll to bottom
  const messagesEl = document.getElementById('chatMessages');
  if (messagesEl) {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // Try WebSocket first
  ws.connect(convId);

  ws.on('connected', () => {
    const status = document.getElementById('wsStatus');
    if (status) status.textContent = '已连接';
  });

  ws.on('disconnected', () => {
    const status = document.getElementById('wsStatus');
    if (status) status.textContent = '连接断开';
  });

  ws.on('fallback', () => {
    usePolling = true;
    const status = document.getElementById('wsStatus');
    if (status) status.textContent = '轮询中';
    startPolling();
  });

  ws.on('message', (data) => {
    if (data.type === 'new_message') {
      appendMessage(data.message);
    }
  });

  // Fallback: polling
  function startPolling() {
    clearInterval(pollTimer);
    pollTimer = setInterval(async () => {
      try {
        const res = await api.get(`/conversations/${convId}/poll?since=${lastMsgTime}`);
        if (res.messages?.length) {
          res.messages.forEach(m => appendMessage(m));
        }
      } catch (e) {}
    }, 3000);
  }

  function appendMessage(msg) {
    const container = document.getElementById('chatMessages');
    if (!container) return;

    // Remove empty state
    const empty = container.querySelector('.empty-state');
    if (empty) empty.remove();

    const div = document.createElement('div');
    div.className = `chat-msg ${msg.sender === 'visitor' ? 'visitor' : 'admin'}`;
    div.innerHTML = `<div>${msg.content}</div><div class="time">${timeAgo(msg.createdAt)}</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    lastMsgTime = msg.createdAt;
  }

  // Send message
  window._sendMsg = async () => {
    const input = document.getElementById('chatInput');
    const content = input?.value.trim();
    if (!content) return;

    input.value = '';

    // Try WebSocket first
    const sent = ws.send({
      type: 'message',
      convId,
      sender: 'visitor',
      content,
    });

    if (!sent) {
      // Fallback to API
      try {
        const msg = await api.post(`/conversations/${convId}/messages`, {
          sender: 'visitor',
          content,
          type: 'text',
        });
        appendMessage(msg);
      } catch (e) {
        showToast('发送失败', 'error');
      }
    }
  };

  // Cleanup
  window.addEventListener('hashchange', () => {
    ws.disconnect();
    clearInterval(pollTimer);
  }, { once: true });
}

export function mountChatList() {
  // Just the list, no special mount logic needed
}
