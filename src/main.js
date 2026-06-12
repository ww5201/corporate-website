// 卓翌定制 - 拼多多风格电商主页 JavaScript
const API_BASE = '/api';

// ========== 多语言翻译 ==========
const translations = {
  zh: {
    'search.placeholder': '搜索商品',
    'nav.home': '首页', 'nav.about': '关于我们', 'nav.services': '服务',
    'nav.products': '产品', 'nav.contact': '联系', 'nav.shop': '商品',
    'banner.s1.title': '全屋定制 工厂直供', 'banner.s1.desc': '品质家居 · 低至3折起', 'banner.s1.tag': '限时特惠',
    'banner.s2.title': '新品上市 橱柜系列', 'banner.s2.desc': '设计师联名 · 限量特惠', 'banner.s2.tag': '新品首发',
    'banner.s3.title': '拼团更优惠', 'banner.s3.desc': '万人团购 · 价格直降到底', 'banner.s3.tag': '万人团',
    'cat.all': '全部', 'cat.cabinet': '柜类', 'cat.wardrobe': '衣柜', 'cat.kitchen': '橱柜',
    'cat.custom': '定制', 'cat.flash': '秒杀', 'cat.group': '拼团', 'cat.contact': '联系',
    'flash.title': '限时秒杀', 'flash.ends': '距结束', 'flash.more': '更多 ›',
    'group.title': '万人拼团', 'group.badge': '超值低价', 'group.more': '更多 ›', 'group.joined': '人已拼',
    'rec.title': '为你推荐',
    'shop.title': '精选商品', 'shop.desc': '甄选好物，品质生活从这里开始',
    'shop.cat.all': '全部', 'shop.cat.cabinet': '柜类', 'shop.cat.wardrobe': '衣柜',
    'shop.cat.kitchen': '橱柜', 'shop.cat.custom': '定制',
    'shop.inquire': '立即咨询', 'shop.price': '起', 'shop.empty': '暂无商品',
    'pc.group_price': '拼团价', 'pc.single_price': '单买价', 'pc.sold': '已拼',
    'pc.coupon': '领券', 'pc.free_ship': '包邮', 'pc.refund': '退',
    'hero.title': '追求卓越<br><span>定义奢华</span>',
    'hero.subtitle': '我们以匠心精神，为高端客户提供极致体验',
    'hero.cta': '开始合作', 'hero.scroll': '探索更多',
    'about.title': '关于我们',
    'about.lead': '超过二十年的行业沉淀，我们始终坚持品质至上的理念。',
    'about.desc': '我们致力于为追求卓越的客户提供量身定制的解决方案，每一个项目都倾注我们的匠心与热情。',
    'about.stat1': '行业经验', 'about.stat2': '成功案例', 'about.stat3': '客户满意度',
    'services.title': '我们的服务',
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
    'tab.inquire': '立即咨询', 'tab.pay': '立即订购',
    'modal.msg': '留言（选填）',
    'pay.name': '您的姓名', 'pay.phone': '联系电话', 'pay.addr': '收货地址', 'pay.note': '备注',
    'pay.total': '订单金额', 'pay.loading': '加载支付方式...',
    'pay.hint': '扫码付款后，点击确认', 'pay.confirm': '确认已支付',
    'pay.required': '请填写姓名和电话', 'pay.success': '订单已提交！我们会尽快确认。',
    'pay.none': '暂未配置支付方式', 'pay.error': '加载失败',
    'bnav.home': '首页', 'bnav.cate': '分类', 'bnav.flash': '秒杀', 'bnav.chat': '联系', 'bnav.mine': '我的'
  },
  en: {
    'search.placeholder': 'Search products',
    'nav.home': 'Home', 'nav.about': 'About', 'nav.services': 'Services',
    'nav.products': 'Products', 'nav.contact': 'Contact', 'nav.shop': 'Shop',
    'banner.s1.title': 'Custom Furniture Factory Direct', 'banner.s1.desc': 'Quality Home · Up to 70% Off', 'banner.s1.tag': 'Flash Deal',
    'banner.s2.title': 'New Arrival Cabinet Series', 'banner.s2.desc': 'Designer Collab · Limited Edition', 'banner.s2.tag': 'New',
    'banner.s3.title': 'Group Buy & Save More', 'banner.s3.desc': '10K+ Group · Rock Bottom Prices', 'banner.s3.tag': 'Group Deal',
    'cat.all': 'All', 'cat.cabinet': 'Cabinets', 'cat.wardrobe': 'Wardrobes', 'cat.kitchen': 'Kitchen',
    'cat.custom': 'Custom', 'cat.flash': 'Flash', 'cat.group': 'Group', 'cat.contact': 'Contact',
    'flash.title': 'Flash Sale', 'flash.ends': 'Ends in', 'flash.more': 'More ›',
    'group.title': 'Group Buy', 'group.badge': 'Best Value', 'group.more': 'More ›', 'group.joined': 'joined',
    'rec.title': 'Recommended',
    'shop.title': 'Featured Shop', 'shop.desc': 'Curated picks for quality life',
    'shop.cat.all': 'All', 'shop.cat.cabinet': 'Cabinets', 'shop.cat.wardrobe': 'Wardrobes',
    'shop.cat.kitchen': 'Kitchen', 'shop.cat.custom': 'Custom',
    'shop.inquire': 'Inquire', 'shop.price': 'up', 'shop.empty': 'No items',
    'pc.group_price': 'Group', 'pc.single_price': 'Single', 'pc.sold': 'sold',
    'pc.coupon': 'Coupon', 'pc.free_ship': 'Free Ship', 'pc.refund': 'Return',
    'hero.title': 'Pursue Excellence<br><span>Define Luxury</span>',
    'hero.subtitle': 'Premium experiences with craftsmanship',
    'hero.cta': 'Get Started', 'hero.scroll': 'Explore',
    'about.title': 'About Us',
    'about.lead': 'With over 20 years of experience, quality first.',
    'about.desc': 'Tailored solutions for clients who pursue excellence.',
    'about.stat1': 'Years', 'about.stat2': 'Projects', 'about.stat3': 'Satisfaction',
    'services.title': 'Services',
    'contact.title': 'Contact Us',
    'contact.addr.label': 'Address', 'contact.addr.value': 'Nanning, Guangxi, China',
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
    'tab.inquire': 'Inquire', 'tab.pay': 'Order',
    'modal.msg': 'Message (opt)',
    'pay.name': 'Name', 'pay.phone': 'Phone', 'pay.addr': 'Address', 'pay.note': 'Note',
    'pay.total': 'Total', 'pay.loading': 'Loading...',
    'pay.hint': 'Scan then confirm', 'pay.confirm': 'Confirm',
    'pay.required': 'Name & phone required', 'pay.success': 'Order submitted!',
    'pay.none': 'No payment', 'pay.error': 'Failed',
    'bnav.home': 'Home', 'bnav.cate': 'Category', 'bnav.flash': 'Flash', 'bnav.chat': 'Chat', 'bnav.mine': 'Me'
  },
  ja: {
    'search.placeholder': '商品を検索',
    'nav.home': 'ホーム', 'nav.about': '会社概要', 'nav.services': 'サービス',
    'nav.products': '製品', 'nav.contact': 'お問い合わせ', 'nav.shop': '商品',
    'banner.s1.title': '全屋カスタム 工場直販', 'banner.s1.desc': '高品質 · 最大70%OFF', 'banner.s1.tag': 'タイムセール',
    'banner.s2.title': '新作キャビネット', 'banner.s2.desc': 'デザイナーコラボ · 限定', 'banner.s2.tag': '新着',
    'banner.s3.title': 'グループ購入でお得', 'banner.s3.desc': '万人団 · 最安値', 'banner.s3.tag': '万人団',
    'cat.all': '全て', 'cat.cabinet': 'キャビネット', 'cat.wardrobe': 'ワードローブ', 'cat.kitchen': 'キッチン',
    'cat.custom': 'オーダー', 'cat.flash': 'セール', 'cat.group': '団購', 'cat.contact': '連絡',
    'flash.title': 'タイムセール', 'flash.ends': '終了まで', 'flash.more': 'もっと ›',
    'group.title': 'グループ購入', 'group.badge': '超お得', 'group.more': 'もっと ›', 'group.joined': '人参加',
    'rec.title': 'おすすめ',
    'shop.title': 'おすすめ商品', 'shop.desc': '厳選された逸品',
    'shop.cat.all': '全て', 'shop.cat.cabinet': 'キャビネット', 'shop.cat.wardrobe': 'ワードローブ',
    'shop.cat.kitchen': 'キッチン', 'shop.cat.custom': 'オーダー',
    'shop.inquire': 'お問い合わせ', 'shop.price': '〜', 'shop.empty': '商品なし',
    'pc.group_price': '団購価', 'pc.single_price': '通常価', 'pc.sold': '販売済',
    'pc.coupon': 'クーポン', 'pc.free_ship': '送料無料', 'pc.refund': '返品可',
    'about.title': '会社概要',
    'about.lead': '20年以上の業界経験、品質第一。',
    'about.desc': 'お客様にカスタムソリューションを提供。',
    'about.stat1': '年の経験', 'about.stat2': '完成事例', 'about.stat3': '満足度',
    'contact.title': 'お問い合わせ',
    'contact.addr.label': '住所', 'contact.addr.value': '中国広西壮族自治区南寧市',
    'contact.phone.label': '電話', 'contact.email.label': 'メール',
    'contact.form.name': 'お名前', 'contact.form.email': 'メール',
    'contact.form.message': 'メッセージ', 'contact.form.submit': '送信',
    'product.inquire': 'お問い合わせ', 'product.price': '〜',
    'modal.close': '閉じる', 'modal.title_prefix': '製品詳細',
    'modal.name': 'お名前', 'modal.phone': '電話番号', 'modal.email': 'メール',
    'modal.submit': '送信', 'modal.success': '送信完了！',
    'modal.wechat_pay': 'WeChat Pay', 'modal.alipay': 'Alipay',
    'lightbox.hint': 'クリックで拡大',
    'tab.inquire': 'お問い合わせ', 'tab.pay': '注文',
    'modal.msg': 'メッセージ',
    'pay.name': '名前', 'pay.phone': '電話', 'pay.addr': '住所', 'pay.note': '備考',
    'pay.total': '合計', 'pay.loading': '読込中...', 'pay.hint': 'スキャンして確認',
    'pay.confirm': '確認', 'pay.required': '名前と電話は必須', 'pay.success': '注文完了！',
    'pay.none': '支払い方法なし', 'pay.error': '失敗',
    'bnav.home': 'ホーム', 'bnav.cate': '分類', 'bnav.flash': 'セール', 'bnav.chat': '連絡', 'bnav.mine': 'マイ'
  },
  ko: {
    'search.placeholder': '상품 검색',
    'nav.home': '홈', 'nav.about': '회사소개', 'nav.services': '서비스',
    'nav.products': '제품', 'nav.contact': '연락처', 'nav.shop': '상점',
    'banner.s1.title': '맞춤 가구 공장 직송', 'banner.s1.desc': '최대 70% 할인', 'banner.s1.tag': '타임세일',
    'banner.s2.title': '신상 캐비닛', 'banner.s2.desc': '디자이너 콜라보', 'banner.s2.tag': '신상',
    'banner.s3.title': '공동구매', 'banner.s3.desc': '최저가 도전', 'banner.s3.tag': '만인단',
    'cat.all': '전체', 'cat.cabinet': '캐비닛', 'cat.wardrobe': '옷장', 'cat.kitchen': '주방',
    'cat.custom': '맞춤', 'cat.flash': '세일', 'cat.group': '공구', 'cat.contact': '연락',
    'flash.title': '타임세일', 'flash.ends': '종료까지', 'flash.more': '더보기 ›',
    'group.title': '공동구매', 'group.badge': '초특가', 'group.more': '더보기 ›', 'group.joined': '명 참여',
    'rec.title': '추천',
    'shop.cat.all': '전체', 'shop.cat.cabinet': '캐비닛', 'shop.cat.wardrobe': '옷장',
    'shop.cat.kitchen': '주방', 'shop.cat.custom': '맞춤',
    'shop.inquire': '문의', 'shop.price': '부터', 'shop.empty': '상품 없음',
    'pc.group_price': '공구가', 'pc.single_price': '정상가', 'pc.sold': '판매',
    'pc.coupon': '쿠폰', 'pc.free_ship': '무료배송', 'pc.refund': '반품',
    'about.title': '회사소개',
    'about.lead': '20년 이상 경력, 품질 우선.',
    'about.desc': '고객 맞춤형 솔루션 제공.',
    'about.stat1': '년 경력', 'about.stat2': '프로젝트', 'about.stat3': '만족도',
    'contact.title': '연락처',
    'contact.addr.label': '주소', 'contact.addr.value': '중국 광시 난닝시',
    'contact.phone.label': '전화', 'contact.email.label': '이메일',
    'contact.form.name': '이름', 'contact.form.email': '이메일',
    'contact.form.message': '메시지', 'contact.form.submit': '보내기',
    'product.inquire': '문의하기', 'product.price': '부터',
    'modal.close': '닫기', 'modal.title_prefix': '제품 상세',
    'modal.name': '이름', 'modal.phone': '전화', 'modal.email': '이메일',
    'modal.submit': '제출', 'modal.success': '제출 완료!',
    'tab.inquire': '문의', 'tab.pay': '주문',
    'modal.msg': '메시지',
    'pay.name': '이름', 'pay.phone': '전화', 'pay.addr': '주소', 'pay.note': '메모',
    'pay.total': '합계', 'pay.loading': '로딩...', 'pay.hint': '스캔 후 확인',
    'pay.confirm': '확인', 'pay.required': '필수 입력', 'pay.success': '주문 완료!',
    'pay.none': '결제수단 없음', 'pay.error': '실패',
    'bnav.home': '홈', 'bnav.cate': '카테고리', 'bnav.flash': '세일', 'bnav.chat': '채팅', 'bnav.mine': '마이'
  },
  th: {
    'search.placeholder': 'ค้นหาสินค้า',
    'nav.home': 'หน้าแรก', 'nav.about': 'เกี่ยวกับ', 'nav.services': 'บริการ',
    'nav.products': 'สินค้า', 'nav.contact': 'ติดต่อ', 'nav.shop': 'ร้านค้า',
    'banner.s1.title': 'เฟอร์นิเจอร์สั่งทำ', 'banner.s1.desc': 'ลดสูงสุด 70%', 'banner.s1.tag': 'แฟลชเซล',
    'banner.s2.title': 'ตู้ชุดใหม่', 'banner.s2.desc': 'ดีไซน์พิเศษ', 'banner.s2.tag': 'มาใหม่',
    'banner.s3.title': 'ซื้อกลุ่มถูกกว่า', 'banner.s3.desc': 'กลุ่มหมื่นคน', 'banner.s3.tag': 'ซื้อกลุ่ม',
    'cat.all': 'ทั้งหมด', 'cat.cabinet': 'ตู้', 'cat.wardrobe': 'ตู้เสื้อผ้า', 'cat.kitchen': 'ครัว',
    'cat.custom': 'สั่งทำ', 'cat.flash': 'เซล', 'cat.group': 'กลุ่ม', 'cat.contact': 'ติดต่อ',
    'flash.title': 'แฟลชเซล', 'flash.ends': 'เหลือเวลา', 'flash.more': 'เพิ่มเติม ›',
    'group.title': 'ซื้อกลุ่ม', 'group.badge': 'คุ้มสุด', 'group.more': 'เพิ่มเติม ›', 'group.joined': 'คนร่วม',
    'rec.title': 'แนะนำ',
    'shop.cat.all': 'ทั้งหมด', 'shop.cat.cabinet': 'ตู้', 'shop.cat.wardrobe': 'ตู้เสื้อผ้า',
    'shop.cat.kitchen': 'ครัว', 'shop.cat.custom': 'สั่งทำ',
    'shop.inquire': 'สอบถาม', 'shop.price': 'เริ่ม', 'shop.empty': 'ไม่มีสินค้า',
    'pc.group_price': 'ราคากลุ่ม', 'pc.single_price': 'ราคาเดี่ยว', 'pc.sold': 'ขายแล้ว',
    'pc.coupon': 'คูปอง', 'pc.free_ship': 'ส่งฟรี', 'pc.refund': 'คืนได้',
    'about.title': 'เกี่ยวกับเรา', 'about.lead': 'ประสบการณ์กว่า 20 ปี', 'about.desc': 'โซลูชันเฉพาะสำหรับคุณ',
    'about.stat1': 'ปี', 'about.stat2': 'โครงการ', 'about.stat3': 'ความพึงพอใจ',
    'contact.title': 'ติดต่อเรา',
    'contact.addr.label': 'ที่อยู่', 'contact.addr.value': 'หนานหนิง กว่างซี จีน',
    'contact.phone.label': 'โทร', 'contact.email.label': 'อีเมล',
    'contact.form.name': 'ชื่อ', 'contact.form.email': 'อีเมล', 'contact.form.message': 'ข้อความ',
    'contact.form.submit': 'ส่ง', 'product.inquire': 'สอบถาม', 'product.price': 'เริ่ม',
    'modal.close': 'ปิด', 'modal.title_prefix': 'รายละเอียด',
    'modal.name': 'ชื่อ', 'modal.phone': 'โทร', 'modal.email': 'อีเมล',
    'modal.submit': 'ส่ง', 'modal.success': 'ส่งสำเร็จ!',
    'tab.inquire': 'สอบถาม', 'tab.pay': 'สั่งซื้อ', 'modal.msg': 'ข้อความ',
    'pay.name': 'ชื่อ', 'pay.phone': 'โทร', 'pay.addr': 'ที่อยู่', 'pay.note': 'หมายเหตุ',
    'pay.total': 'รวม', 'pay.loading': 'กำลังโหลด...', 'pay.hint': 'สแกนแล้วยืนยัน',
    'pay.confirm': 'ยืนยัน', 'pay.required': 'กรุณากรอก', 'pay.success': 'สั่งซื้อสำเร็จ!',
    'pay.none': 'ไม่มีช่องทาง', 'pay.error': 'ล้มเหลว',
    'bnav.home': 'หน้าแรก', 'bnav.cate': 'หมวดหมู่', 'bnav.flash': 'เซล', 'bnav.chat': 'แชท', 'bnav.mine': 'ฉัน'
  },
  vi: {
    'search.placeholder': 'Tìm sản phẩm',
    'nav.home': 'Trang chủ', 'nav.about': 'Giới thiệu', 'nav.services': 'Dịch vụ',
    'nav.products': 'Sản phẩm', 'nav.contact': 'Liên hệ', 'nav.shop': 'Cửa hàng',
    'banner.s1.title': 'Nội Thất Đặt Làm', 'banner.s1.desc': 'Giảm đến 70%', 'banner.s1.tag': 'Flash Sale',
    'banner.s2.title': 'Tủ Bếp Mới', 'banner.s2.desc': 'Thiết kế đặc biệt', 'banner.s2.tag': 'Mới',
    'banner.s3.title': 'Mua Nhóm Rẻ Hơn', 'banner.s3.desc': 'Nhóm vạn người', 'banner.s3.tag': 'Mua nhóm',
    'cat.all': 'Tất cả', 'cat.cabinet': 'Tủ', 'cat.wardrobe': 'Tủ áo', 'cat.kitchen': 'Bếp',
    'cat.custom': 'Tùy chỉnh', 'cat.flash': 'Sale', 'cat.group': 'Nhóm', 'cat.contact': 'Liên hệ',
    'flash.title': 'Flash Sale', 'flash.ends': 'Còn lại', 'flash.more': 'Thêm ›',
    'group.title': 'Mua Nhóm', 'group.badge': 'Siêu rẻ', 'group.more': 'Thêm ›', 'group.joined': 'người',
    'rec.title': 'Gợi ý',
    'shop.cat.all': 'Tất cả', 'shop.cat.cabinet': 'Tủ', 'shop.cat.wardrobe': 'Tủ áo',
    'shop.cat.kitchen': 'Bếp', 'shop.cat.custom': 'Tùy chỉnh',
    'shop.inquire': 'Hỏi', 'shop.price': 'từ', 'shop.empty': 'Chưa có',
    'pc.group_price': 'Nhóm', 'pc.single_price': 'Lẻ', 'pc.sold': 'đã bán',
    'pc.coupon': 'Coupon', 'pc.free_ship': 'Free ship', 'pc.refund': 'Trả',
    'about.title': 'Về chúng tôi', 'about.lead': 'Hơn 20 năm kinh nghiệm', 'about.desc': 'Giải pháp riêng cho bạn',
    'about.stat1': 'Năm', 'about.stat2': 'Dự án', 'about.stat3': 'Hài lòng',
    'contact.title': 'Liên hệ',
    'contact.addr.label': 'Địa chỉ', 'contact.addr.value': 'Nam Ninh, Quảng Tây, TQ',
    'contact.phone.label': 'ĐT', 'contact.email.label': 'Email',
    'contact.form.name': 'Họ tên', 'contact.form.email': 'Email', 'contact.form.message': 'Tin nhắn',
    'contact.form.submit': 'Gửi', 'product.inquire': 'Hỏi ngay', 'product.price': 'từ',
    'modal.close': 'Đóng', 'modal.title_prefix': 'Chi tiết',
    'modal.name': 'Họ tên', 'modal.phone': 'SĐT', 'modal.email': 'Email',
    'modal.submit': 'Gửi', 'modal.success': 'Đã gửi!',
    'tab.inquire': 'Hỏi', 'tab.pay': 'Đặt', 'modal.msg': 'Tin nhắn',
    'pay.name': 'Tên', 'pay.phone': 'SĐT', 'pay.addr': 'Địa chỉ', 'pay.note': 'Ghi chú',
    'pay.total': 'Tổng', 'pay.loading': 'Đang tải...', 'pay.hint': 'Quét rồi xác nhận',
    'pay.confirm': 'Xác nhận', 'pay.required': 'Vui lòng nhập', 'pay.success': 'Đặt hàng thành công!',
    'pay.none': 'Chưa có TT', 'pay.error': 'Lỗi',
    'bnav.home': 'Trang chủ', 'bnav.cate': 'Danh mục', 'bnav.flash': 'Sale', 'bnav.chat': 'Chat', 'bnav.mine': 'Tôi'
  },
  ms: {
    'search.placeholder': 'Cari produk',
    'nav.home': 'Utama', 'nav.about': 'Tentang', 'nav.services': 'Perkhidmatan',
    'nav.products': 'Produk', 'nav.contact': 'Hubungi', 'nav.shop': 'Kedai',
    'banner.s1.title': 'Perabot Tersuai Kilang', 'banner.s1.desc': 'Diskaun 70%', 'banner.s1.tag': 'Jualan Kilat',
    'banner.s2.title': 'Kabinet Baru', 'banner.s2.desc': 'Edisi terhad', 'banner.s2.tag': 'Baru',
    'banner.s3.title': 'Beli Kumpulan', 'banner.s3.desc': 'Harga terendah', 'banner.s3.tag': 'Kumpulan',
    'cat.all': 'Semua', 'cat.cabinet': 'Kabinet', 'cat.wardrobe': 'Almari', 'cat.kitchen': 'Dapur',
    'cat.custom': 'Tersuai', 'cat.flash': 'Kilat', 'cat.group': 'Kumpulan', 'cat.contact': 'Hubungi',
    'flash.title': 'Jualan Kilat', 'flash.ends': 'Tamat', 'flash.more': 'Lagi ›',
    'group.title': 'Beli Kumpulan', 'group.badge': 'Jimat', 'group.more': 'Lagi ›', 'group.joined': 'orang',
    'rec.title': 'Disyorkan',
    'shop.cat.all': 'Semua', 'shop.cat.cabinet': 'Kabinet', 'shop.cat.wardrobe': 'Almari',
    'shop.cat.kitchen': 'Dapur', 'shop.cat.custom': 'Tersuai',
    'shop.inquire': 'Tanya', 'shop.price': 'dari', 'shop.empty': 'Tiada',
    'pc.group_price': 'Kumpulan', 'pc.single_price': 'Satu', 'pc.sold': 'dijual',
    'pc.coupon': 'Kupon', 'pc.free_ship': 'Hantar percuma', 'pc.refund': 'Pulang',
    'about.title': 'Tentang Kami', 'about.lead': '20+ tahun pengalaman', 'about.desc': 'Penyelesaian tersuai',
    'about.stat1': 'Tahun', 'about.stat2': 'Projek', 'about.stat3': 'Puas hati',
    'contact.title': 'Hubungi Kami',
    'contact.addr.label': 'Alamat', 'contact.addr.value': 'Nanning, Guangxi, China',
    'contact.phone.label': 'Tel', 'contact.email.label': 'Emel',
    'contact.form.name': 'Nama', 'contact.form.email': 'Emel', 'contact.form.message': 'Mesej',
    'contact.form.submit': 'Hantar', 'product.inquire': 'Tanya', 'product.price': 'dari',
    'modal.close': 'Tutup', 'modal.title_prefix': 'Butiran',
    'modal.name': 'Nama', 'modal.phone': 'Tel', 'modal.email': 'Emel',
    'modal.submit': 'Hantar', 'modal.success': 'Berjaya!',
    'tab.inquire': 'Tanya', 'tab.pay': 'Pesan', 'modal.msg': 'Mesej',
    'pay.name': 'Nama', 'pay.phone': 'Tel', 'pay.addr': 'Alamat', 'pay.note': 'Nota',
    'pay.total': 'Jumlah', 'pay.loading': 'Memuatkan...', 'pay.hint': 'Imbas & sahkan',
    'pay.confirm': 'Sahkan', 'pay.required': 'Sila isi', 'pay.success': 'Pesanan berjaya!',
    'pay.none': 'Tiada bayaran', 'pay.error': 'Gagal',
    'bnav.home': 'Utama', 'bnav.cate': 'Kategori', 'bnav.flash': 'Kilat', 'bnav.chat': 'Chat', 'bnav.mine': 'Saya'
  }
};

const langLabels = {
  zh: '🇨🇳', en: '🇺🇸', ja: '🇯🇵',
  ko: '🇰🇷', th: '🇹🇭', vi: '🇻🇳', ms: '🇲🇾'
};

// ========== 产品名称翻译 ==========
const productNames = {
  zh: { '鱼缸柜': '鱼缸柜', '柜子': '柜子', '橱柜定制': '橱柜定制', '衣帽间定制': '衣帽间定制', '整体衣柜定制': '整体衣柜定制', '666': '666' },
  en: { '鱼缸柜': 'Fish Tank Cabinet', '柜子': 'Cabinet', '橱柜定制': 'Kitchen Cabinet', '衣帽间定制': 'Walk-in Closet', '整体衣柜定制': 'Wardrobe', '666': '666' },
  ja: { '鱼缸柜': '魚棚キャビネット', '柜子': 'キャビネット', '橱柜定制': 'システムキッチン', '衣帽间定制': 'ウォークインクローゼット', '整体衣柜定制': 'ワードローブ', '666': '666' },
  ko: { '鱼缸柜': '수족관 캐비닛', '柜子': '캐비닛', '橱柜定制': '주방 캐비닛', '衣帽间定制': '워크인 클로젯', '整体衣柜定制': '워드로브', '666': '666' },
  th: { '鱼缸柜': 'ตู้ปลา', '柜子': 'ตู้', '橱柜定制': 'ตู้ครัว', '衣帽间定制': 'ตู้เสื้อผ้าWalk-in', '整体衣柜定制': 'ตู้เสื้อผ้า', '666': '666' },
  vi: { '鱼缸柜': 'Tủ Bể Cá', '柜子': 'Tủ', '橱柜定制': 'Tủ Bếp', '衣帽间定制': 'Tủ Quần Áo', '整体衣柜定制': 'Tủ Đồ', '666': '666' },
  ms: { '鱼缸柜': 'Kabinet Akuarium', '柜子': 'Kabinet', '橱柜定制': 'Kabinet Dapur', '衣帽间定制': 'Wardrobe Walk-in', '整体衣柜定制': 'Wardrobe', '666': '666' }
};
const productDescs = {
  zh: { '鱼缸柜': '精美鱼缸柜定制', '柜子': '多功能柜子定制', '橱柜定制': '高端整体橱柜定制', '衣帽间定制': '豪华衣帽间定制', '整体衣柜定制': '全屋整体衣柜定制' },
  en: { '鱼缸柜': 'Custom Fish Tank Cabinet', '柜子': 'Multi-purpose Cabinet', '橱柜定制': 'Premium Kitchen Cabinet', '衣帽间定制': 'Luxury Walk-in Closet', '整体衣柜定制': 'Custom Wardrobe System' },
  ja: { '鱼缸柜': 'カスタム魚棚キャビネット', '柜子': '多目的キャビネット', '橱柜定制': 'プレミアムシステムキッチン', '衣帽间定制': 'ラグジュアリーウォークイン', '整体衣柜定制': 'カスタムワードローブ' },
  ko: { '鱼缸柜': '맞춤 수족관 캐비닛', '柜子': '다용도 캐비닛', '橱柜定制': '프리미엄 주방 캐비닛', '衣帽间定制': '럭셔리 워크인 클로젯', '整体衣柜定制': '맞춤 워드로브' },
  th: { '鱼缸柜': 'ตู้ปลาสั่งทำ', '柜子': 'ตู้อเนกประสงค์', '橱柜定制': 'ตู้ครัวพรีเมียม', '衣帽间定制': 'ตู้เสื้อผ้าหรู', '整体衣柜定制': 'ตู้เสื้อผ้าสั่งทำ' },
  vi: { '鱼缸柜': 'Tủ Bể Cá Đặt Làm', '柜子': 'Tủ Đa Năng', '橱柜定制': 'Tủ Bếp Cao Cấp', '衣帽间定制': 'Tủ Quần Áo Sang Trọng', '整体衣柜定制': 'Tủ Đồ Theo Yêu Cầu' },
  ms: { '鱼缸柜': 'Kabinet Akuarium Tersuai', '柜子': 'Kabinet Serbaguna', '橱柜定制': 'Kabinet Dapur Premium', '衣帽间定制': 'Wardrobe Mewah', '整体衣柜定制': 'Wardrobe Tersuai' }
};

function trProductName(name) {
  const lang = productNames[currentLang] || productNames.zh;
  return lang[name] || name;
}
function trProductDesc(name) {
  const lang = productDescs[currentLang] || productDescs.zh;
  return lang[name] || '';
}

// ========== 全局状态 ==========
let currentLang = localStorage.getItem('lang') || 'zh';
let allProducts = [];
let currentCat = 'all';
let bannerIdx = 0;
let bannerTimer = null;

// ========== 语言切换 ==========
function applyLang(lang) {
  currentLang = lang;
  localStorage.setItem('lang', lang);
  const t = translations[lang] || translations.zh;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.innerHTML = t[key];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });

  document.getElementById('currentLang').textContent = langLabels[lang] || langLabels.zh;
  document.getElementById('langDropdown').querySelectorAll('.lang-option').forEach(opt => {
    opt.classList.toggle('active', opt.dataset.lang === lang);
  });

  renderAllProducts();
}

// ========== 语言切换器 ==========
const langBtn = document.getElementById('langBtn');
const langDropdown = document.getElementById('langDropdown');
langBtn.addEventListener('click', e => {
  e.stopPropagation();
  langDropdown.classList.toggle('show');
});
document.addEventListener('click', () => langDropdown.classList.remove('show'));
langDropdown.querySelectorAll('.lang-option').forEach(opt => {
  opt.addEventListener('click', () => {
    applyLang(opt.dataset.lang);
    langDropdown.classList.remove('show');
  });
});

// ========== 轮播 ==========
function initBanner() {
  const track = document.getElementById('bannerTrack');
  const dots = document.getElementById('bannerDots');
  if (!track || !dots) return;
  const slides = track.querySelectorAll('.pdd-banner-slide');
  if (slides.length === 0) return;

  function goTo(idx) {
    bannerIdx = idx;
    track.style.transform = `translateX(-${idx * 100}%)`;
    dots.querySelectorAll('.pdd-dot').forEach((d, i) => d.classList.toggle('active', i === idx));
  }

  function next() {
    goTo((bannerIdx + 1) % slides.length);
  }

  bannerTimer = setInterval(next, 4000);

  // 触摸滑动
  let startX = 0;
  track.addEventListener('touchstart', e => {
    clearInterval(bannerTimer);
    startX = e.touches[0].clientX;
  }, { passive: true });
  track.addEventListener('touchend', e => {
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      goTo(diff > 0 ? (bannerIdx + 1) % slides.length : (bannerIdx - 1 + slides.length) % slides.length);
    }
    bannerTimer = setInterval(next, 4000);
  }, { passive: true });
}

// ========== 倒计时 ==========
function initCountdown() {
  // 设置到今天结束时间
  const now = new Date();
  const end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);

  function update() {
    const diff = Math.max(0, end - new Date());
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    const cdH = document.getElementById('cdH');
    const cdM = document.getElementById('cdM');
    const cdS = document.getElementById('cdS');
    if (cdH) cdH.textContent = String(h).padStart(2, '0');
    if (cdM) cdM.textContent = String(m).padStart(2, '0');
    if (cdS) cdS.textContent = String(s).padStart(2, '0');
  }
  update();
  setInterval(update, 1000);
}

// ========== 商品分类 ==========
function getShopCategory(name) {
  const n = (name || '').toLowerCase();
  if (n.includes('鱼缸') || n.includes('666')) return 'cabinet';
  if (n.includes('衣帽') || n.includes('衣柜') || n.includes('整体衣柜')) return 'wardrobe';
  if (n.includes('橱柜') || n.includes('厨')) return 'kitchen';
  return 'custom';
}

// ========== 加载商品 ==========
async function loadProducts() {
  try {
    const res = await fetch(`${API_BASE}/products`);
    allProducts = (await res.json()).filter(p => !p.status || p.status === 'active');
    renderAllProducts();
  } catch (e) {
    console.error('加载商品失败:', e);
  }
}

// ========== 渲染所有区域 ==========
function renderAllProducts() {
  renderFlashSale();
  renderGroupBuy();
  renderProductGrid();
}

// ========== 限时秒杀 ==========
function renderFlashSale() {
  const container = document.getElementById('flashScroll');
  if (!container) return;
  const t = translations[currentLang] || translations.zh;

  if (allProducts.length === 0) {
    container.innerHTML = `<div class="pdd-empty">${t['shop.empty'] || '暂无商品'}</div>`;
    return;
  }

  container.innerHTML = allProducts.map((p, i) => {
    const img = p.images && p.images.length > 0 ? p.images[0] : null;
    const price = p.price ? Number(p.price) : 0;
    const flashPrice = Math.round(price * 0.7);
    const discount = p.price ? '7折' : '';
    const soldPct = Math.min(95, 50 + Math.floor(Math.random() * 45));

    return `
      <div class="pdd-flash-card" data-product-idx="${i}">
        <div class="pdd-flash-img">
          ${img ? `<img src="${img}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=image-placeholder></div>'">` : '<div class="image-placeholder"></div>'}
          ${discount ? `<span class="pdd-flash-discount">${discount}</span>` : ''}
        </div>
        <div class="pdd-flash-info">
          <div class="pdd-flash-price">¥${flashPrice.toLocaleString()} <small>${t['shop.price'] || '起'}</small></div>
          ${p.price ? `<div class="pdd-flash-original">¥${price.toLocaleString()}</div>` : ''}
          <div class="pdd-flash-sold">
            <div class="pdd-flash-sold-bar">
              <div class="pdd-flash-sold-fill" style="width:${soldPct}%"></div>
              <span>${soldPct}%</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ========== 万人拼团 ==========
function renderGroupBuy() {
  const container = document.getElementById('groupList');
  if (!container) return;
  const t = translations[currentLang] || translations.zh;

  if (allProducts.length === 0) {
    container.innerHTML = `<div class="pdd-empty">${t['shop.empty'] || '暂无商品'}</div>`;
    return;
  }

  container.innerHTML = allProducts.map((p, i) => {
    const img = p.images && p.images.length > 0 ? p.images[0] : null;
    const price = p.price ? Number(p.price) : 0;
    const groupPrice = Math.round(price * 0.6);
    const joined = 1000 + Math.floor(Math.random() * 9000);

    return `
      <div class="pdd-group-card" data-product-idx="${i}">
        <div class="pdd-group-img">
          ${img ? `<img src="${img}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=image-placeholder></div>'">` : '<div class="image-placeholder"></div>'}
        </div>
        <div class="pdd-group-info">
          <div class="pdd-group-name">${trProductName(p.name)}</div>
          <div class="pdd-group-meta">
            <span class="pdd-group-price">¥${groupPrice.toLocaleString()} <small>${t['shop.price'] || '起'}</small></span>
            ${p.price ? `<span class="pdd-group-orig">¥${price.toLocaleString()}</span>` : ''}
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
            <span class="pdd-group-joined">${joined.toLocaleString()}+ ${t['group.joined'] || '人已拼'}</span>
            <button class="pdd-group-btn" data-product-idx="${i}">${t['shop.inquire'] || '立即咨询'}</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ========== 商品瀑布流（为你推荐） ==========
function renderProductGrid() {
  const grid = document.getElementById('productsGrid');
  if (!grid) return;
  const t = translations[currentLang] || translations.zh;

  let filtered = allProducts;
  if (currentCat !== 'all') {
    filtered = allProducts.filter(p => getShopCategory(p.name) === currentCat);
  }

  if (filtered.length === 0) {
    grid.innerHTML = `<div class="pdd-empty">${t['shop.empty'] || '暂无商品'}</div>`;
    return;
  }

  grid.innerHTML = filtered.map((p) => {
    const realIdx = allProducts.indexOf(p);
    const img = p.images && p.images.length > 0 ? p.images[0] : null;
    const price = p.price ? Number(p.price) : 0;
    const groupPrice = Math.round(price * 0.65);
    const soldNum = 100 + Math.floor(Math.random() * 5000);
    const badges = ['HOT', '爆款', '新品', '推荐'];
    const badge = badges[Math.floor(Math.random() * badges.length)];

    return `
      <div class="pdd-product-card" data-product-idx="${realIdx}">
        <div class="pdd-pc-img">
          ${img ? `<img src="${img}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=image-placeholder></div>'">` : '<div class="image-placeholder"></div>'}
          <span class="pdd-pc-badge">${badge}</span>
          <span class="pdd-pc-coupon">${t['pc.coupon'] || '领券'}</span>
        </div>
        <div class="pdd-pc-body">
          <div class="pdd-pc-title">${trProductName(p.name)} ${trProductDesc(p.name)}</div>
          <div class="pdd-pc-tags">
            <span class="pdd-pc-tag">${t['pc.free_ship'] || '包邮'}</span>
            <span class="pdd-pc-tag green">${t['pc.refund'] || '退'}</span>
          </div>
          <div class="pdd-pc-price-row">
            <span class="pdd-pc-price"><span class="yen">¥</span>${groupPrice.toLocaleString()} <small>${t['shop.price'] || '起'}</small></span>
            <span class="pdd-pc-sold">${soldNum.toLocaleString()}+ ${t['pc.sold'] || '已拼'}</span>
          </div>
          <div class="pdd-pc-group-row">
            <button class="pdd-pc-group-btn primary" data-product-idx="${realIdx}">${t['pc.group_price'] || '拼团价'}</button>
            <button class="pdd-pc-group-btn secondary" data-product-idx="${realIdx}">${t['pc.single_price'] || '单买价'}</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ========== 分类Tab ==========
document.getElementById('filterTabs')?.addEventListener('click', e => {
  const tab = e.target.closest('.pdd-filter-tab');
  if (!tab) return;
  currentCat = tab.dataset.cat;
  document.querySelectorAll('.pdd-filter-tab').forEach(t => t.classList.remove('active'));
  tab.classList.add('active');
  renderProductGrid();
});

// ========== 分类图标点击 ==========
document.querySelector('.pdd-cat-grid')?.addEventListener('click', e => {
  const item = e.target.closest('.pdd-cat-item');
  if (!item) return;

  // 滚动类
  if (item.dataset.scroll) {
    const target = document.getElementById(item.dataset.scroll === 'flash' ? 'flashSale' : item.dataset.scroll === 'group' ? 'groupBuy' : 'contact');
    if (target) target.scrollIntoView({ behavior: 'smooth' });
    return;
  }

  // 分类筛选
  if (item.dataset.cat) {
    currentCat = item.dataset.cat;
    document.querySelectorAll('.pdd-filter-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.cat === currentCat);
    });
    renderProductGrid();
    document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
  }
});

// ========== 商品点击 -> 弹窗 ==========
document.addEventListener('click', e => {
  const card = e.target.closest('.pdd-product-card, .pdd-flash-card, .pdd-group-card, .pdd-group-btn, .pdd-pc-group-btn');
  if (!card) return;
  const idx = parseInt(card.dataset.productIdx);
  if (!isNaN(idx) && allProducts[idx]) {
    showProductModal(allProducts[idx]);
  }
});

// ========== 搜索 ==========
document.getElementById('pddSearchInput')?.addEventListener('input', e => {
  const q = e.target.value.trim().toLowerCase();
  if (!q) {
    renderProductGrid();
    return;
  }
  const grid = document.getElementById('productsGrid');
  if (!grid) return;
  const t = translations[currentLang] || translations.zh;

  const filtered = allProducts.filter(p => {
    const name = trProductName(p.name).toLowerCase();
    const desc = (trProductDesc(p.name) || p.description || '').toLowerCase();
    return name.includes(q) || desc.includes(q);
  });

  if (filtered.length === 0) {
    grid.innerHTML = `<div class="pdd-empty">${t['shop.empty'] || '暂无商品'}</div>`;
    return;
  }

  grid.innerHTML = filtered.map(p => {
    const realIdx = allProducts.indexOf(p);
    const img = p.images && p.images.length > 0 ? p.images[0] : null;
    const price = p.price ? Number(p.price) : 0;
    const groupPrice = Math.round(price * 0.65);
    const soldNum = 100 + Math.floor(Math.random() * 5000);

    return `
      <div class="pdd-product-card" data-product-idx="${realIdx}">
        <div class="pdd-pc-img">
          ${img ? `<img src="${img}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=image-placeholder></div>'">` : '<div class="image-placeholder"></div>'}
          <span class="pdd-pc-badge">HOT</span>
        </div>
        <div class="pdd-pc-body">
          <div class="pdd-pc-title">${trProductName(p.name)} ${trProductDesc(p.name)}</div>
          <div class="pdd-pc-price-row">
            <span class="pdd-pc-price"><span class="yen">¥</span>${groupPrice.toLocaleString()}</span>
            <span class="pdd-pc-sold">${soldNum.toLocaleString()}+ ${t['pc.sold'] || '已拼'}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
});

// ========== 产品弹窗 ==========
function showProductModal(product) {
  const t = translations[currentLang] || translations.zh;
  const images = product.images || [];
  let currentIdx = 0;
  let lightboxOpen = false;
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.innerHTML = `
    <div class="modal-content product-modal">
      <button class="modal-close">&times;</button>
      <h3>${t['modal.title_prefix'] || '产品详情'} - ${trProductName(product.name)}</h3>
      <div class="modal-images">
        ${images.length > 0
          ? `<div class="modal-main-image" id="modalMainImg">
               <img src="${images[0]}" alt="${product.name}" id="modalMainImgTag"
                    onerror="this.parentElement.innerHTML='<div class=image-placeholder></div>'"
                    style="cursor:zoom-in" title="${t['lightbox.hint']||'点击放大'}">
               ${images.length > 1 ? `
                 <button class="img-nav img-nav-prev">&#10094;</button>
                 <button class="img-nav img-nav-next">&#10095;</button>
                 <span class="img-counter">1 / ${images.length}</span>
               ` : ''}
             </div>
             ${images.length > 1 ? `<div class="modal-thumb-strip">${images.map((img,i) => `<img src="${img}" class="modal-thumb ${i===0?'active':''}" data-idx="${i}" alt="">`).join('')}</div>` : ''}`
          : '<div class="image-placeholder" style="height:200px"></div>'}
      </div>
      ${product.price ? `<p class="modal-price">¥ ${Number(product.price).toLocaleString()}</p>` : ''}
      <p class="modal-desc">${trProductDesc(product.name) || product.description || ''}</p>
      <div class="modal-tabs">
        <button class="modal-tab active" data-tab="inquiry">${t['tab.inquire']||'立即咨询'}</button>
        <button class="modal-tab" data-tab="payment">${t['tab.pay']||'立即订购'}</button>
      </div>
      <div class="modal-tab-content active" id="tabInquiry">
        <form class="modal-form" id="inquiryForm">
          <input type="text" placeholder="${t['modal.name']}" required>
          <input type="tel" placeholder="${t['modal.phone']}" required>
          <input type="email" placeholder="${t['modal.email']}">
          <textarea placeholder="${t['modal.msg']||'留言（选填）'}" rows="2"></textarea>
          <button type="submit" class="submit-btn submit-primary">${t['modal.submit']}</button>
        </form>
      </div>
      <div class="modal-tab-content" id="tabPayment" style="display:none">
        <div class="payment-area">
          <div class="pay-order-form">
            <input type="text" placeholder="${t['pay.name']||'您的姓名'}" id="payName" required>
            <input type="tel" placeholder="${t['pay.phone']||'联系电话'}" id="payPhone" required>
            <input type="text" placeholder="${t['pay.addr']||'收货地址'}" id="payAddr">
            <textarea placeholder="${t['pay.note']||'备注'}" id="payNote" rows="2"></textarea>
          </div>
          <div class="pay-qr-section" id="payQrSection">
            <p class="pay-total"><b>${t['pay.total']||'订单金额'}:</b> ¥ ${Number(product.price||0).toLocaleString()}</p>
            <div class="pay-qr-codes" id="payQrCodes">
              <p style="color:#888;text-align:center;padding:20px">${t['pay.loading']||'加载中...'}</p>
            </div>
            <p class="pay-hint">${t['pay.hint']||'扫码付款后，点击确认'}</p>
            <button class="submit-btn submit-pay" id="payConfirmBtn">${t['pay.confirm']||'确认已支付'}</button>
          </div>
        </div>
      </div>
    </div>
    <div class="lightbox-overlay" id="lightboxOverlay" style="display:none">
      <button class="lightbox-close">&times;</button>
      <button class="img-nav lightbox-prev">&#10094;</button>
      <img class="lightbox-img" id="lightboxImg" src="" alt="">
      <button class="img-nav lightbox-next">&#10095;</button>
      <span class="img-counter lightbox-counter" id="lightboxCounter"></span>
    </div>
  `;
  document.body.appendChild(modal);

  function goToImage(idx) {
    if (!images.length) return;
    if (idx < 0) idx = images.length - 1;
    if (idx >= images.length) idx = 0;
    currentIdx = idx;
    const mainImg = document.getElementById('modalMainImgTag');
    if (mainImg && images[idx]) {
      mainImg.src = images[idx];
      modal.querySelectorAll('.modal-thumb').forEach(th => th.classList.remove('active'));
      const activeThumb = modal.querySelector(`.modal-thumb[data-idx="${idx}"]`);
      if (activeThumb) { activeThumb.classList.add('active'); activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' }); }
      const counter = modal.querySelector('.img-counter:not(.lightbox-counter)');
      if (counter) counter.textContent = `${idx + 1} / ${images.length}`;
      if (lightboxOpen) {
        document.getElementById('lightboxImg').src = images[idx];
        document.getElementById('lightboxCounter').textContent = `${idx + 1} / ${images.length}`;
      }
    }
  }

  function closeModal() { modal.remove(); document.removeEventListener('keydown', onKeydown); }
  modal.querySelector('.modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

  modal.querySelectorAll('.img-nav-prev, .img-nav-next').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      goToImage(currentIdx + (btn.classList.contains('img-nav-prev') ? -1 : 1));
    });
  });

  modal.querySelector('.modal-images')?.addEventListener('click', e => {
    const thumb = e.target.closest('.modal-thumb');
    if (!thumb) return;
    goToImage(parseInt(thumb.dataset.idx));
  });

  const mainImgArea = document.getElementById('modalMainImg');
  mainImgArea?.addEventListener('click', () => {
    if (!images.length) return;
    lightboxOpen = true;
    const lb = document.getElementById('lightboxOverlay');
    document.getElementById('lightboxImg').src = images[currentIdx];
    document.getElementById('lightboxCounter').textContent = `${currentIdx + 1} / ${images.length}`;
    lb.style.display = 'flex'; document.body.style.overflow = 'hidden';
  });

  const lightbox = document.getElementById('lightboxOverlay');
  lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
    lightbox.style.display = 'none'; lightboxOpen = false; document.body.style.overflow = '';
  });
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox) { lightbox.style.display = 'none'; lightboxOpen = false; document.body.style.overflow = ''; }
  });

  function onKeydown(e) {
    if (e.key === 'ArrowLeft') goToImage(currentIdx - 1);
    else if (e.key === 'ArrowRight') goToImage(currentIdx + 1);
    else if (e.key === 'Escape') {
      if (lightboxOpen) { lightbox.style.display = 'none'; lightboxOpen = false; document.body.style.overflow = ''; }
      else closeModal();
    }
  }
  document.addEventListener('keydown', onKeydown);

  modal.querySelectorAll('.modal-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      modal.querySelectorAll('.modal-tab').forEach(x => x.classList.remove('active'));
      modal.querySelectorAll('.modal-tab-content').forEach(c => c.style.display = 'none');
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab === 'inquiry' ? 'tabInquiry' : 'tabPayment').style.display = 'block';
      if (tab.dataset.tab === 'payment') loadPaymentQr();
    });
  });

  function loadPaymentQr() {
    const container = document.getElementById('payQrCodes');
    if (container.dataset.loaded) return;
    fetch(`${API_BASE}/payment-config`).then(r => r.json()).then(cfg => {
      container.dataset.loaded = '1';
      let html = '';
      if (cfg.wechatPay) html += `<div class="pay-qr-item"><p>${t['modal.wechat_pay']||'微信支付'}</p><img src="${cfg.wechatPay}" alt="wechat"></div>`;
      if (cfg.alipay) html += `<div class="pay-qr-item"><p>${t['modal.alipay']||'支付宝'}</p><img src="${cfg.alipay}" alt="alipay"></div>`;
      if (!html) html = `<p style="color:#999;text-align:center;padding:10px">${t['pay.none']||'暂未配置支付方式'}</p>`;
      container.innerHTML = html;
    }).catch(() => {
      container.innerHTML = `<p style="color:#999;text-align:center">${t['pay.error']||'加载失败'}</p>`;
    });
  }

  document.getElementById('inquiryForm').addEventListener('submit', async e => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input, textarea');
    try {
      await fetch(`${API_BASE}/messages`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: inputs[0].value, phone: inputs[1].value, email: inputs[2].value, message: inputs[3].value || `产品咨询: ${product.name}`, product: product.name })
      });
      alert(t['modal.success']); closeModal();
    } catch (err) { alert('Error: ' + err.message); }
  });

  document.getElementById('payConfirmBtn').addEventListener('click', async () => {
    const name = document.getElementById('payName').value.trim();
    const phone = document.getElementById('payPhone').value.trim();
    if (!name || !phone) { alert(t['pay.required']||'请填写姓名和电话'); return; }
    try {
      await fetch(`${API_BASE}/orders`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          customerName: name, customerPhone: phone,
          address: document.getElementById('payAddr').value,
          note: document.getElementById('payNote').value,
          productName: product.name, price: product.price, status: 'pending_payment'
        })
      });
      alert(t['pay.success']||'订单已提交！'); closeModal();
    } catch (err) { alert('Error: ' + err.message); }
  });
}

// ========== 联系表单 ==========
document.querySelector('.pdd-contact-form')?.addEventListener('submit', async e => {
  e.preventDefault();
  const t = translations[currentLang] || translations.zh;
  const inputs = e.target.querySelectorAll('input, textarea');
  try {
    await fetch(`${API_BASE}/messages`, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ name: inputs[0].value, email: inputs[1].value, message: inputs[2].value })
    });
    alert(t['modal.success']); e.target.reset();
  } catch (e) { alert('Error: ' + e.message); }
});

// ========== 底部导航高亮 ==========
function updateBottomNav() {
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.pdd-bnav-item');
  let current = '';
  sections.forEach(section => {
    if (section.getBoundingClientRect().top <= 150) current = section.id;
  });
  navItems.forEach(item => {
    item.classList.remove('active');
    const href = item.getAttribute('href');
    if (href === '#' + current) item.classList.add('active');
  });
}
window.addEventListener('scroll', updateBottomNav);

// ========== Header 滚动效果 ==========
window.addEventListener('scroll', () => {
  const header = document.getElementById('pddHeader');
  if (header) header.classList.toggle('scrolled', window.scrollY > 50);
});

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', () => {
  applyLang(currentLang);
  loadProducts();
  initBanner();
  initCountdown();
  console.log('✨ 卓翌定制 - 拼多多风格主页已加载');
});
