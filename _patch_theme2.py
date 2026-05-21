fp = r"C:\Users\15994\WorkBuddy\Claw\zelo-relationship-graph.html"
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 更新 locked-box 等样式，用 CSS 变量
replacements = [
    # locked-box 系列
    (".locked-box{position:relative;border:1px solid rgba(139,105,20,.3);border-radius:6px;overflow:hidden;margin-top:4px}",
     ".locked-box{position:relative;border:1px solid var(--border);border-radius:6px;overflow:hidden;margin-top:4px;transition:border-color .4s}"),
    (".locked-overlay{padding:20px;text-align:center;background:rgba(15,12,8,.95);cursor:pointer;transition:background .2s}",
     ".locked-overlay{padding:20px;text-align:center;background:var(--panel-bg);cursor:pointer;transition:background .2s}"),
    (".locked-overlay:hover{background:rgba(139,105,20,.08)}",
     ".locked-overlay:hover{background:rgba(139,105,20,.1)}"),
    (".locked-overlay .lock-icon{font-size:22px;color:#8b6914;margin-bottom:6px}",
     ".locked-overlay .lock-icon{font-size:22px;color:var(--gold-dim);margin-bottom:6px}"),
    (".locked-pw-row{display:flex;gap:8px;padding:10px 14px;background:rgba(15,12,8,.95);align-items:center}",
     ".locked-pw-row{display:flex;gap:8px;padding:10px 14px;background:var(--panel-bg);align-items:center;transition:background .4s}"),
    (".locked-pw-btn:hover{background:#8b6914;color:#000}",
     ".locked-pw-btn:hover{background:var(--gold-dim);color:#000}"),
    (".locked-pw-err{color:#e06060;font-size:11px;padding:0 14px 8px;background:rgba(15,12,8,.95)}",
     ".locked-pw-err{color:#e06060;font-size:11px;padding:0 14px 8px;background:var(--panel-bg);transition:background .4s}"),
    (".admin-back-btn{",
     ".admin-back-btn{transition:all .2s}"),

    # mobile btn-theme
    ("  /* 管理后台悬浮按钮 */\n  #btn-admin{top:12px;right:12px;width:36px;height:36px;line-height:36px;font-size:14px}",
     "  /* 管理后台悬浮按钮 */\n  #btn-admin{top:12px;right:12px;width:36px;height:36px;line-height:36px;font-size:14px}\n  #btn-theme{top:12px;right:58px;width:36px;height:36px;line-height:36px;font-size:16px}"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: replaced {old[:60]!r}")
    else:
        print(f"NOT FOUND: {old[:60]!r}")

# 额外：locked 系列样式精确替换
extra = [
    (".locked-box{position:relative;border:1px solid rgba(139,105,20,.3);border-radius:6px;overflow:hidden;margin-top:4px}",
     ".locked-box{position:relative;border:1px solid var(--border);border-radius:6px;overflow:hidden;margin-top:4px;transition:border-color .4s}"),
    (".locked-overlay{padding:20px;text-align:center;background:rgba(15,12,8,.95);cursor:pointer;transition:background .2s}",
     ".locked-overlay{padding:20px;text-align:center;background:var(--panel-bg);cursor:pointer;transition:background .2s}"),
    (".locked-overlay .lock-icon{font-size:22px;color:#8b6914;margin-bottom:6px}",
     ".locked-overlay .lock-icon{font-size:22px;color:var(--gold-dim);margin-bottom:6px}"),
    (".locked-pw-row{display:flex;gap:8px;padding:10px 14px;background:rgba(15,12,8,.95);align-items:center}",
     ".locked-pw-row{display:flex;gap:8px;padding:10px 14px;background:var(--panel-bg);align-items:center;transition:background .4s}"),
    (".locked-pw-input{flex:1;background:rgba(20,16,10,.9);border:1px solid #555;border-radius:4px;color:#d4a843;padding:6px 10px;font-size:13px;outline:none;font-family:inherit}",
     ".locked-pw-input{flex:1;background:rgba(20,16,10,.9);border:1px solid var(--border);border-radius:4px;color:var(--gold);padding:6px 10px;font-size:13px;outline:none;font-family:inherit;transition:border-color .4s,color .4s}"),
    (".locked-pw-input:focus{border-color:#d4a843}",
     ".locked-pw-input:focus{border-color:var(--gold)}"),
    (".locked-pw-btn{background:rgba(139,105,20,.3);border:1px solid #8b6914;color:#d4a843;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px;font-family:inherit;transition:all .2s}",
     ".locked-pw-btn{background:rgba(139,105,20,.3);border:1px solid var(--gold-dim);color:var(--gold);padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px;font-family:inherit;transition:all .2s}"),
    (".locked-pw-btn:hover{background:#8b6914;color:#000}",
     ".locked-pw-btn:hover{background:var(--gold-dim);color:#000}"),
    (".locked-pw-err{color:#e06060;font-size:11px;padding:0 14px 8px;background:rgba(15,12,8,.95)}",
     ".locked-pw-err{color:#e06060;font-size:11px;padding:0 14px 8px;background:var(--panel-bg);transition:background .4s}"),
    (".admin-back-btn{\n  display:inline-block;margin-top:10px;\n  background:rgba(90,128,176,.15);border:1px solid rgba(90,128,176,.5);\n  color:#5a80b0;padding:8px 18px;border-radius:6px;\n  cursor:pointer;font-size:13px;font-family:inherit;letter-spacing:1px;\n  transition:all .2s;\n}",
     ".admin-back-btn{\n  display:inline-block;margin-top:10px;\n  background:rgba(90,128,176,.15);border:1px solid rgba(90,128,176,.5);\n  color:#5a80b0;padding:8px 18px;border-radius:6px;\n  cursor:pointer;font-size:13px;font-family:inherit;letter-spacing:1px;\n  transition:all .2s;\n  color:var(--blue);\n}"),
    ("  /* 管理后台悬浮按钮 */\n  #btn-admin{top:12px;right:12px;width:36px;height:36px;line-height:36px;font-size:14px}",
     "  /* 管理后台悬浮按钮 */\n  #btn-admin{top:12px;right:12px;width:36px;height:36px;line-height:36px;font-size:14px}\n  #btn-theme{top:12px;right:58px;width:36px;height:36px;line-height:36px;font-size:16px}"),
]

for old, new in extra:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK extra: {old[:50]!r}")
    else:
        print(f"NOT FOUND extra: {old[:50]!r}")

# 2. 添加主题切换按钮 HTML
btn_admin_line = '<button id="btn-admin" title="&#128737; 管理局后台">&#128202;</button>'
btn_theme_html = '<button id="btn-theme" title="切换主题" onclick="toggleTheme()">☽</button>'
if btn_admin_line in content:
    content = content.replace(btn_admin_line, btn_admin_line + "\n" + btn_theme_html, 1)
    print("OK: added btn-theme HTML")
else:
    print("NOT FOUND: btn-admin button HTML")

# 3. 添加 JS 逻辑 - 在 script 开头或合适位置插入 toggleTheme 函数
# 找到 script 标签
script_tag = '<script>'
if script_tag in content:
    toggle_js = """
// ===== 主题切换 =====
function toggleTheme(){
  var body = document.body;
  var isLight = body.classList.contains('theme-light');
  if(isLight){
    body.classList.remove('theme-light');
    try{localStorage.setItem('_zelo_theme','dark');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '\u263D';
  } else {
    body.classList.add('theme-light');
    try{localStorage.setItem('_zelo_theme','light');}catch(e){}
    var btn = document.getElementById('btn-theme');
    if(btn) btn.innerHTML = '\u2600';
  }
}
// 页面加载时恢复主题
(function(){
  try{
    var saved = localStorage.getItem('_zelo_theme');
    if(saved === 'light'){
      document.body.classList.add('theme-light');
      var btn = document.getElementById('btn-theme');
      if(btn) btn.innerHTML = '\u2600';
    } else {
      var btn = document.getElementById('btn-theme');
      if(btn) btn.innerHTML = '\u263D';
    }
  }catch(e){}
})();

"""
    content = content.replace(script_tag, script_tag + toggle_js, 1)
    print("OK: added toggleTheme JS")
else:
    print("NOT FOUND: script tag")

with open(fp, "w", encoding="utf-8") as f:
    f.write(content)
print("File saved.")
