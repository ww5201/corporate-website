// ========== 卓翌定制 - 共享模块 ==========
export const API_BASE = '/api';

// ========== 多语言翻译 ==========
export const translations = {
  zh: {
    'search.placeholder': '搜索商品',
    'banner.s1.title': '全屋定制 工厂直供', 'banner.s1.desc': '品质家居 · 低至3折起', 'banner.s1.tag': '限时特惠',
    'banner.s2.title': '新品上市 橱柜系列', 'banner.s2.desc': '设计师联名 · 限量特惠', 'banner.s2.tag': '新品首发',
    'banner.s3.title': '拼团更优惠', 'banner.s3.desc': '万人团购 · 价格直降到底', 'banner.s3.tag': '万人团',
    'cat.all': '全部', 'cat.cabinet': '柜类', 'cat.wardrobe': '衣柜', 'cat.kitchen': '橱柜',
    'cat.custom': '定制', 'cat.flash': '秒杀', 'cat.group': '拼团', 'cat.contact': '联系',
    'flash.title': '限时秒杀', 'flash.ends': '距结束', 'flash.more': '更多 ›',
    'group.title': '万人拼团', 'group.badge': '超值低价', 'group.more': '更多 ›', 'group.joined': '人已拼',
    'rec.title': '为你推荐',
    'shop.title': '精选商品', 'shop.cat.all': '全部', 'shop.cat.cabinet': '柜类', 'shop.cat.wardrobe': '衣柜',
    'shop.cat.kitchen': '橱柜', 'shop.cat.custom': '定制',
    'shop.inquire': '立即咨询', 'shop.price': '起', 'shop.empty': '暂无商品',
    'pc.group_price': '拼团价', 'pc.single_price': '单买价', 'pc.sold': '已拼',
    'pc.coupon': '领券', 'pc.free_ship': '包邮', 'pc.refund': '退',
    'about.title': '关于我们',
    'about.lead': '超过二十年的行业沉淀，我们始终坚持品质至上的理念。',
    'about.desc': '我们致力于为追求卓越的客户提供量身定制的解决方案，每一个项目都倾注我们的匠心与热情。',
    'about.stat1': '行业经验', 'about.stat2': '成功案例', 'about.stat3': '客户满意度',
    'contact.title': '联系我们',
    'contact.addr.label': '地址', 'contact.addr.value': '广西壮族自治区南宁市江南区那洪大道留村路 1-2 号',
    'contact.phone.label': '电话', 'contact.email.label': '邮箱',
    'contact.form.name': '您的姓名', 'contact.form.email': '电子邮箱',
    'contact.form.message': '留言内容', 'contact.form.submit': '发送留言',
    'product.inquire': '立即咨询', 'product.price': '起',
    'modal.close': '关闭', 'modal.title_prefix': '产品详情',
    'modal.name': '您的姓名', 'modal.phone': '联系电话', 'modal.email': '邮箱（选填）',
    'modal.submit': '提交咨询', 'modal.success': '提交成功！我们会尽快联系您。',
    'modal.wechat_pay': '微信支付', 'modal.alipay': '支付宝',
    'modal.scan_pay': '扫描二维码支付', 'modal.pay_success': '支付完成', 'modal.pay_confirm': '确认支付',
    'lightbox.hint': '点击放大',
    'tab.inquire': '立即咨询', 'tab.pay': '立即订购', 'modal.msg': '留言（选填）',
    'pay.name': '您的姓名', 'pay.phone': '联系电话', 'pay.addr': '收货地址', 'pay.note': '备注',
    'pay.total': '订单金额', 'pay.loading': '加载支付方式...',
    'pay.hint': '扫码付款后，点击确认', 'pay.confirm': '确认已支付',
    'pay.required': '请填写姓名和电话', 'pay.success': '订单已提交！我们会尽快确认。',
    'pay.none': '暂未配置支付方式', 'pay.error': '加载失败',
    'bnav.home': '首页', 'bnav.cate': '分类', 'bnav.flash': '秒杀', 'bnav.chat': '消息', 'bnav.mine': '我的',
    // 用户中心
    'mine.title': '我的', 'mine.login': '登录/注册', 'mine.orders': '我的订单', 'mine.chat': '我的消息',
    'mine.settings': '设置', 'mine.about': '关于我们', 'mine.logout': '退出登录',
    'mine.phone': '手机号', 'mine.nickname': '昵称', 'mine.bindphone': '绑定手机',
    'mine.all_orders': '全部订单', 'mine.pending': '待付款', 'mine.paid': '已付款', 'mine.shipped': '已发货', 'mine.done': '已完成',
    'mine.no_orders': '暂无订单', 'mine.login_hint': '登录后享受更多服务',
    // 登录
    'login.title': '登录', 'login.phone': '手机号', 'login.code': '验证码',
    'login.send_code': '获取验证码', 'login.resend': '秒后重发', 'login.submit': '登录',
    'login.wechat': '微信登录', 'login.agree': '登录即表示同意', 'login.terms': '用户协议',
    'login.phone_error': '请输入正确的手机号', 'login.code_error': '请输入6位验证码',
    // 聊天
    'chat.title': '消息', 'chat.empty': '暂无消息', 'chat.placeholder': '输入消息...',
    'chat.send': '发送', 'chat.new': '新对话', 'chat.no_conv': '暂无对话，点击发起新对话',
    'chat.visitor': '访客', 'chat.admin': '客服',
  },
  en: {
    'search.placeholder': 'Search products',
    'banner.s1.title': 'Custom Furniture Factory Direct', 'banner.s1.desc': 'Quality Home · Up to 70% Off', 'banner.s1.tag': 'Flash Deal',
    'banner.s2.title': 'New Arrival Cabinet Series', 'banner.s2.desc': 'Designer Collab · Limited Edition', 'banner.s2.tag': 'New',
    'banner.s3.title': 'Group Buy & Save More', 'banner.s3.desc': '10K+ Group · Rock Bottom Prices', 'banner.s3.tag': 'Group Deal',
    'cat.all': 'All', 'cat.cabinet': 'Cabinets', 'cat.wardrobe': 'Wardrobes', 'cat.kitchen': 'Kitchen',
    'cat.custom': 'Custom', 'cat.flash': 'Flash', 'cat.group': 'Group', 'cat.contact': 'Contact',
    'flash.title': 'Flash Sale', 'flash.ends': 'Ends in', 'flash.more': 'More ›',
    'group.title': 'Group Buy', 'group.badge': 'Best Value', 'group.more': 'More ›', 'group.joined': 'joined',
    'rec.title': 'Recommended',
    'shop.title': 'Featured Shop', 'shop.cat.all': 'All', 'shop.cat.cabinet': 'Cabinets', 'shop.cat.wardrobe': 'Wardrobes',
    'shop.cat.kitchen': 'Kitchen', 'shop.cat.custom': 'Custom',
    'shop.inquire': 'Inquire', 'shop.price': 'up', 'shop.empty': 'No items',
    'pc.group_price': 'Group', 'pc.single_price': 'Single', 'pc.sold': 'sold',
    'pc.coupon': 'Coupon', 'pc.free_ship': 'Free Ship', 'pc.refund': 'Return',
    'about.title': 'About Us', 'about.lead': 'With over 20 years of experience, quality first.',
    'about.desc': 'Tailored solutions for clients who pursue excellence.',
    'about.stat1': 'Years', 'about.stat2': 'Projects', 'about.stat3': 'Satisfaction',
    'contact.title': 'Contact Us', 'contact.addr.label': 'Address', 'contact.addr.value': 'Nanning, Guangxi, China',
    'contact.phone.label': 'Phone', 'contact.email.label': 'Email',
    'contact.form.name': 'Your Name', 'contact.form.email': 'Email',
    'contact.form.message': 'Message', 'contact.form.submit': 'Send',
    'product.inquire': 'Inquire Now', 'product.price': 'up',
    'modal.close': 'Close', 'modal.title_prefix': 'Details',
    'modal.name': 'Name', 'modal.phone': 'Phone', 'modal.email': 'Email (opt)',
    'modal.submit': 'Submit', 'modal.success': 'Submitted!',
    'modal.wechat_pay': 'WeChat Pay', 'modal.alipay': 'Alipay',
    'modal.scan_pay': 'Scan QR', 'modal.pay_success': 'Done', 'modal.pay_confirm': 'Confirm',
    'lightbox.hint': 'Click to enlarge',
    'tab.inquire': 'Inquire', 'tab.pay': 'Order', 'modal.msg': 'Message (opt)',
    'pay.name': 'Name', 'pay.phone': 'Phone', 'pay.addr': 'Address', 'pay.note': 'Note',
    'pay.total': 'Total', 'pay.loading': 'Loading...', 'pay.hint': 'Scan then confirm',
    'pay.confirm': 'Confirm', 'pay.required': 'Name & phone required', 'pay.success': 'Order submitted!',
    'pay.none': 'No payment', 'pay.error': 'Failed',
    'bnav.home': 'Home', 'bnav.cate': 'Category', 'bnav.flash': 'Flash', 'bnav.chat': 'Chat', 'bnav.mine': 'Me',
    'mine.title': 'Me', 'mine.login': 'Login', 'mine.orders': 'My Orders', 'mine.chat': 'Messages',
    'mine.settings': 'Settings', 'mine.about': 'About', 'mine.logout': 'Logout',
    'mine.phone': 'Phone', 'mine.nickname': 'Nickname', 'mine.bindphone': 'Bind Phone',
    'mine.all_orders': 'All', 'mine.pending': 'Pending', 'mine.paid': 'Paid', 'mine.shipped': 'Shipped', 'mine.done': 'Done',
    'mine.no_orders': 'No orders', 'mine.login_hint': 'Login for more',
    'login.title': 'Login', 'login.phone': 'Phone', 'login.code': 'Code',
    'login.send_code': 'Send Code', 'login.resend': 's resend', 'login.submit': 'Login',
    'login.wechat': 'WeChat Login', 'login.agree': 'By logging in you agree to', 'login.terms': 'Terms',
    'login.phone_error': 'Enter valid phone', 'login.code_error': 'Enter 6-digit code',
    'chat.title': 'Messages', 'chat.empty': 'No messages', 'chat.placeholder': 'Type a message...',
    'chat.send': 'Send', 'chat.new': 'New Chat', 'chat.no_conv': 'No conversations, start one',
    'chat.visitor': 'You', 'chat.admin': 'Support',
  },
  ja: {
    'search.placeholder': '商品を検索',
    'banner.s1.title': '全屋カスタム 工場直販', 'banner.s1.desc': '高品質 · 最大70%OFF', 'banner.s1.tag': 'タイムセール',
    'banner.s2.title': '新作キャビネット', 'banner.s2.desc': 'デザイナーコラボ · 限定', 'banner.s2.tag': '新着',
    'banner.s3.title': 'グループ購入でお得', 'banner.s3.desc': '万人団 · 最安値', 'banner.s3.tag': '万人団',
    'cat.all': '全て', 'cat.cabinet': 'キャビネット', 'cat.wardrobe': 'ワードローブ', 'cat.kitchen': 'キッチン',
    'cat.custom': 'オーダー', 'cat.flash': 'セール', 'cat.group': '団購', 'cat.contact': '連絡',
    'flash.title': 'タイムセール', 'flash.ends': '終了まで', 'flash.more': 'もっと ›',
    'group.title': 'グループ購入', 'group.badge': '超お得', 'group.more': 'もっと ›', 'group.joined': '人参加',
    'rec.title': 'おすすめ',
    'shop.cat.all': '全て', 'shop.cat.cabinet': 'キャビネット', 'shop.cat.wardrobe': 'ワードローブ',
    'shop.cat.kitchen': 'キッチン', 'shop.cat.custom': 'オーダー',
    'shop.inquire': 'お問い合わせ', 'shop.price': '〜', 'shop.empty': '商品なし',
    'pc.group_price': '団購価', 'pc.single_price': '通常価', 'pc.sold': '販売済',
    'pc.coupon': 'クーポン', 'pc.free_ship': '送料無料', 'pc.refund': '返品可',
    'about.title': '会社概要', 'about.lead': '20年以上の業界経験、品質第一。',
    'about.desc': 'お客様にカスタムソリューションを提供。',
    'about.stat1': '年の経験', 'about.stat2': '完成事例', 'about.stat3': '満足度',
    'contact.title': 'お問い合わせ', 'contact.addr.label': '住所', 'contact.addr.value': '中国広西壮族自治区南寧市',
    'contact.phone.label': '電話', 'contact.email.label': 'メール',
    'contact.form.name': 'お名前', 'contact.form.email': 'メール',
    'contact.form.message': 'メッセージ', 'contact.form.submit': '送信',
    'product.inquire': 'お問い合わせ', 'product.price': '〜',
    'modal.close': '閉じる', 'modal.title_prefix': '製品詳細',
    'modal.name': 'お名前', 'modal.phone': '電話番号', 'modal.email': 'メール',
    'modal.submit': '送信', 'modal.success': '送信完了！',
    'modal.wechat_pay': 'WeChat Pay', 'modal.alipay': 'Alipay',
    'lightbox.hint': 'クリックで拡大', 'tab.inquire': 'お問い合わせ', 'tab.pay': '注文', 'modal.msg': 'メッセージ',
    'pay.name': '名前', 'pay.phone': '電話', 'pay.addr': '住所', 'pay.note': '備考',
    'pay.total': '合計', 'pay.loading': '読込中...', 'pay.hint': 'スキャンして確認',
    'pay.confirm': '確認', 'pay.required': '名前と電話は必須', 'pay.success': '注文完了！',
    'pay.none': '支払い方法なし', 'pay.error': '失敗',
    'bnav.home': 'ホーム', 'bnav.cate': '分類', 'bnav.flash': 'セール', 'bnav.chat': 'チャット', 'bnav.mine': 'マイ',
    'mine.title': 'マイ', 'mine.login': 'ログイン', 'mine.orders': '注文履歴', 'mine.chat': 'メッセージ',
    'mine.settings': '設定', 'mine.about': '会社概要', 'mine.logout': 'ログアウト',
    'mine.phone': '電話番号', 'mine.nickname': 'ニックネーム', 'mine.bindphone': '携帯連携',
    'mine.all_orders': '全て', 'mine.pending': '未払い', 'mine.paid': '支払済', 'mine.shipped': '発送済', 'mine.done': '完了',
    'mine.no_orders': '注文なし', 'mine.login_hint': 'ログインでもっと便利に',
    'login.title': 'ログイン', 'login.phone': '電話番号', 'login.code': '認証コード',
    'login.send_code': 'コード取得', 'login.resend': '秒後に再送', 'login.submit': 'ログイン',
    'login.wechat': 'WeChatログイン', 'login.agree': 'ログインで', 'login.terms': '利用規約',
    'login.phone_error': '正しい電話番号を', 'login.code_error': '6桁コードを入力',
    'chat.title': 'メッセージ', 'chat.empty': 'メッセージなし', 'chat.placeholder': 'メッセージを入力...',
    'chat.send': '送信', 'chat.new': '新規チャット', 'chat.no_conv': 'チャットなし、新規作成',
    'chat.visitor': '自分', 'chat.admin': 'サポート',
  },
  ko: {
    'search.placeholder': '상품 검색',
    'bnav.home': '홈', 'bnav.cate': '카테고리', 'bnav.flash': '세일', 'bnav.chat': '채팅', 'bnav.mine': '마이',
    'flash.title': '타임세일', 'flash.ends': '종료까지', 'group.joined': '명 참여',
    'rec.title': '추천', 'shop.empty': '상품 없음', 'shop.inquire': '문의', 'shop.price': '부터',
    'mine.title': '마이', 'mine.login': '로그인', 'mine.orders': '주문내역', 'mine.chat': '메시지',
    'mine.settings': '설정', 'mine.logout': '로그아웃', 'mine.no_orders': '주문 없음',
    'login.title': '로그인', 'login.phone': '전화번호', 'login.code': '인증코드',
    'login.send_code': '코드 받기', 'login.submit': '로그인',
    'chat.title': '메시지', 'chat.empty': '메시지 없음', 'chat.send': '전송',
    'cat.all': '전체', 'cat.cabinet': '캐비닛', 'cat.wardrobe': '옷장', 'cat.kitchen': '주방', 'cat.custom': '맞춤',
  },
  th: {
    'search.placeholder': 'ค้นหาสินค้า',
    'bnav.home': 'หน้าแรก', 'bnav.cate': 'หมวดหมู่', 'bnav.flash': 'เซล', 'bnav.chat': 'แชท', 'bnav.mine': 'ฉัน',
    'flash.title': 'แฟลชเซล', 'rec.title': 'แนะนำ', 'shop.empty': 'ไม่มีสินค้า',
    'mine.title': 'ฉัน', 'mine.login': 'เข้าสู่ระบบ', 'mine.orders': 'คำสั่งซื้อ', 'mine.chat': 'ข้อความ',
    'mine.settings': 'ตั้งค่า', 'mine.logout': 'ออกจากระบบ', 'mine.no_orders': 'ไม่มีคำสั่ง',
    'login.title': 'เข้าสู่ระบบ', 'login.phone': 'เบอร์โทร', 'login.code': 'รหัส',
    'login.send_code': 'ขอรหัส', 'login.submit': 'เข้าสู่ระบบ',
    'chat.title': 'ข้อความ', 'chat.send': 'ส่ง', 'cat.all': 'ทั้งหมด',
  },
  vi: {
    'search.placeholder': 'Tìm sản phẩm',
    'bnav.home': 'Trang chủ', 'bnav.cate': 'Danh mục', 'bnav.flash': 'Sale', 'bnav.chat': 'Chat', 'bnav.mine': 'Tôi',
    'flash.title': 'Flash Sale', 'rec.title': 'Gợi ý', 'shop.empty': 'Chưa có',
    'mine.title': 'Tôi', 'mine.login': 'Đăng nhập', 'mine.orders': 'Đơn hàng', 'mine.chat': 'Tin nhắn',
    'mine.settings': 'Cài đặt', 'mine.logout': 'Đăng xuất', 'mine.no_orders': 'Chưa có đơn',
    'login.title': 'Đăng nhập', 'login.phone': 'SĐT', 'login.code': 'Mã',
    'login.send_code': 'Gửi mã', 'login.submit': 'Đăng nhập',
    'chat.title': 'Tin nhắn', 'chat.send': 'Gửi', 'cat.all': 'Tất cả',
  },
  ms: {
    'search.placeholder': 'Cari produk',
    'bnav.home': 'Utama', 'bnav.cate': 'Kategori', 'bnav.flash': 'Kilat', 'bnav.chat': 'Chat', 'bnav.mine': 'Saya',
    'flash.title': 'Jualan Kilat', 'rec.title': 'Disyorkan', 'shop.empty': 'Tiada',
    'mine.title': 'Saya', 'mine.login': 'Log masuk', 'mine.orders': 'Pesanan', 'mine.chat': 'Mesej',
    'mine.settings': 'Tetapan', 'mine.logout': 'Log keluar', 'mine.no_orders': 'Tiada pesanan',
    'login.title': 'Log masuk', 'login.phone': 'Telefon', 'login.code': 'Kod',
    'login.send_code': 'Hantar kod', 'login.submit': 'Log masuk',
    'chat.title': 'Mesej', 'chat.send': 'Hantar', 'cat.all': 'Semua',
  }
};

export const langLabels = { zh: '🇨🇳', en: '🇺🇸', ja: '🇯🇵', ko: '🇰🇷', th: '🇹🇭', vi: '🇻🇳', ms: '🇲🇾' };

export const productNames = {
  zh: { '鱼缸柜': '鱼缸柜', '柜子': '柜子', '橱柜定制': '橱柜定制', '衣帽间定制': '衣帽间定制', '整体衣柜定制': '整体衣柜定制', '666': '666' },
  en: { '鱼缸柜': 'Fish Tank Cabinet', '柜子': 'Cabinet', '橱柜定制': 'Kitchen Cabinet', '衣帽间定制': 'Walk-in Closet', '整体衣柜定制': 'Wardrobe', '666': '666' },
  ja: { '鱼缸柜': '魚棚キャビネット', '柜子': 'キャビネット', '橱柜定制': 'システムキッチン', '衣帽间定制': 'ウォークインクローゼット', '整体衣柜定制': 'ワードローブ', '666': '666' },
  ko: { '鱼缸柜': '수족관 캐비닛', '柜子': '캐비닛', '橱柜定制': '주방 캐비닛', '衣帽间定制': '워크인 클로젯', '整体衣柜定制': '워드로브', '666': '666' },
  th: { '鱼缸柜': 'ตู้ปลา', '柜子': 'ตู้', '橱柜定制': 'ตู้ครัว', '衣帽间定制': 'ตู้เสื้อผ้าWalk-in', '整体衣柜定制': 'ตู้เสื้อผ้า', '666': '666' },
  vi: { '鱼缸柜': 'Tủ Bể Cá', '柜子': 'Tủ', '橱柜定制': 'Tủ Bếp', '衣帽间定制': 'Tủ Quần Áo', '整体衣柜定制': 'Tủ Đồ', '666': '666' },
  ms: { '鱼缸柜': 'Kabinet Akuarium', '柜子': 'Kabinet', '橱柜定制': 'Kabinet Dapur', '衣帽间定制': 'Wardrobe Walk-in', '整体衣柜定制': 'Wardrobe', '666': '666' }
};

export const productDescs = {
  zh: { '鱼缸柜': '精美鱼缸柜定制', '柜子': '多功能柜子定制', '橱柜定制': '高端整体橱柜定制', '衣帽间定制': '豪华衣帽间定制', '整体衣柜定制': '全屋整体衣柜定制' },
  en: { '鱼缸柜': 'Custom Fish Tank Cabinet', '柜子': 'Multi-purpose Cabinet', '橱柜定制': 'Premium Kitchen Cabinet', '衣帽间定制': 'Luxury Walk-in Closet', '整体衣柜定制': 'Custom Wardrobe System' },
  ja: { '鱼缸柜': 'カスタム魚棚キャビネット', '柜子': '多目的キャビネット', '橱柜定制': 'プレミアムシステムキッチン', '衣帽间定制': 'ラグジュアリーウォークイン', '整体衣柜定制': 'カスタムワードローブ' },
  ko: { '鱼缸柜': '맞춤 수족관 캐비닛', '柜子': '다용도 캐비닛', '橱柜定制': '프리미엄 주방 캐비닛', '衣帽间定制': '럭셔리 워크인 클로젯', '整体衣柜定制': '맞춤 워드로브' },
  th: { '鱼缸柜': 'ตู้ปลาสั่งทำ', '柜子': 'ตู้อเนกประสงค์', '橱柜定制': 'ตู้ครัวพรีเมียม', '衣帽间定制': 'ตู้เสื้อผ้าหรู', '整体衣柜定制': 'ตู้เสื้อผ้าสั่งทำ' },
  vi: { '鱼缸柜': 'Tủ Bể Cá Đặt Làm', '柜子': 'Tủ Đa Năng', '橱柜定制': 'Tủ Bếp Cao Cấp', '衣帽间定制': 'Tủ Quần Áo Sang Trọng', '整体衣柜定制': 'Tủ Đồ Theo Yêu Cầu' },
  ms: { '鱼缸柜': 'Kabinet Akuarium Tersuai', '柜子': 'Kabinet Serbaguna', '橱柜定制': 'Kabinet Dapur Premium', '衣帽间定制': 'Wardrobe Mewah', '整体衣柜定制': 'Wardrobe Tersuai' }
};

// ========== 全局状态 ==========
export let currentLang = localStorage.getItem('lang') || 'zh';

export function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('lang', lang);
}

export function t(key) {
  const langData = translations[currentLang] || translations.zh;
  return langData[key] || translations.zh[key] || key;
}

export function trProductName(name) {
  const lang = productNames[currentLang] || productNames.zh;
  return lang[name] || name;
}

export function trProductDesc(name) {
  const lang = productDescs[currentLang] || productDescs.zh;
  return lang[name] || '';
}

export function applyLangToDOM() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = t(key);
    if (val) el.innerHTML = val;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const val = t(key);
    if (val) el.placeholder = val;
  });
  const langEl = document.getElementById('currentLang');
  if (langEl) langEl.textContent = langLabels[currentLang] || '🇨🇳';
}

// ========== 认证状态 ==========
export function getToken() { return localStorage.getItem('token'); }
export function getUser() {
  try { return JSON.parse(localStorage.getItem('user')); } catch { return null; }
}
export function isLoggedIn() { return !!getToken(); }
export function setAuth(token, user) {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
}
export function clearAuth() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

export async function fetchMe() {
  const token = getToken();
  if (!token) return null;
  try {
    const res = await fetch(`${API_BASE}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
    if (!res.ok) { clearAuth(); return null; }
    const data = await res.json();
    if (data.success) {
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    }
    return null;
  } catch { return null; }
}

// ========== 底部导航 ==========
export function renderBottomNav(activeTab) {
  const tabs = [
    { key: 'home', icon: '🏠', labelKey: 'bnav.home', href: '/index.html' },
    { key: 'cate', icon: '📦', labelKey: 'bnav.cate', href: '/category.html' },
    { key: 'flash', icon: '⚡', labelKey: 'bnav.flash', href: '/flash.html' },
    { key: 'chat', icon: '💬', labelKey: 'bnav.chat', href: '/chat.html' },
    { key: 'mine', icon: '👤', labelKey: 'bnav.mine', href: '/mine.html' },
  ];

  const nav = document.createElement('nav');
  nav.className = 'pdd-bottom-nav';
  nav.innerHTML = tabs.map(tab => `
    <a href="${tab.href}" class="pdd-bnav-item ${tab.key === activeTab ? 'active' : ''}">
      <span class="pdd-bnav-icon">${tab.icon}</span>
      <span>${t(tab.labelKey)}</span>
    </a>
  `).join('');

  document.body.appendChild(nav);
}

// ========== 顶部Header ==========
export function renderHeader(opts = {}) {
  const { showBack = false, title = '', showSearch = true, showLang = true } = opts;
  const header = document.createElement('header');
  header.className = 'pdd-header';
  header.id = 'pddHeader';

  let leftHtml = '';
  if (showBack) {
    leftHtml = `<a href="javascript:history.back()" class="header-back">‹</a>`;
  }

  let centerHtml = '';
  if (title) {
    centerHtml = `<div class="header-title">${title}</div>`;
  } else if (showSearch) {
    centerHtml = `
      <div class="pdd-search-bar">
        <span class="pdd-search-icon">🔍</span>
        <input type="text" class="pdd-search-input" id="pddSearchInput"
          data-i18n-placeholder="search.placeholder" placeholder="${t('search.placeholder')}">
      </div>`;
  }

  let rightHtml = '';
  if (showLang) {
    rightHtml = `
      <div class="lang-switcher">
        <button class="lang-btn" id="langBtn">
          <span id="currentLang">${langLabels[currentLang] || '🇨🇳'}</span>
          <span class="arrow">▾</span>
        </button>
        <div class="lang-dropdown" id="langDropdown">
          ${Object.entries(langLabels).map(([code, emoji]) => `
            <div class="lang-option ${code === currentLang ? 'active' : ''}" data-lang="${code}">${emoji} ${code.toUpperCase()}</div>
          `).join('')}
        </div>
      </div>`;
  }

  header.innerHTML = `
    <div class="pdd-header-inner">
      ${leftHtml}
      ${title ? '' : '<div class="pdd-logo">卓翌<span>定制</span></div>'}
      ${centerHtml}
      ${rightHtml}
    </div>`;

  document.body.prepend(header);
  initLangSwitcher();
}

function initLangSwitcher() {
  const langBtn = document.getElementById('langBtn');
  const langDropdown = document.getElementById('langDropdown');
  if (!langBtn || !langDropdown) return;

  langBtn.addEventListener('click', e => { e.stopPropagation(); langDropdown.classList.toggle('show'); });
  document.addEventListener('click', () => langDropdown.classList.remove('show'));
  langDropdown.querySelectorAll('.lang-option').forEach(opt => {
    opt.addEventListener('click', () => {
      setLang(opt.dataset.lang);
      applyLangToDOM();
      // Re-render nav with new lang
      const oldNav = document.querySelector('.pdd-bottom-nav');
      const activeTab = oldNav?.querySelector('.pdd-bnav-item.active')?.querySelector('.pdd-bnav-icon')?.textContent;
      if (oldNav) oldNav.remove();
      // Find active tab key
      const tabs = { '🏠': 'home', '📦': 'cate', '⚡': 'flash', '💬': 'chat', '👤': 'mine' };
      renderBottomNav(tabs[activeTab] || 'home');
      langDropdown.classList.remove('show');
      // Update dropdown active state
      langDropdown.querySelectorAll('.lang-option').forEach(o => o.classList.toggle('active', o.dataset.lang === currentLang));
      document.getElementById('currentLang').textContent = langLabels[currentLang] || '🇨🇳';
    });
  });
}

// ========== 商品分类 ==========
export function getShopCategory(name) {
  const n = (name || '').toLowerCase();
  if (n.includes('鱼缸') || n.includes('666')) return 'cabinet';
  if (n.includes('衣帽') || n.includes('衣柜') || n.includes('整体衣柜')) return 'wardrobe';
  if (n.includes('橱柜') || n.includes('厨')) return 'kitchen';
  return 'custom';
}

// ========== 加载商品 ==========
export async function loadProducts() {
  try {
    const res = await fetch(`${API_BASE}/products`);
    return (await res.json()).filter(p => !p.status || p.status === 'active');
  } catch (e) {
    console.error('加载商品失败:', e);
    return [];
  }
}
