# -*- coding: utf-8 -*-
"""为泽罗关系图添加：1)夜间黑+红电路板 2)白天白+金电路板 3)更新日志"""
import re

path = r"C:\Users\15994\WorkBuddy\Claw\zelo-relationship-graph.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1. 替换 CSS 主题块（:root + .theme-light + body::before）
# ============================================================

old_css_head = """/* ============================================================
   主题变量：夜间（默认） & 白天（金色电路板）
   ============================================================ */
:root{
  --bg:#111;
  --text:#ddd;
  --gold:#d4a843;
  --gold-dim:#8b6914;
  --gold-faint:#5a4a2a;
  --red:#c03c3c;
  --blue:#5a80b0;
  --border:rgba(139,105,20,.4);
  --panel-bg:rgba(15,12,8,.97);
  --topbar-grad:linear-gradient(90deg,#d4a843,#8b6914,#c03c3c,#8b6914,#d4a843);
}
/* 白天模式：白色 + 金色电路板纹理 */
.theme-light{
  --bg:#ffffff;
  --text:#1a1a1a;
  --gold:#c9920a;
  --gold-dim:#a07808;
  --gold-faint:#b09060;
  --red:#b02020;
  --blue:#2a5a8a;
  --border:rgba(180,140,20,.35);
  --panel-bg:rgba(248,245,238,.97);
  --topbar-grad:linear-gradient(90deg,#e0b030,#c9920a,#a01818,#c9920a,#e0b030);
}

/* 金色电路板 SVG 纹理 */
body::before{
  content:'';
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg stroke='%23c9920a' stroke-width='.7' fill='none'%3E%3Cpath d='M0 20h20M40 0v20M60 0v10M80 20H60M20 40v20M40 60v20M0 40H20M60 40H80M40 80V60M20 60H0M40 20H60M60 60h20M20 80V60'/%3E%3Cpath d='M10 10l10 10M50 10l-10 10M30 30l10 10M70 30l-10 10M10 70l10-10M50 70l-10-10M30 50l10 10M70 50l-10 10'/%3E%3C/g%3E%3Cg fill='%23c9920a'%3E%3Ccircle cx='20' cy='20' r='2.8'/%3E%3Ccircle cx='60' cy='20' r='2.8'/%3E%3Ccircle cx='20' cy='60' r='2.8'/%3E%3Ccircle cx='60' cy='60' r='2.8'/%3E%3Ccircle cx='40' cy='40' r='2.8'/%3E%3Ccircle cx='0' cy='20' r='1.8'/%3E%3Ccircle cx='80' cy='20' r='1.8'/%3E%3Ccircle cx='0' cy='60' r='1.8'/%3E%3Ccircle cx='80' cy='60' r='1.8'/%3E%3Ccircle cx='20' cy='0' r='1.8'/%3E%3Ccircle cx='60' cy='0' r='1.8'/%3E%3Ccircle cx='20' cy='80' r='1.8'/%3E%3Ccircle cx='60' cy='80' r='1.8'/%3E%3Ccircle cx='40' cy='0' r='1.8'/%3E%3Ccircle cx='40' cy='80' r='1.8'/%3E%3Ccircle cx='0' cy='40' r='1.8'/%3E%3Ccircle cx='80' cy='40' r='1.8'/%3E%3C/g%3E%3C/svg%3E");
  background-size:80px 80px;
  opacity:.18;
  transition:opacity .4s;
}
.theme-light::before{opacity:.14}
.theme-light{background:#ffffff}"""

new_css_head = """/* ============================================================
   主题变量：夜间（默认=纯黑+红电路板） & 白天（白+金电路板）
   ============================================================ */
:root{
  --bg:#000000;
  --text:#ddd;
  --gold:#c03c3c;
  --gold-dim:#8b1a1a;
  --gold-faint:#5a2020;
  --gold-faint2:#3a1515;
  --red:#e05050;
  --blue:#5a80b0;
  --border:rgba(150,30,30,.4);
  --panel-bg:rgba(8,3,3,.97);
  --topbar-grad:linear-gradient(90deg,#c03c3c,#8b1a1a,#e05050,#8b1a1a,#c03c3c);
}
/* 白天模式：白色 + 金色电路板纹理 */
.theme-light{
  --bg:#ffffff;
  --text:#1a1a1a;
  --gold:#c9920a;
  --gold-dim:#a07808;
  --gold-faint:#b09060;
  --gold-faint2:#c8b880;
  --red:#b02020;
  --blue:#2a5a8a;
  --border:rgba(180,140,20,.35);
  --panel-bg:rgba(248,245,238,.97);
  --topbar-grad:linear-gradient(90deg,#e0b030,#c9920a,#a01818,#c9920a,#e0b030);
}

/* 电路板 SVG 纹理（夜间=红，白天=金，JS 动态切换） */
body::before{
  content:'';
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:var(--circuit-svg);
  background-size:80px 80px;
  opacity:.2;
  transition:opacity .4s,background-image 0s;
}
.theme-light::before{opacity:.14}
.theme-light{background:#ffffff}"""

# URL-encode the SVG for dark mode (red) and light mode (gold)
# Red circuit SVG (dark mode default)
red_svg = """data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg stroke='%23c03c3c' stroke-width='.7' fill='none'%3E%3Cpath d='M0 20h20M40 0v20M60 0v10M80 20H60M20 40v20M40 60v20M0 40H20M60 40H80M40 80V60M20 60H0M40 20H60M60 60h20M20 80V60'/%3E%3Cpath d='M10 10l10 10M50 10l-10 10M30 30l10 10M70 30l-10 10M10 70l10-10M50 70l-10-10M30 50l10 10M70 50l-10 10'/%3E%3C/g%3E%3Cg fill='%23c03c3c'%3E%3Ccircle cx='20' cy='20' r='2.8'/%3E%3Ccircle cx='60' cy='20' r='2.8'/%3E%3Ccircle cx='20' cy='60' r='2.8'/%3E%3Ccircle cx='60' cy='60' r='2.8'/%3E%3Ccircle cx='40' cy='40' r='2.8'/%3E%3Ccircle cx='0' cy='20' r='1.8'/%3E%3Ccircle cx='80' cy='20' r='1.8'/%3E%3Ccircle cx='0' cy='60' r='1.8'/%3E%3Ccircle cx='80' cy='60' r='1.8'/%3E%3Ccircle cx='20' cy='0' r='1.8'/%3E%3Ccircle cx='60' cy='0' r='1.8'/%3E%3Ccircle cx='20' cy='80' r='1.8'/%3E%3Ccircle cx='60' cy='80' r='1.8'/%3E%3Ccircle cx='40' cy='0' r='1.8'/%3E%3Ccircle cx='40' cy='80' r='1.8'/%3E%3Ccircle cx='0' cy='40' r='1.8'/%3E%3Ccircle cx='80' cy='40' r='1.8'/%3E%3C/g%3E%3C/svg%3E"""
gold_svg = """data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg stroke='%23c9920a' stroke-width='.7' fill='none'%3E%3Cpath d='M0 20h20M40 0v20M60 0v10M80 20H60M20 40v20M40 60v20M0 40H20M60 40H80M40 80V60M20 60H0M40 20H60M60 60h20M20 80V60'/%3E%3Cpath d='M10 10l10 10M50 10l-10 10M30 30l10 10M70 30l-10 10M10 70l10-10M50 70l-10-10M30 50l10 10M70 50l-10 10'/%3E%3C/g%3E%3Cg fill='%23c9920a'%3E%3Ccircle cx='20' cy='20' r='2.8'/%3E%3Ccircle cx='60' cy='20' r='2.8'/%3E%3Ccircle cx='20' cy='60' r='2.8'/%3E%3Ccircle cx='60' cy='60' r='2.8'/%3E%3Ccircle cx='40' cy='40' r='2.8'/%3E%3Ccircle cx='0' cy='20' r='1.8'/%3E%3Ccircle cx='80' cy='20' r='1.8'/%3E%3Ccircle cx='0' cy='60' r='1.8'/%3E%3Ccircle cx='80' cy='60' r='1.8'/%3E%3Ccircle cx='20' cy='0' r='1.8'/%3E%3Ccircle cx='60' cy='0' r='1.8'/%3E%3Ccircle cx='20' cy='80' r='1.8'/%3E%3Ccircle cx='60' cy='80' r='1.8'/%3E%3Ccircle cx='40' cy='0' r='1.8'/%3E%3Ccircle cx='40' cy='80' r='1.8'/%3E%3Ccircle cx='0' cy='40' r='1.8'/%3E%3Ccircle cx='80' cy='40' r='1.8'/%3E%3C/g%3E%3C/svg%3E"""

new_css_head_filled = new_css_head.replace(
    'var(--circuit-svg)',
    f'url("{red_svg}")'
)

if old_css_head in html:
    html = html.replace(old_css_head, new_css_head_filled)
    print("✅ CSS主题块替换成功")
else:
    print("❌ 未找到原始CSS头块，尝试模糊匹配...")
    # Try to find and replace just the first block
    idx = html.find('/* ============================================================\n   主题变量')
    if idx == -1:
        idx = html.find('/* =====')
    if idx >= 0:
        print(f"  找到CSS起始于 {idx}")

# ============================================================
# 2. JS toggleTheme 增加电路板SVG切换
# ============================================================
old_toggle = """function toggleTheme(){
  var body = document.body;
  var isLight = body.classList.contains('theme-light');
  if(isLight){
    body.classList.remove('theme-light');
    try{localStorage.setItem('_zelo_theme','dark');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '☽';
  } else {
    body.classList.add('theme-light');
    try{localStorage.setItem('_zelo_theme','light');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '☀';
  }
}"""

new_toggle = """function toggleTheme(){
  var body = document.body;
  var isLight = body.classList.contains('theme-light');
  if(isLight){
    body.classList.remove('theme-light');
    try{localStorage.setItem('_zelo_theme','dark');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '\\u263E';
    // 切换到夜间：红电路板
    try{document.body.style.setProperty('--circuit-svg','url("%s")');}catch(e){}
  } else {
    body.classList.add('theme-light');
    try{localStorage.setItem('_zelo_theme','light');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '\\u2600';
    // 切换到白天：金电路板
    try{document.body.style.setProperty('--circuit-svg','url("%s")');}catch(e){}
  }
}""" % (red_svg, gold_svg)

if old_toggle in html:
    html = html.replace(old_toggle, new_toggle)
    print("✅ toggleTheme JS替换成功")
else:
    print("❌ 未找到原始toggleTheme函数")

# ============================================================
# 3. 页面加载时初始化电路板SVG
# ============================================================
old_iife_end = """  }catch(e){}
})();"""

new_iife_end = """  }catch(e){}
  // 初始化电路板SVG
  try{
    if(saved === 'light'){
      document.body.style.setProperty('--circuit-svg','url("%s")');
    } else {
      document.body.style.setProperty('--circuit-svg','url("%s")');
    }
  }catch(e){}
}})();""" % (gold_svg, red_svg)

if old_iife_end in html:
    html = html.replace(old_iife_end, new_iife_end)
    print("✅ IIFE初始化SVG成功")
else:
    print("❌ 未找到IIFE尾部")

# ============================================================
# 4. 门页背景改为纯黑（已在CSS中，但门页元素本身是#111）
# ============================================================
old_gate = '#gate{position:fixed;inset:0;background:#111;'
new_gate = '#gate{position:fixed;inset:0;background:#000;'
if old_gate in html:
    html = html.replace(old_gate, new_gate)
    print("✅ 门页背景改为纯黑")
else:
    print("⚠️ 门页背景未变化（可能已正确）")

# ============================================================
# 5. 添加更新日志CSS + HTML按钮 + 模态框
# ============================================================

# 新增CSS（插到 </style> 之前）
changelog_css = """
/* ============================================================
   更新日志（所有人可见）
   ============================================================ */
#btn-log{
  position:fixed;top:16px;right:116px;z-index:30;
  background:var(--panel-bg);border:1px solid var(--border);
  color:var(--gold);width:40px;height:40px;
  border-radius:8px;cursor:pointer;
  font-size:16px;line-height:40px;text-align:center;
  transition:all .3s;
  box-shadow:0 2px 12px rgba(0,0,0,.4);
}
#btn-log:hover{background:var(--gold-dim);color:#000;border-color:var(--gold-dim)}

#changelog-modal{
  position:fixed;inset:0;z-index:99990;
  display:none;align-items:center;justify-content:center;
  background:rgba(0,0,0,.88);
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
}
#changelog-modal.show{display:flex;animation:clFadeIn .35s ease}
@keyframes clFadeIn{from{opacity:0;transform:scale(.96)}to{opacity:1;transform:scale(1)}}
#cl-box{
  background:var(--panel-bg);border:1px solid var(--border);
  border-radius:12px;width:520px;max-width:92vw;max-height:78vh;
  display:flex;flex-direction:column;
  box-shadow:0 0 60px rgba(0,0,0,.6);
  animation:clBoxIn .4s cubic-bezier(.22,1,.36,1);
}
@keyframes clBoxIn{from{transform:translateY(16px);opacity:0}to{transform:translateY(0);opacity:1}}
#cl-head{
  padding:20px 24px 16px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:12px;flex-shrink:0;
}
#cl-head .cl-seal{
  width:32px;height:32px;border:1px solid var(--gold-dim);border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:16px;flex-shrink:0;
}
#cl-head .cl-title{font-size:15px;color:var(--gold);letter-spacing:3px}
#cl-head .cl-sub{font-size:10px;color:var(--gold-faint);letter-spacing:2px;margin-left:auto}
#cl-close{
  margin-left:12px;width:28px;height:28px;border-radius:4px;
  background:none;border:1px solid var(--border);color:var(--gold-dim);
  cursor:pointer;font-size:16px;line-height:1;transition:all .2s;
}
#cl-close:hover{background:var(--gold-dim);color:#000}
#cl-body{
  padding:16px 24px 24px;overflow-y:auto;flex:1;
}
.cl-entry{
  padding:12px 0;border-bottom:1px solid var(--border);
  animation:clEntryIn .3s ease forwards;opacity:0;
}
.cl-entry:last-child{border-bottom:none}
@keyframes clEntryIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.cl-e-head{display:flex;align-items:center;gap:8px;margin-bottom:6px}
.cl-e-ver{
  font-size:11px;color:var(--gold);letter-spacing:1px;
  background:rgba(139,105,20,.15);border:1px solid var(--border);
  padding:2px 8px;border-radius:3px;
}
.cl-e-date{font-size:10px;color:var(--gold-faint);letter-spacing:1px;margin-left:auto}
.cl-e-title{font-size:13px;color:var(--gold-dim);letter-spacing:1px;margin-bottom:6px}
.cl-e-items{margin:0;padding-left:18px}
.cl-e-items li{font-size:12px;color:var(--text);line-height:1.8;margin:2px 0}
.cl-e-items li::marker{color:var(--gold-dim)}
.cl-e-lore{
  font-size:10px;color:var(--gold-faint);font-style:italic;
  margin-top:6px;letter-spacing:1px;
}
@media(max-width:600px){
  #btn-log{top:12px;right:100px;width:36px;height:36px;line-height:36px;font-size:14px}
  #cl-box{max-height:85vh}
  #cl-head{padding:14px 16px 12px}
  #cl-body{padding:12px 16px 20px}
  .cl-e-title{font-size:12px}
  .cl-e-items li{font-size:11px}
}
"""

# 找到 </style> 并插入CSS之前
style_close = '</style>'
insert_pos = html.rfind(style_close)
if insert_pos >= 0:
    html = html[:insert_pos] + changelog_css + '\n' + style_close + html[insert_pos+len(style_close):]
    print("✅ 更新日志CSS插入成功")
else:
    print("❌ 未找到 </style>")

# ============================================================
# 6. 添加更新日志按钮 HTML（在 btn-admin 前面）
# ============================================================
old_btn_area = '<button id="btn-admin"'
new_btn_area = """<button id="btn-log" title="&#9670; 档案更新日志" onclick="showChangelog()">&#9654;</button>
<button id="btn-admin\""""
if old_btn_area in html:
    html = html.replace(old_btn_area, new_btn_area)
    print("✅ 更新日志按钮HTML插入成功")
else:
    print("❌ 未找到btn-admin按钮")

# ============================================================
# 7. 添加JS：showChangelog 函数 + changelog数据
# ============================================================

# 更新日志数据（世界观风格）
changelog_js = """
// ===== 档案更新日志（所有人可见）=====
var CHANGELOG_DATA = [
  {
    ver:"v2.3.0",
    date:"2026-05-08",
    title:"时序回路校准完毕",
    lore:"本记录已同步至主时间线档案库，编号 TMB-ZELO-20260508。",
    items:[
      "新增「档案更新日志」入口，所有访客均可查阅关系图历次更新",
      "夜间模式重构：纯黑背景 + 红色电路板纹理，符合时序回路的底层逻辑",
      "白天模式保留：白色背景 + 金色电路板纹理，适配高光环境",
      "主题偏好自动保存至本地存储"
    ]
  },
  {
    ver:"v2.2.0",
    date:"2026-04-22",
    title:"角色节点扩充",
    lore:"新增实验体与历史角色档案，记忆碎片密度提升 37%。",
    items:[
      "新增角色：李斯、老莫、花生（实验体系列）",
      "新增角色：双子、针线（历史遗留节点）",
      "角色关系连线扩充至 35 条",
      "故事关联锚点精确到章节级别"
    ]
  },
  {
    ver:"v2.1.0",
    date:"2026-04-15",
    title:"故事档案库开放",
    lore:"故事集已由「零号计划」档案室移交至主索引，可按角色筛选阅读。",
    items:[
      "开放 15 篇故事阅读（需角色解锁权限）",
      "故事按时间线排列，含章节锚点跳转",
      "新增「全部故事」视图",
      "角色面板显示关联故事列表"
    ]
  },
  {
    ver:"v2.0.0",
    date:"2026-04-10",
    title:"关系网络重构上线",
    lore:"网络拓扑由单层结构升级为双圈 Hub-Spoke 布局，节点信息密度提升。",
    items:[
      "核心角色（内圈）自动显示关联节点",
      "Canvas 拖拽交互优化",
      "搜索支持角色和故事双维度",
      "移动端适配重构"
    ]
  },
  {
    ver:"v1.0.0",
    date:"2026-04-01",
    title:"系统初始化",
    lore:"关系图谱由时序管理局档案系统自动生成，初次校准完成。",
    items:[
      "角色节点：22 个",
      "关系连线：18 条",
      "密码保护：zero2026（访客） / zero000（专属权限）"
    ]
  }
];

function showChangelog(){
  var modal = document.getElementById('changelog-modal');
  if(!modal) return;
  var body = document.getElementById('cl-body');
  if(!body) return;

  var html = '';
  CHANGELOG_DATA.forEach(function(entry, i){
    var items = entry.items.map(function(item){ return '<li>'+item+'</li>'; }).join('');
    html += '<div class="cl-entry" style="animation-delay:'+(i*60)+'ms">'+
      '<div class="cl-e-head">'+
        '<span class="cl-e-ver">'+entry.ver+'</span>'+
        '<span class="cl-e-date">'+entry.date+'</span>'+
      '</div>'+
      '<div class="cl-e-title">'+entry.title+'</div>'+
      '<ul class="cl-e-items">'+items+'</ul>'+
      '<div class="cl-e-lore">'+entry.lore+'</div>'+
    '</div>';
  });
  body.innerHTML = html;
  modal.classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeChangelog(){
  var modal = document.getElementById('changelog-modal');
  if(modal) modal.classList.remove('show');
  document.body.style.overflow = '';
}

function initChangelogModal(){
  // 点击遮罩关闭
  var modal = document.getElementById('changelog-modal');
  if(modal){
    modal.addEventListener('click', function(e){
      if(e.target === modal) closeChangelog();
    });
  }
  // ESC关闭
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape') closeChangelog();
  });
}
"""

# 在 // ===== DATA ===== 之前插入
data_marker = '\n// ===== DATA =====\n'
if data_marker in html:
    html = html.replace(data_marker, changelog_js + '\n' + data_marker)
    print("✅ 更新日志JS数据插入成功")
else:
    print("❌ 未找到DATA标记")

# ============================================================
# 8. 添加模态框 HTML（在 </body> 之前）
# ============================================================
changelog_modal_html = """
<div id="changelog-modal" onclick="if(event.target===this)closeChangelog()">
  <div id="cl-box">
    <div id="cl-head">
      <div class="cl-seal">&#9670;</div>
      <div class="cl-title">档案更新日志</div>
      <div class="cl-sub">TEMPORAL ARCHIVE LOG · ALL VISITORS</div>
      <button id="cl-close" onclick="closeChangelog()">&#10005;</button>
    </div>
    <div id="cl-body"><!-- JS填充 --></div>
  </div>
</div>
"""

if '</body>' in html:
    html = html.replace('</body>', changelog_modal_html + '\n</body>')
    print("✅ 更新日志模态框HTML插入成功")
else:
    print("❌ 未找到</body>")

# ============================================================
# 9. 页面加载时调用 initChangelogModal
# ============================================================
old_docready = """// ===== DATA ====="""
new_docready = """// ===== 初始化 =====\ninitChangelogModal();\n\n// ===== DATA ====="""
if old_docready in html:
    html = html.replace(old_docready, new_docready)
    print("✅ initChangelogModal调用插入成功")
else:
    print("❌ 未找到DATA标记（第二次）")

# ============================================================
# 10. 移动端 #btn-log 定位
# ============================================================
old_mob = "  #btn-theme{top:12px;right:58px;width:36px;height:36px;line-height:36px;font-size:16px}"
new_mob = "  #btn-log{top:12px;right:100px;width:36px;height:36px;line-height:36px;font-size:14px}\n  #btn-theme{top:12px;right:58px;width:36px;height:36px;line-height:36px;font-size:16px}"
if old_mob in html:
    html = html.replace(old_mob, new_mob)
    print("✅ 移动端 btn-log 定位插入")
else:
    print("⚠️ 移动端btn-theme未精确匹配，尝试搜索...")
    idx = html.find('#btn-theme{top:12px;right:58px')
    if idx >= 0:
        print(f"  找到于 {idx}")

# ============================================================
# 写入
# ============================================================
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("\n写入完成！")
