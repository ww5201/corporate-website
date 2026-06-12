const crypto = require("crypto");
const https = require("https");

// 阿里云短信配置
const SMS_CONFIG = {
  accessKeyId: process.env.ALIYUN_ACCESS_KEY_ID || "",
  accessKeySecret: process.env.ALIYUN_ACCESS_KEY_SECRET || "",
  signName: process.env.SMS_SIGN_NAME || "卓翌定制",
  templateCode: process.env.SMS_TEMPLATE_CODE || "",
  region: "dysmsapi.aliyuncs.com"
};

// 设置配置
function setConfig(config) {
  Object.assign(SMS_CONFIG, config);
}

// 生成随机验证码
function generateCode(length = 6) {
  return String(Math.floor(Math.pow(10, length - 1) + Math.random() * (Math.pow(10, length) - Math.pow(10, length - 1))));
}

// 阿里云短信签名 (v1 签名算法)
function sign(params, secret) {
  const sortedKeys = Object.keys(params).sort();
  const canonicalized = sortedKeys
    .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
    .join("&");
  const stringToSign = `GET&${encodeURIComponent("/")}&${encodeURIComponent(canonicalized)}`;
  const hmac = crypto.createHmac("sha1", secret + "&");
  hmac.update(stringToSign);
  return hmac.digest("base64");
}

// 发送短信验证码
async function sendSmsCode(phone, code) {
  if (!SMS_CONFIG.accessKeyId || !SMS_CONFIG.accessKeySecret || !SMS_CONFIG.templateCode) {
    console.log(`[SMS-DEV] 手机号 ${phone} 验证码: ${code}`);
    return { success: true, debug: true, code };
  }

  const params = {
    Action: "SendSms",
    PhoneNumbers: phone,
    SignName: SMS_CONFIG.signName,
    TemplateCode: SMS_CONFIG.templateCode,
    TemplateParam: JSON.stringify({ code }),
    Format: "JSON",
    Version: "2017-05-25",
    AccessKeyId: SMS_CONFIG.accessKeyId,
    SignatureMethod: "HMAC-SHA1",
    Timestamp: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    SignatureVersion: "1.0",
    SignatureNonce: Math.random().toString(36).substr(2)
  };

  params.Signature = sign(params, SMS_CONFIG.accessKeySecret);

  const queryString = Object.keys(params)
    .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
    .join("&");

  const url = `https://${SMS_CONFIG.region}/?${queryString}`;

  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        try {
          const result = JSON.parse(data);
          if (result.Code === "OK") {
            resolve({ success: true, requestId: result.RequestId });
          } else {
            console.error("[SMS] 发送失败:", result);
            resolve({ success: false, error: result.Message || "发送失败", code: result.Code });
          }
        } catch (e) {
          console.error("[SMS] 响应解析失败:", data);
          resolve({ success: false, error: "服务响应异常" });
        }
      });
    }).on("error", (e) => {
      console.error("[SMS] 网络错误:", e.message);
      resolve({ success: false, error: e.message });
    });
  });
}

module.exports = { sendSmsCode, generateCode, setConfig, SMS_CONFIG };
