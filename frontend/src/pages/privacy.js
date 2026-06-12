/**
 * Privacy Policy Page - 隐私政策
 */

export async function privacyPage() {
  return {
    title: '隐私政策',
    render: () => `
      <div class="page-body" style="padding:16px 20px;max-width:680px;margin:0 auto">
        <div class="privacy-header">
          <a href="#/profile" style="display:inline-flex;align-items:center;color:var(--text-secondary);font-size:14px;text-decoration:none;margin-bottom:12px">
            <span style="font-size:18px;margin-right:4px">‹</span> 返回
          </a>
          <h1 style="font-size:22px;font-weight:700;margin:0 0 4px">隐私政策</h1>
          <p style="font-size:12px;color:var(--text-secondary);margin:0">更新日期：2026年6月12日 &nbsp;|&nbsp; 生效日期：2026年6月12日</p>
        </div>

        <div class="privacy-content" style="margin-top:20px;line-height:1.8;color:var(--text-primary);font-size:14px">
          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">一、引言</h2>
          <p>卓翌定制（以下简称"我们"或"本平台"）非常重视您的隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的个人信息，以及您如何管理这些信息。</p>
          <p>请您在使用我们的服务前，仔细阅读并充分理解本隐私政策。如果您不同意本政策的任何内容，请停止使用我们的服务。</p>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">二、我们收集的信息</h2>
          <p>在您使用我们的服务时，我们可能收集以下类型的信息：</p>
          <ul style="padding-left:20px">
            <li><strong>账号信息</strong>：手机号码、昵称、头像等注册/登录信息</li>
            <li><strong>订单信息</strong>：您提交的产品定制订单、收货地址、联系方式</li>
            <li><strong>通讯信息</strong>：您与客服的聊天记录、咨询内容</li>
            <li><strong>设备信息</strong>：设备型号、操作系统、网络类型等（用于优化服务体验）</li>
            <li><strong>日志信息</strong>：访问日期和时间、浏览记录等</li>
          </ul>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">三、信息的使用</h2>
          <p>我们收集的信息将用于以下目的：</p>
          <ul style="padding-left:20px">
            <li>提供、维护和改进我们的产品和服务</li>
            <li>处理您的订单和咨询请求</li>
            <li>向您发送服务通知和订单状态更新</li>
            <li>保障账户安全，防止欺诈和滥用行为</li>
            <li>遵守法律法规的要求</li>
          </ul>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">四、信息的存储与保护</h2>
          <p>我们采取合理的技术和管理措施来保护您的个人信息安全：</p>
          <ul style="padding-left:20px">
            <li>数据传输采用加密方式</li>
            <li>服务器设有访问权限控制</li>
            <li>定期对系统进行安全审查</li>
          </ul>
          <p>您的个人信息将存储于中华人民共和国境内，存储期限为实现收集目的所必需的最短时间。超出存储期限后，我们将删除或匿名化处理您的信息。</p>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">五、信息的共享</h2>
          <p>未经您的同意，我们不会与第三方共享您的个人信息，以下情况除外：</p>
          <ul style="padding-left:20px">
            <li>经您明确授权同意</li>
            <li>为完成订单所必需（如物流配送）</li>
            <li>法律法规要求或政府主管部门依法要求</li>
            <li>为保护我们或公众的人身财产安全</li>
          </ul>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">六、您的权利</h2>
          <p>您对您的个人信息享有以下权利：</p>
          <ul style="padding-left:20px">
            <li><strong>访问权</strong>：您可以查看我们持有的您的个人信息</li>
            <li><strong>更正权</strong>：您可以要求我们更正不准确的个人信息</li>
            <li><strong>删除权</strong>：在特定情况下，您可以要求我们删除您的个人信息</li>
            <li><strong>撤回同意权</strong>：您可以随时撤回之前给予的同意</li>
          </ul>
          <p>如需行使上述权利，请通过平台内的"联系客服"功能与我们联系。</p>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">七、未成年人保护</h2>
          <p>我们非常重视对未成年人个人信息的保护。如果您是18周岁以下的未成年人，请在您的监护人的指导下使用我们的服务，并在监护人同意的前提下向我们提供您的个人信息。</p>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">八、政策更新</h2>
          <p>我们可能会适时修订本隐私政策。当政策发生重大变更时，我们将通过平台公告或推送通知等方式告知您。更新后的隐私政策自发布之日起生效。</p>

          <h2 style="font-size:16px;font-weight:600;margin:24px 0 8px;border-left:3px solid var(--primary);padding-left:10px">九、联系我们</h2>
          <p>如果您对本隐私政策有任何疑问或建议，请通过以下方式联系我们：</p>
          <ul style="padding-left:20px">
            <li>平台内"联系客服"功能</li>
            <li>网站：<a href="https://www.wgh2026.top" style="color:var(--primary)">www.wgh2026.top</a></li>
          </ul>

          <div style="text-align:center;padding:32px 0 16px;color:var(--text-secondary);font-size:12px">
            <p>卓翌定制 &copy; 2026</p>
          </div>
        </div>
      </div>
    `
  };
}

export function mountPrivacy() {
  // No interactive logic needed for this page
}
