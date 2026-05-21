/**
 * auth-server.js — 泽罗角色关系图 · 双权限认证服务器
 *
 * 用法: node auth-server.js [端口]
 * 默认端口: 8888
 *
 * 依赖: Node.js 内置模块 (http, fs, path, url, crypto, querystring)
 * 无需 npm install
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const crypto = require('crypto');

// ===================== 配置 =====================
const PORT = process.argv[2] ? parseInt(process.argv[2]) : 8888;
const HOST = '0.0.0.0';

// 密码（生产环境建议改为复杂密码，或通过环境变量传入）
const PASSWORDS = {
  guest: 'zero2026',
  admin: 'zero000',
  egg: 'zerotime'
};

// Cookie 签名密钥（生产环境务必通过环境变量设置）
const COOKIE_SECRET = process.env.ZELO_COOKIE_SECRET || 'Z3r0_Sh1ro_SecretKey_2026';

// Cookie 设置
const COOKIE_NAME = 'zelo_auth';
const COOKIE_MAX_AGE = 7 * 24 * 60 * 60; // 7 天（秒）

// HTML 文件路径
const HTML_GUEST = path.join(__dirname, 'zelo-guest.html');
const HTML_ADMIN = path.join(__dirname, 'zelo-relationship-graph.html');

// ===================== HMAC Cookie 签名 =====================
/**
 * 创建签名 cookie: level:expiry:HMAC
 */
function makeCookie(level) {
  const expiry = Date.now() + COOKIE_MAX_AGE * 1000;
  const raw = level + ':' + expiry;
  const sig = crypto.createHmac('sha256', COOKIE_SECRET).update(raw).digest('hex');
  return COOKIE_NAME + '=' + [level, expiry, sig].join(':') +
    '; Max-Age=' + COOKIE_MAX_AGE +
    '; Path=/' +
    '; HttpOnly' +
    '; SameSite=Strict';
}

/**
 * 验证 cookie，返回 level 或 null
 */
function verifyCookie(cookieHeader) {
  if (!cookieHeader) return null;
  const match = cookieHeader.match(new RegExp(COOKIE_NAME + '=([^;]+)'));
  if (!match) return null;
  const parts = match[1].split(':');
  if (parts.length !== 3) return null;
  const [level, expiryStr, sig] = parts;
  const expiry = parseInt(expiryStr);
  if (isNaN(expiry) || expiry < Date.now()) return null; // 已过期
  const raw = level + ':' + expiryStr;
  const expectedSig = crypto.createHmac('sha256', COOKIE_SECRET).update(raw).digest('hex');
  if (sig !== expectedSig) return null; // 被篡改
  if (level !== 'guest' && level !== 'admin' && level !== 'egg') return null;
  return level;
}

// ===================== 登录页面 HTML =====================
function loginPageHTML(msg) {
  const errMsg = msg ? '<div class="err">' + msg + '</div>' : '';
  return `<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泽罗 · 角色关系图</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:"Microsoft YaHei","PingFang SC",sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;color:#ddd}
.box{background:#0a0808;border:1px solid #3a1515;border-radius:12px;padding:48px 56px;text-align:center;max-width:380px;width:90%}
h1{color:#d4a843;font-size:22px;letter-spacing:4px;margin-bottom:8px}
p{color:#8b7355;font-size:13px;margin-bottom:28px}
input{display:block;width:100%;padding:12px 16px;background:#1a0f0f;border:1px solid #3a1515;border-radius:6px;color:#d4a843;font-size:16px;text-align:center;outline:none;margin-bottom:16px;font-family:inherit}
input:focus{border-color:#8b6914}
input::placeholder{color:#5a3020}
button{width:100%;padding:12px;background:rgba(139,105,20,.3);border:1px solid #8b6914;color:#d4a843;border-radius:6px;font-size:15px;cursor:pointer;letter-spacing:2px;transition:all .2s;font-family:inherit}
button:hover{background:#8b6914;color:#fff}
button:active{transform:scale(.97)}
.err{color:#e06060;font-size:13px;margin-bottom:12px;min-height:20px}
.note{color:#5a3020;font-size:11px;margin-top:20px}
</style>
</head>
<body>
<div class="box">
  <h1>泽罗 · 角色关系图</h1>
  <p>Temporal Administration Bureau</p>
  ${errMsg}
  <form method="POST" action="/login">
    <input type="password" name="pw" placeholder="输入访问密码" autofocus />
    <button type="submit">确认</button>
  </form>
  <div class="note">仅限受邀访客</div>
</div>
</body>
</html>`;
}

// ===================== 主服务器 =====================
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // ---- 静态资源（/public/ 目录）----
  if (pathname.startsWith('/public/')) {
    const filePath = path.join(__dirname, pathname);
    serveFile(res, filePath, req.headers['accept-encoding']);
    return;
  }

  // ---- 静态资源（根目录下的 JS/JSON/WAV 等）----
  const ALLOWED_EXTS = ['.js', '.json', '.wav', '.mp3', '.png', '.jpg', '.gif', '.svg', '.css', '.ico'];
  const ext = path.extname(pathname).toLowerCase();
  if (method === 'GET' && ALLOWED_EXTS.indexOf(ext) >= 0 && !pathname.includes('..')) {
    const filePath = path.join(__dirname, pathname);
    serveFile(res, filePath, req.headers['accept-encoding']);
    return;
  }

  // ---- 登录页 GET / ----
  if (method === 'GET' && (pathname === '/' || pathname === '/login')) {
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
    res.end(loginPageHTML());
    return;
  }

  // ---- 处理登录 POST /login ----
  if (method === 'POST' && pathname === '/login') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const pw = (params.get('pw') || '').trim();

      if (pw === PASSWORDS.admin) {
        res.writeHead(302, {
          'Location': '/index.html',
          'Set-Cookie': makeCookie('admin'),
          'Content-Type': 'text/plain'
        });
        res.end('Redirecting...');
      } else if (pw === PASSWORDS.guest) {
        res.writeHead(302, {
          'Location': '/index.html',
          'Set-Cookie': makeCookie('guest'),
          'Content-Type': 'text/plain'
        });
        res.end('Redirecting...');
      } else if (pw === PASSWORDS.egg) {
        res.writeHead(302, {
          'Location': '/index.html',
          'Set-Cookie': makeCookie('egg'),
          'Content-Type': 'text/plain'
        });
        res.end('Redirecting...');
      } else {
        res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
        res.end(loginPageHTML('密码错误，请重试'));
      }
    });
    return;
  }

  // ---- 登出 GET /logout ----
  if (method === 'GET' && pathname === '/logout') {
    res.writeHead(302, {
      'Location': '/',
      'Set-Cookie': COOKIE_NAME + '=; Max-Age=0; Path=/',
      'Content-Type': 'text/plain'
    });
    res.end('Logging out...');
    return;
  }

  // ---- 主页面 /index.html ----
  if (method === 'GET' && (pathname === '/index.html' || pathname === '/zelo')) {
    const level = verifyCookie(req.headers.cookie);
    if (!level) {
      // 未登录，重定向到登录页
      res.writeHead(302, {'Location': '/'});
      res.end();
      return;
    }
    // 统一返回完整版，三个密码的逻辑都在里面
    res.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'X-Auth-Level': level
    });
    try {
      let html = fs.readFileSync(HTML_ADMIN, 'utf-8');
      // 注入认证级别，gate 门页自动跳过
      const inject = '<script>window.__AUTH_LEVEL__="' + level + '";</script>';
      html = html.replace('</head>', inject + '</head>');
      res.end(html);
    } catch (e) {
      res.writeHead(500);
      res.end('文件读取错误: ' + e.message);
    }
    return;
  }

  // ---- 404 ----
  res.writeHead(404, {'Content-Type': 'text/plain'});
  res.end('404 Not Found');
});

// ===================== 文件服务（带缓存头）====================
function serveFile(res, filePath, acceptEncoding) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not Found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
      '.html': 'text/html; charset=utf-8',
      '.js': 'application/javascript',
      '.css': 'text/css',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.ico': 'image/x-icon',
      '.json': 'application/json',
      '.txt': 'text/plain'
    };
    const contentType = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'public, max-age=3600'
    });
    res.end(data);
  });
}

// ===================== 启动 =====================
server.listen(PORT, HOST, () => {
  console.log('泽罗认证服务器已启动');
  console.log('访问地址: http://localhost:' + PORT);
  console.log('访客密码: ' + PASSWORDS.guest);
  console.log('管理员密码: ' + PASSWORDS.admin);
  console.log('');
  console.log('配合 Cloudflare Tunnel 使用时:');
  console.log('  cloudflared.exe tunnel --url http://localhost:' + PORT);
  console.log('');
  console.log('停止服务器: Ctrl+C');
  console.log('');
  console.log('【安全提醒】生产环境请设置环境变量:');
  console.log('  set ZELO_COOKIE_SECRET=你的随机长字符串');
  console.log('  set ZELO_ADMIN_PASS=你的管理员密码');
  console.log('  set ZELO_GUEST_PASS=你的访客密码');
});
