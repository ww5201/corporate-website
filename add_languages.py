import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 定义新语言翻译
new_languages = '''      ja: {
        nav_home: 'ホーム', nav_about: '会社概要', nav_services: 'サービス', nav_products: '製品', nav_portfolio: '実績', nav_contact: 'お問い合わせ',
        hero_badge: '匠の技 · 卓越', hero_title: 'あなたの<br><em>理想の生活空間</em>を創る', hero_sub: '高級カスタム家具 · 全てのディテールがアート',
        hero_btn_products: '製品を見る', hero_btn_contact: 'デザイン予約 →',
        about_badge: '会社概要', about_title: '十年の匠の技<br>理想の暮らしをカスタム', about_desc: '卓翌カスタムは高級カスタム家具に特化し、精湛な技術と革新的なデザインで、全てのお客様にユニークな生活空間を提供します。家は住む場所だけでなく、生活態度の表現だと信じています。',
        stat_years: '年の経験', stat_clients: '世帯サービス', stat_satisfaction: '満足度 %',
        quality_title: '品質保証', quality_desc: '3年保証',
        services_label: 'OUR SERVICES', services_title: 'サービス内容', services_desc: 'デザインから設置まで、完全1対1の専属サービス',
        service_wardrobe: 'ウォードローブ', service_wardrobe_desc: 'スペースに合わせた<br>完璧な収納ソリューション',
        service_cloakroom: 'ウォークインクローゼット', service_cloakroom_desc: 'ラグジュアリークローゼット<br>非凡な品質を体験',
        service_kitchen: 'キッチンキャビネット', service_kitchen_desc: 'ハイエンドキッチンソリューション<br>機能と美学の融合',
        service_whole: '全屋カスタム', service_whole_desc: 'ワンストップ全屋カスタム<br>理想の家を創造',
        products_label: 'PRODUCTS', products_title: '製品展示', products_desc: '全ての作品が匠の技と美学の融合',
        portfolio_label: 'PORTFOLIO', portfolio_title: '主要プロジェクト', portfolio_desc: 'お客様のために創造した夢の空間をご覧ください',
        contact_label: 'CONTACT US', contact_title: 'お問い合わせ',
        contact_addr_title: '住所', contact_addr: '広西チワン族自治区南寧市江南区<br>那洪大道留村路 1-2 号',
        contact_phone_title: '電話', contact_phone: '+86 189 7712 2166',
        contact_email_title: 'メール', contact_email: '2841327487@qq.com',
        contact_wechat_title: 'WeChat', contact_wechat: 'WeChatをスキャンして相談',
        contact_form_title: 'メッセージを送る', form_name: 'お名前', form_phone: '電話番号', form_msg: 'お客様のニーズをお聞かせください（間取り、サイズ、カスタムタイプなど）...', form_submit: '送信',
        footer_products: '製品', footer_about: '会社概要', footer_contact: 'お問い合わせ',
        footer_p1: 'ウォードローブ', footer_p2: 'クローゼット', footer_p3: 'キッチン', footer_p4: '全屋',
        footer_a1: '会社紹介', footer_a2: '実績', footer_a3: 'お問い合わせ',
        copyright: '© 2026 卓翌カスタム All Rights Reserved.',
        mobile_home: 'ホーム', mobile_products: '製品', mobile_consult: '相談'
      },
      ko: {
        nav_home: '홈', nav_about: '회사소개', nav_services: '서비스', nav_products: '제품', nav_portfolio: '실적', nav_contact: '문의',
        hero_badge: '장인정신 · 탁월함', hero_title: '당신의<br><em>이상적인 생활 공간</em>을 만듭니다', hero_sub: '프리미엄 커스텀 가구 · 모든 디테일이 예술',
        hero_btn_products: '제품 보기', hero_btn_contact: '디자인 예약 →',
        about_badge: '회사소개', about_title: '10년의 장인정신<br>이상적인 생활을 커스터마이징', about_desc: '쭈이 커스텀은 고급 커스텀 가구 분야에 전문화되어 있으며, 정교한 기술과 혁신적인 디자인으로 모든 고객에게 독특한 생활 공간을 제공합니다. 집은 단순한 거주 공간이 아니라 생활 태도의 표현이라고 믿습니다.',
        stat_years: '년 경력', stat_clients: '가정 서비스', stat_satisfaction: '만족도 %',
        quality_title: '품질 보증', quality_desc: '3년 보증',
        services_label: 'OUR SERVICES', services_title: '서비스 내용', services_desc: '디자인에서 설치까지 전담 1:1 서비스',
        service_wardrobe: '워드로브', service_wardrobe_desc: '공간에 맞춘<br>완벽한 수납 솔루션',
        service_cloakroom: '워크인 클로젯', service_cloakroom_desc: '럭셔리 클로젯 커스터마이징<br>뛰어난 품질 경험',
        service_kitchen: '키장', service_kitchen_desc: '하이엔드 키친 솔루션<br>기능과 미학의 조화',
        service_whole: '전체 홈 커스텀', service_whole_desc: '원스톱 전체 홈 커스텀<br>이상적인 집 만들기',
        products_label: 'PRODUCTS', products_title: '제품 전시', products_desc: '모든 작품이 장인정신과 미학의 융합',
        portfolio_label: 'PORTFOLIO', portfolio_title: '주요 프로젝트', portfolio_desc: '고객을 위해 만든 꿈의 공간을 확인하세요',
        contact_label: 'CONTACT US', contact_title: '문의하기',
        contact_addr_title: '주소', contact_addr: '광서壯族自治区 난닝시 장난구<br>나홍대로 류촌로 1-2호',
        contact_phone_title: '전화', contact_phone: '+86 189 7712 2166',
        contact_email_title: '이메일', contact_email: '2841327487@qq.com',
        contact_wechat_title: '위챗', contact_wechat: '위챗 스캔하여 상담',
        contact_form_title: '메시지 보내기', form_name: '이름', form_phone: '전화번호', form_msg: '고객의 니즈를 알려주세요 (평수, 크기, 커스텀 유형 등)...', form_submit: '전송',
        footer_products: '제품', footer_about: '회사소개', footer_contact: '문의',
        footer_p1: '워드로브', footer_p2: '클로젯', footer_p3: '키장', footer_p4: '전체 홈',
        footer_a1: '회사 소개', footer_a2: '실적', footer_a3: '문의',
        copyright: '© 2026 쭈이 커스텀 All Rights Reserved.',
        mobile_home: '홈', mobile_products: '제품', mobile_consult: '상담'
      },
      th: {
        nav_home: 'หน้าแรก', nav_about: 'เกี่ยวกับเรา', nav_services: 'บริการ', nav_products: 'สินค้า', nav_portfolio: 'ผลงาน', nav_contact: 'ติดต่อ',
        hero_badge: 'ฝีมือช่าง · ยอดเยี่ยม', hero_title: 'สร้าง<br><em>พื้นที่อยู่อาศัยในฝัน</em>ของคุณ', hero_sub: 'เฟอร์นิเจอร์สั่งทำระดับพรีเมียม · ทุกรายละเอียดคืองานศิลปะ',
        hero_btn_products: 'ดูสินค้า', hero_btn_contact: 'จองออกแบบ →',
        about_badge: 'เกี่ยวกับเรา', about_title: 'ฝีมือช่าง 10 ปี<br>สร้างบ้านในฝันของคุณ', about_desc: 'จ่วนอี้ คัสตอมเชี่ยวชาญเฟอร์นิเจอร์สั่งทำระดับไฮเอนด์ ด้วยฝีมือช่างที่ประณีตและออกแบบที่สร้างสรรค์ เพื่อมอบพื้นที่อยู่อาศัยที่ไม่เหมือนใครให้ลูกค้าทุกคน เราเชื่อว่าบ้านไม่ใช่แค่ที่อยู่อาศัย แต่เป็นการแสดงออกถึงวิถีชีวิต',
        stat_years: 'ปีประสบการณ์', stat_clients: 'ครัวเรือนที่ให้บริการ', stat_satisfaction: 'ความพึงพอใจ %',
        quality_title: 'รับประกันคุณภาพ', quality_desc: 'รับประกัน 3 ปี',
        services_label: 'OUR SERVICES', services_title: 'บริการของเรา', services_desc: 'บริการเฉพาะด้าน ตั้งแต่การออกแบบจนถึงติดตั้ง',
        service_wardrobe: 'ตู้เสื้อผ้า', service_wardrobe_desc: 'ออกแบบตามพื้นที่<br>โซลูชันจัดเก็บที่สมบูรณ์แบบ',
        service_cloakroom: 'ตู้เสื้อผ้าแบบเดินเข้าได้', service_cloakroom_desc: 'ตู้เสื้อผ้าหรูสั่งทำ<br>ประสบการณ์คุณภาพเยี่ยม',
        service_kitchen: 'ตู้ครัว', service_kitchen_desc: 'โซลูชันครัวระดับไฮเอนด์<br>ฟังก์ชันผสานความงาม',
        service_whole: 'สั่งทำทั้งบ้าน', service_whole_desc: 'สั่งทำทั้งบ้านครบวงจร<br>สร้างบ้านในฝัน',
        products_label: 'PRODUCTS', products_title: 'แสดงสินค้า', products_desc: 'ทุกชิ้นคือการผสานฝีมือช่างและความงาม',
        portfolio_label: 'PORTFOLIO', portfolio_title: 'โครงการสำคัญ', portfolio_desc: 'ดูพื้นที่ในฝันที่เราสร้างให้ลูกค้า',
        contact_label: 'CONTACT US', contact_title: 'ติดต่อเรา',
        contact_addr_title: 'ที่อยู่', contact_addr: 'ถนนน่าหงง ตำบลหลิวชุน เขตเจียงหนาน<br>เมืองหนานหนิง มณฑลกว่างซี',
        contact_phone_title: 'โทรศัพท์', contact_phone: '+86 189 7712 2166',
        contact_email_title: 'อีเมล', contact_email: '2841327487@qq.com',
        contact_wechat_title: 'WeChat', contact_wechat: 'สแกน WeChat เพื่อปรึกษา',
        contact_form_title: 'ส่งข้อความ', form_name: 'ชื่อของคุณ', form_phone: 'หมายเลขโทรศัพท์', form_msg: 'กรุณาระบุความต้องการของคุณ (ขนาดห้อง, ประเภทสั่งทำ ฯลฯ)...', form_submit: 'ส่ง',
        footer_products: 'สินค้า', footer_about: 'เกี่ยวกับเรา', footer_contact: 'ติดต่อ',
        footer_p1: 'ตู้เสื้อผ้า', footer_p2: 'ตู้เสื้อผ้า', footer_p3: 'ตู้ครัว', footer_p4: 'ทั้งบ้าน',
        footer_a1: 'เกี่ยวกับบริษัท', footer_a2: 'ผลงาน', footer_a3: 'ติดต่อ',
        copyright: '© 2026 จ่วนอี้ คัสตอม สงวนลิขสิทธิ์',
        mobile_home: 'หน้าแรก', mobile_products: 'สินค้า', mobile_consult: 'ปรึกษา'
      },
      vi: {
        nav_home: 'Trang chủ', nav_about: 'Giới thiệu', nav_services: 'Dịch vụ', nav_products: 'Sản phẩm', nav_portfolio: 'Dự án', nav_contact: 'Liên hệ',
        hero_badge: 'Tay nghề thủ công · Xuất sắc', hero_title: 'Tạo ra<br><em>không gian sống mơ ước</em> của bạn', hero_sub: 'Nội thất đặt làm cao cấp · Mọi chi tiết là nghệ thuật',
        hero_btn_products: 'Xem sản phẩm', hero_btn_contact: 'Đặt lịch thiết kế →',
        about_badge: 'Giới thiệu', about_title: 'Thập kỷ tay nghề thủ công<br>Tạo nên ngôi nhà lý tưởng', about_desc: 'Trác Dĩ Chuyên sâu vào nội thất đặt làm cao cấp, với tay nghề thủ công tinh xảo và thiết kế sáng tạo, mang đến không gian sống độc đáo cho mỗi khách hàng. Chúng tôi tin rằng ngôi nhà không chỉ là nơi ở, mà còn là biểu hiện của phong cách sống.',
        stat_years: 'năm kinh nghiệm', stat_clients: 'hộ gia đình phục vụ', stat_satisfaction: 'Độ hài lòng %',
        quality_title: 'Bảo đảm chất lượng', quality_desc: 'Bảo hành 3 năm',
        services_label: 'OUR SERVICES', services_title: 'Dịch vụ của chúng tôi', services_desc: 'Dịch vụ chuyên biệt 1-1 từ thiết kế đến lắp đặt',
        service_wardrobe: 'Tủ quần áo', service_wardrobe_desc: 'Tùy chỉnh theo không gian<br>Giải pháp lưu trữ hoàn hảo',
        service_cloakroom: 'Tủ quần áo đi bộ', service_cloakroom_desc: 'Tủ quần áo cao cấp đặt làm<br>Trải nghiệm chất lượng tuyệt vời',
        service_kitchen: 'Tủ bếp', service_kitchen_desc: 'Giải pháp bếp cao cấp<br>Chức năng kết hợp thẩm mỹ',
        service_whole: 'Nội thất toàn nhà', service_whole_desc: 'Nội thất toàn nhà một cửa<br>Tạo ngôi nhà lý tưởng',
        products_label: 'PRODUCTS', products_title: 'Triển lãm sản phẩm', products_desc: 'Mỗi tác phẩm là sự kết hợp giữa tay nghề thủ công và nghệ thuật',
        portfolio_label: 'PORTFOLIO', portfolio_title: 'Dự án tiêu biểu', portfolio_desc: 'Xem không gian mơ ước mà chúng tôi đã tạo cho khách hàng',
        contact_label: 'CONTACT US', contact_title: 'Liên hệ với chúng tôi',
        contact_addr_title: 'Địa chỉ', contact_addr: 'Đường Naphong, Thôn Lưu Thôn, Quận Giang Nam<br>Thành phố Nam Ninh, Quảng Tây',
        contact_phone_title: 'Điện thoại', contact_phone: '+86 189 7712 2166',
        contact_email_title: 'Email', contact_email: '2841327487@qq.com',
        contact_wechat_title: 'WeChat', contact_wechat: 'Quét WeChat để tư vấn',
        contact_form_title: 'Gửi tin nhắn', form_name: 'Họ tên', form_phone: 'Số điện thoại', form_msg: 'Vui lòng mô tả nhu cầu của bạn (diện tích phòng, loại đặt làm...)', form_submit: 'Gửi',
        footer_products: 'Sản phẩm', footer_about: 'Giới thiệu', footer_contact: 'Liên hệ',
        footer_p1: 'Tủ quần áo', footer_p2: 'Tủ quần áo', footer_p3: 'Tủ bếp', footer_p4: 'Toàn nhà',
        footer_a1: 'Giới thiệu công ty', footer_a2: 'Dự án', footer_a3: 'Liên hệ',
        copyright: '© 2026 Trác Dĩ Chuyênสง giữ bản quyền',
        mobile_home: 'Trang chủ', mobile_products: 'Sản phẩm', mobile_consult: 'Tư vấn'
      },
      ms: {
        nav_home: 'Utama', nav_about: 'Tentang Kami', nav_services: 'Perkhidmatan', nav_products: 'Produk', nav_portfolio: 'Portfolio', nav_contact: 'Hubungi',
        hero_badge: 'Kraf Tangan · Kecemerlangan', hero_title: 'Mencipta<br><em>Ruang Hidup Impian</em> Anda', hero_sub: 'Perabot Tersuai Premium · Setiap Butiran Adalah Seni',
        hero_btn_products: 'Lihat Produk', hero_btn_contact: 'Tempah Reka Bentuk →',
        about_badge: 'Tentang Kami', about_title: 'Dekad Kraf Tangan<br>Mencipta Rumah Impian Anda', about_desc: 'Zhuoyi Custom pakar dalam perabot tersuai mewah, dengan kraf tangan yang halus dan reka bentuk inovatif, menyediakan ruang hidup unik untuk setiap pelanggan. Kami percaya rumah bukan sahaja tempat tinggal, tetapi juga ekspresi gaya hidup.',
        stat_years: 'Tahun Pengalaman', stat_clients: 'Keluarga Dilayani', stat_satisfaction: 'Kepuasan %',
        quality_title: 'Jaminan Kualiti', quality_desc: 'Jaminan 3 Tahun',
        services_label: 'OUR SERVICES', services_title: 'Perkhidmatan Kami', services_desc: 'Perkhidmatan eksklusif 1-1 dari reka bentuk hingga pemasangan',
        service_wardrobe: 'Almiari', service_wardrobe_desc: 'Dilakukan mengikut ruang<br>Penyelesaian penyimpanan sempurna',
        service_cloakroom: ' almari pakaian berjalan', service_cloakroom_desc: 'almari pakaian mewah tersuai<br>Pengalaman kualiti luar biasa',
        service_kitchen: 'Kabinet Dapur', service_kitchen_desc: 'Penyelesaian dapur mewah<br>Fungsi bertemu estetika',
        service_whole: 'Tersuai Rumah Penuh', service_whole_desc: 'Satu hentian tersuai rumah penuh<br>Cipta rumah impian',
        products_label: 'PRODUCTS', products_title: 'Pameran Produk', products_desc: 'Setiap hasil adalah gabungan kraf tangan dan estetika',
        portfolio_label: 'PORTFOLIO', portfolio_title: 'Projek Utama', portfolio_desc: 'Lihat ruang impian yang kami cipta untuk pelanggan',
        contact_label: 'CONTACT US', contact_title: 'Hubungi Kami',
        contact_addr_title: 'Alamat', contact_addr: 'Jalan Liucun, Dao Naphong, Daerah Jiangnan<br>Nanning, Guangxi',
        contact_phone_title: 'Telefon', contact_phone: '+86 189 7712 2166',
        contact_email_title: 'Emel', contact_email: '2841327487@qq.com',
        contact_wechat_title: 'WeChat', contact_wechat: 'Imbas WeChat untuk bermesyuarat',
        contact_form_title: 'Hantar Mesej', form_name: 'Nama Anda', form_phone: 'Nombor Telefon', form_msg: 'Sila nyatakan keperluan anda (saiz bilik, jenis tersuai...)', form_submit: 'Hantar',
        footer_products: 'Produk', footer_about: 'Tentang Kami', footer_contact: 'Hubungi',
        footer_p1: 'Almiari', footer_p2: 'Almari Pakaian', footer_p3: 'Kabinet Dapur', footer_p4: 'Rumah Penuh',
        footer_a1: 'Tentang Syarikat', footer_a2: 'Portfolio', footer_a3: 'Hubungi',
        copyright: '© 2026 Zhuoyi Custom Hak Cipta Terpelihara.',
        mobile_home: 'Utama', mobile_products: 'Produk', mobile_consult: 'Rundingan'
      },
     '''

# 在 en 语言块结束后插入新语言
old_en_end = '''        mobile_home: 'Home', mobile_products: 'Products', mobile_consult: 'Consult'
      }
    };'''

new_en_end = '''        mobile_home: 'Home', mobile_products: 'Products', mobile_consult: 'Consult'
      },
''' + new_languages + '''    };'''

html = html.replace(old_en_end, new_en_end)

# 更新语言切换按钮 HTML
old_lang_btns = '''<button class="lang-btn active" onclick="setLang('zh')">中文</button>
        <button class="lang-btn" onclick="setLang('en')">EN</button>'''

new_lang_btns = '''<button class="lang-btn active" onclick="setLang('zh')">中文</button>
        <button class="lang-btn" onclick="setLang('en')">EN</button>
        <button class="lang-btn" onclick="setLang('ja')">日本語</button>
        <button class="lang-btn" onclick="setLang('ko')">한국어</button>
        <button class="lang-btn" onclick="setLang('th')">ไทย</button>
        <button class="lang-btn" onclick="setLang('vi')">Tiếng Việt</button>
        <button class="lang-btn" onclick="setLang('ms')">Melayu</button>'''

html = html.replace(old_lang_btns, new_lang_btns)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added 5 new languages: Japanese, Korean, Thai, Vietnamese, Malay")

# 上传
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()
ssh.exec_command("nginx -s reload")
ssh.close()
print("Uploaded!")
