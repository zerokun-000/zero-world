/* zelo-admin.js — 覆盖/补充 admin 相关函数
   所有中文字符用 \u 转义，彻底避免编码问题
*/

// ===== 获取公网 IP + 地理位置（JSONP，file:// 下可用）=====
function getIPAndGeo(){
  // whois.pconline.com.cn 固定用 window.IPCallBack 回调
  // 返回：IPCallBack({"ip":"...","pro":"省份","city":"城市",...})
  return new Promise(function(resolve){
    // 先定义回调，再加载 script
    window.IPCallBack = function(data){
      var ip = data.ip || "";
      var loc = (data.pro || "") + " " + (data.city || "");
      cleanup();
      resolve({ip: ip, loc: loc.replace(/市$/, "").trim()});
    };
    var s = document.createElement("script");
    s.src = "https://whois.pconline.com.cn/ipJson.jsp?t=" + Date.now();
    s.onerror = function(){
      cleanup();
      // 备用：myip.ipip.net（需要 CORS，http:// 下可用）
      fetch("https://myip.ipip.net/json")
        .then(function(r){ return r.json(); })
        .then(function(d){
          var ip = (d.data && d.data.ip) ? d.data.ip : "";
          var loc = "";
          if(d.data && Array.isArray(d.data.location)){
            var p = d.data.location.filter(function(s){ return s && s.trim(); });
            if(p.length >= 3) loc = p[1] + " " + p[2];
            else if(p.length >= 2) loc = p[1];
          }
          resolve({ip: ip, loc: loc});
        })
        .catch(function(){ resolve({ip:"", loc:""}); });
    };
    function cleanup(){
      try{ delete window.IPCallBack; document.head.removeChild(s); }catch(e){}
    }
    document.head.appendChild(s);
    // 6 秒超时
    setTimeout(function(){
      if(window.IPCallBack){ cleanup(); resolve({ip:"", loc:""}); }
    }, 6000);
  });
}

// ===== 设备指纹识别 =====
// 返回 {os, browser, device, icon}，icon 是 emoji
function getDeviceInfo(){
  var ua = navigator.userAgent || "";
  var os = "\u672A\u77E5", browser = "\u672A\u77E5", device = "\u2014", icon = "\uD83D\uDCBB";
  // OS
  if(/Windows NT 10/.test(ua)) os = "Windows 10/11";
  else if(/Windows NT 6\.3/.test(ua)) os = "Windows 8.1";
  else if(/Mac OS X/.test(ua)) os = "macOS";
  else if(/Linux/.test(ua)) os = "Linux";
  else if(/Android/.test(ua)) os = "Android";
  else if(/\biPhone|iPad|iPod/.test(ua)) os = "iOS";
  // Browser
  if(/Edg\//.test(ua)) browser = "Edge";
  else if(/OPR\//.test(ua) || /Opera/.test(ua)) browser = "Opera";
  else if(/Chrome\//.test(ua) && !/Chromium/.test(ua)) browser = "Chrome";
  else if(/Firefox\//.test(ua)) browser = "Firefox";
  else if(/Safari\//.test(ua) && !/Chrome/.test(ua)) browser = "Safari";
  else if(/QQBrowser\//.test(ua)) browser = "QQ\u6D4F\u89C8\u5668";
  else if(/MicroMessenger\//.test(ua)) browser = "\u5FAE\u4FE1";
  // Device type
  if(/Mobile|Android|iPhone|iPad|iPod/.test(ua)){
    if(/iPad|Tablet/i.test(ua)){ device = "\u5E73\u677F"; icon = "\uD83D\uDCF1"; }
    else{ device = "\u624B\u673A"; icon = "\uD83D\uDCF1"; }
  } else { device = "\u684C\u9762"; icon = "\uD83D\uDDA5\uFE0F"; }
  return {os:os, browser:browser, device:device, icon:icon};
}

// ===== 记录一次访问 =====
function recordSession(type){
  var records = [];
  try{ records = JSON.parse(localStorage.getItem("_zelo_records")||"[]"); }catch(e){records=[];}
  var now = new Date();
  var ts = now.getFullYear()+"-"
           +String(now.getMonth()+1).padStart(2,"0")+"-"
           +String(now.getDate()).padStart(2,"0")+" "
           +String(now.getHours()).padStart(2,"0")+":"
           +String(now.getMinutes()).padStart(2,"0")+":"
           +String(now.getSeconds()).padStart(2,"0");
  var eggName = "";
  try{ eggName = localStorage.getItem("_zelo_egg_name")||""; }catch(e){}
  var identity = eggName ? eggName : "\u8BBF\u5BA2-" + String(records.length+1).padStart(3,"0");
  var dev = getDeviceInfo();
  var deviceStr = dev.icon + " " + dev.device + " / " + dev.os + " / " + dev.browser;

  // 获取 IP + 地理位置（国内 API）
  getIPAndGeo().then(function(result){
    var displayIP = result.ip || "\u672A\u77E5";
    var displayLoc = result.loc || "\u672A\u77E5";
    records.unshift({seq:records.length+1, time:ts, identity:identity, type:type, ip:displayIP, loc:displayLoc, device:deviceStr});
    if(records.length>50) records = records.slice(0,50);
    try{ localStorage.setItem("_zelo_records", JSON.stringify(records)); }catch(e){}
    var panel = document.getElementById("admin-panel");
    if(panel && panel.classList.contains("show")) refreshAdminRecords();
  }).catch(function(){
    records.unshift({seq:records.length+1, time:ts, identity:identity, type:type, ip:"\u672A\u77E5", loc:"\u672A\u77E5", device:deviceStr});
    if(records.length>50) records = records.slice(0,50);
    try{ localStorage.setItem("_zelo_records", JSON.stringify(records)); }catch(e){}
  });
}

// ===== 刷新后台记录表 =====
function refreshAdminRecords(){
  var body = document.getElementById("ap-records");
  if(!body) return;
  var records = [];
  try{ records = JSON.parse(localStorage.getItem("_zelo_records")||"[]"); }catch(e){records=[];}
  var html = '<table class="ap-table"><thead><tr>'
    +'<th>#</th><th>\u767B\u5F55\u65F6\u95F4</th><th>\u8BBF\u95EE\u8005</th>'
    +'<th>\u64CD\u4F5C\u7C7B\u578B</th><th>IP</th><th>\u5730\u70B9</th><th>\u8BBE\u5907</th></tr></thead><tbody>';
  records.forEach(function(r){
    var tc = r.type==="\u7BA1\u7406\u5C40\u8BBF\u95EE"?"#e06060"
              :r.type==="\u4E13\u5C5E\u8BBF\u95EE"?"#d4a843"
              :r.type==="\u5916\u89C2\u89E3\u9501"?"#5a80b0"
              :"#7ab08a";
    var devCol = r.device || "\u2014";
    html += '<tr><td>'+r.seq+'</td><td>'+r.time+'</td>'
           +'<td style="color:#d4a843">'+r.identity+'</td>'
           +'<td><span style="color:'+tc+'">'+r.type+'</span></td>'
           +'<td>'+r.ip+'</td><td style="color:#888">'+r.loc+'</td><td style="color:#aaa;font-size:12px">'+devCol+'</td></tr>';
  });
  html += '</tbody></table>';
  body.innerHTML = html;
  // 更新顶部统计
  var total = records.length;
  var n1=0,n2=0,n3=0,n4=0;
  records.forEach(function(r){
    if(r.type==="\u4E13\u5C5E\u8BBF\u95EE") n1++;
    else if(r.type==="\u7BA1\u7406\u5C40\u8BBF\u95EE") n2++;
    else if(r.type==="\u5916\u89C2\u89E3\u9501") n3++;
    else n4++;
  });
  var mk = document.querySelectorAll(".as-val");
  if(mk&&mk[0]) mk[0].textContent=total;
  if(mk&&mk[1]) mk[1].textContent=n1;
  if(mk&&mk[2]) mk[2].textContent=n2;
  if(mk&&mk[3]) mk[3].textContent=n3;
  if(mk&&mk[4]) mk[4].textContent=n4;
}

// ===== 覆盖 enterMember（加按钮显示+记录）=====
function enterMember(){
  var el = document.getElementById("admin-entry");
  if(el) el.classList.remove("show");
  window._zeroAppUnlocked = true;
  loadStories();
  var btn = document.getElementById("btn-admin");
  if(btn) btn.style.display = "";
  recordSession("\u4E13\u5C5E\u8BBF\u95EE");
}

// ===== 覆盖 enterAdminBackend（加记录）=====
(function(){
  var _orig = window.enterAdminBackend;
  window.enterAdminBackend = function(){
    var el = document.getElementById("admin-entry");
    if(el) el.classList.remove("show");
    var panel = document.getElementById("admin-panel");
    if(panel) panel.classList.add("show");
    refreshAdminRecords();
    recordSession("\u7BA1\u7406\u5C40\u8BBF\u95EE");
  };
})();

// ===== 覆盖 enterEggSession（保存名字+记录）=====
(function(){
  var _orig = window.enterEggSession;
  if(typeof _orig === "function"){
    window.enterEggSession = function(name){
      window.isOwner = false;
      window._eggName = name;
      if(name) try{ localStorage.setItem("_zelo_egg_name", name); }catch(e){}
      applyGuestLock();
      loadStories();
      recordSession("\u8BBF\u5BA2\u8BBF\u95EE");
      setTimeout(function(){
        var el = document.getElementById("egg-welcome");
        var nm = document.getElementById("wel-name");
        if(nm) nm.textContent = name || "\u8BBF\u5BA2";
        if(el) el.classList.add("show");
        var cw = function(){ el.classList.remove("show"); document.removeEventListener("click",cw); };
        setTimeout(function(){ document.addEventListener("click",cw); },500);
      },200);
      // 显示时空模拟按钮
      setTimeout(function(){
        var btn = document.getElementById("btn-adventure");
        if(btn){ btn.style.display = "block"; window._zerotimeMode = true; }
      }, 500);
    };
  }
})();

// ===== 初始化：绑定管理员按钮事件 =====
window._zeloAdminInited = false;
function _initAdminButton(){
  if(window._zeloAdminInited) return;
  window._zeloAdminInited = true;

  // 右上角悬浮按钮
  var btn = document.getElementById("btn-admin");
  if(btn){
    btn.onclick = function(){
      var p = document.getElementById("admin-panel");
      if(!window.isOwner) return;
      if(p && p.classList.contains("show")){
        closeAdminPanel();
      } else {
        enterAdminBackend();
      }
    };
  }

  // 管理入口模态框按钮（防止 HTML onclick 绑定时机问题）
  var aeBox = document.getElementById("ae-box");
  if(aeBox){
    aeBox.onclick = function(e){
      var t = e.target;
      if(t && t.classList.contains("ae-btn-gold")){
        // 专属模式 → 隐藏模态框 + 显示按钮 + 进入专属模式
        var el = document.getElementById("admin-entry");
        if(el) el.classList.remove("show");
        window._zeroAppUnlocked = true;
        loadStories();
        var ab = document.getElementById("btn-admin");
        if(ab) ab.style.display = "";
        recordSession("\u4E13\u5C5E\u8BBF\u95EE");
      } else if(t && t.classList.contains("ae-btn-blue")){
        // 管理局后台 → 直接打开后台面板
        var el = document.getElementById("admin-entry");
        if(el) el.classList.remove("show");
        var panel = document.getElementById("admin-panel");
        if(panel) panel.classList.add("show");
        refreshAdminRecords();
        recordSession("\u7BA1\u7406\u5C40\u8BBF\u95EE");
      }
    };
  }
}
if(document.readyState === "loading"){
  document.addEventListener("DOMContentLoaded", _initAdminButton);
} else {
  _initAdminButton();
}

console.log("[zelo-admin.js] loaded");
