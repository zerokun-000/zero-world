fp = r"C:\Users\15994\WorkBuddy\Claw\zelo-relationship-graph.html"
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

old = '''<style>
#gate{position:fixed;inset:0;background:#111;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Microsoft YaHei",sans-serif}
#gate h1{color:#d4a843;font-size:28px;letter-spacing:4px;margin-bottom:8px}
#gate p{color:#8b7355;font-size:13px;margin-bottom:24px}
#gate input{background:rgba(20,16,10,.9);border:1px solid #555;border-radius:4px;color:#d4a843;padding:10px 16px;font-size:14px;width:240px;text-align:center;outline:none;font-family:inherit}
#gate input:focus{border-color:#d4a843}
#gate button{margin-top:12px;background:rgba(139,105,20,.3);border:1px solid #8b6914;color:#d4a843;padding:10px 32px;border-radius:4px;cursor:pointer;font-size:14px;font-family:inherit;transition:all .2s}
#gate button:hover{background:#8b6914;color:#000}
#gate .err{color:#e06060;font-size:12px;margin-top:8px;min-height:18px}

*{margin:0;padding:0;box-sizing:border-box}
body{background:#111;color:#ddd;font-family:"Microsoft YaHei","PingFang SC",sans-serif;overflow:hidden;height:100vh}
canvas{display:block;cursor:grab}
canvas:active{cursor:grabbing}

.topbar{position:fixed;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#d4a843,#8b6914,#c03c3c,#8b6914,#d4a843);z-index:10}
.topbar-text{position:fixed;top:12px;left:50%;transform:translateX(-50%);font-size:11px;color:#5a4a2a;letter-spacing:4px;text-transform:uppercase;z-index:10;pointer-events:none}

#search{position:fixed;top:14px;left:20px;z-index:30;background:rgba(20,16,10,.9);border:1px solid #555;border-radius:4px;color:#d4a843;padding:8px 14px;font-size:13px;width:220px;outline:none;font-family:inherit}
#search::placeholder{color:#555}
#search:focus{border-color:#d4a843}

#search-drop{position:fixed;top:52px;left:20px;z-index:30;background:rgba(15,12,8,.97);border:1px solid #8b6914;border-radius:6px;max-height:60vh;overflow-y:auto;display:none;min-width:320px;box-shadow:0 8px 30px rgba(0,0,0,.5)}
#search-drop .drop-section{padding:8px 14px 4px;font-size:10px;color:#8b6914;letter-spacing:3px;text-transform:uppercase;border-bottom:1px solid rgba(139,105,20,.2)}
#search-drop .drop-item{display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;transition:background .2s;border-bottom:1px solid rgba(139,105,20,.08)}
#search-drop .drop-item:hover{background:rgba(139,105,20,.15)}
#search-drop .drop-item:last-child{border-bottom:none}
#search-drop .drop-icon{width:8px;height:8px;border-radius:50%;flex-shrink:0}
#search-drop .drop-name{color:#d4a843;font-size:13px}
#search-drop .drop-sub{color:#8b7355;font-size:11px;margin-left:6px}
#search-drop .drop-type{color:#555;font-size:10px;margin-left:auto}

#controls{position:fixed;top:50px;left:20px;z-index:20;display:flex;flex-direction:column;gap:6px}
.btn{background:rgba(20,16,10,.9);border:1px solid #555;color:#999;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px;font-family:inherit;transition:all .2s}
.btn:hover{background:#8b6914;color:#000;border-color:#8b6914}
#btn-admin{
  display:none;
  position:fixed;top:16px;right:16px;z-index:30;
  background:rgba(13,26,46,.92);border:1px solid rgba(90,128,176,.5);
  color:#5a80b0;width:40px;height:40px;
  border-radius:8px;cursor:pointer;
  font-size:16px;line-height:40px;text-align:center;
  transition:all .2s;
  box-shadow:0 2px 12px rgba(0,0,0,.5);
}
#btn-admin:hover{background:rgba(90,128,176,.3);color:#fff;border-color:rgba(90,128,176,.8)}
#btn-admin.alt{border-color:rgba(212,168,67,.5);color:#d4a843}
#btn-admin.alt:hover{background:rgba(212,168,67,.2)}

#detail{position:fixed;top:20px;right:20px;width:380px;max-height:calc(100vh - 40px);background:rgba(15,12,8,.97);border:1px solid #8b6914;border-radius:8px;overflow:hidden;display:none;z-index:20;box-shadow:0 0 40px rgba(139,105,20,.3)}
#detail.show{display:block}
#d-head{background:linear-gradient(135deg,#1a1208,#2a1f0a);padding:20px;border-bottom:1px solid #8b6914;position:relative}
#d-head .name{font-size:22px;color:#d4a843;letter-spacing:2px}
#d-head .sub{font-size:13px;color:#8b7355;margin-top:4px}
#d-close{position:absolute;top:16px;right:16px;background:none;border:1px solid #8b6914;color:#8b6914;width:28px;height:28px;border-radius:4px;cursor:pointer;font-size:16px;line-height:1}
#d-close:hover{background:#8b6914;color:#000}
#d-body{padding:20px;overflow-y:auto;max-height:calc(100vh - 120px)}
.sec{margin-bottom:18px}
.sec-title{font-size:11px;color:#8b6914;letter-spacing:3px;text-transform:uppercase;margin-bottom:6px}
.sec-text{font-size:14px;line-height:1.8;color:#c0b090}
.quote{font-style:italic;color:#d4a843;border-left:2px solid #8b6914;padding-left:12px;margin-top:6px;display:block}
.rel-item{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(139,105,20,.15);cursor:pointer;transition:background .2s}
.rel-item:hover{background:rgba(139,105,20,.1)}
.rel-arrow{color:#8b6914;font-size:12px}
.rel-name{color:#d4a843;font-size:13px}
.rel-label{color:#8b7355;font-size:11px;margin-left:auto}
.tag{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;margin:2px;background:rgba(139,105,20,.2);border:1px solid #8b6914;color:#d4a843}

.story-link{display:flex;align-items:center;gap:6px;padding:8px 12px;margin:4px 0;background:rgba(200,60,60,.12);border:1px solid rgba(200,60,60,.3);border-radius:4px;cursor:pointer;transition:all .2s}
.story-link:hover{background:rgba(200,60,60,.25);border-color:#c03c3c}
.story-link .sl-icon{color:#c03c3c;font-size:12px}
.story-link .sl-title{color:#e06060;font-size:13px}
.story-link .sl-time{color:#8b7355;font-size:10px;margin-left:auto}
.story-link .sl-anchor{color:#8b6914;font-size:10px;margin-left:6px;font-style:italic}

#legend{position:fixed;bottom:20px;left:20px;background:rgba(15,12,8,.9);border:1px solid rgba(139,105,20,.4);border-radius:6px;padding:14px 18px;font-size:12px;z-index:10}
#legend .lt{color:#8b6914;letter-spacing:2px;font-size:10px;margin-bottom:10px;text-transform:uppercase}
.li{display:flex;align-items:center;gap:8px;margin:5px 0;color:#8b7355}
.ld{width:10px;height:10px;border-radius:50%;flex-shrink:0}

#hint{position:fixed;bottom:20px;right:20px;font-size:11px;color:#444;z-index:10}
#tip{position:fixed;background:rgba(15,12,8,.95);border:1px solid #8b6914;border-radius:4px;padding:8px 12px;font-size:13px;color:#d4a843;pointer-events:none;display:none;z-index:30;max-width:200px}'''

# SVG data URI for circuit board texture - using %23 for # and %3C/%3E for </>
svg_data = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E"
    "%3Cg stroke='%23c9920a' stroke-width='.7' fill='none'%3E"
    "%3Cpath d='M0 20h20M40 0v20M60 0v10M80 20H60M20 40v20M40 60v20"
    "M0 40H20M60 40H80M40 80V60M20 60H0M40 20H60M60 60h20M20 80V60'/%3E"
    "%3Cpath d='M10 10l10 10M50 10l-10 10M30 30l10 10M70 30l-10 10"
    "M10 70l10-10M50 70l-10-10M30 50l10 10M70 50l-10 10'/%3E"
    "%3C/g%3E"
    "%3Cg fill='%23c9920a'%3E"
    "%3Ccircle cx='20' cy='20' r='2.8'/%3E%3Ccircle cx='60' cy='20' r='2.8'/%3E"
    "%3Ccircle cx='20' cy='60' r='2.8'/%3E%3Ccircle cx='60' cy='60' r='2.8'/%3E"
    "%3Ccircle cx='40' cy='40' r='2.8'/%3E"
    "%3Ccircle cx='0' cy='20' r='1.8'/%3E%3Ccircle cx='80' cy='20' r='1.8'/%3E"
    "%3Ccircle cx='0' cy='60' r='1.8'/%3E%3Ccircle cx='80' cy='60' r='1.8'/%3E"
    "%3Ccircle cx='20' cy='0' r='1.8'/%3E%3Ccircle cx='60' cy='0' r='1.8'/%3E"
    "%3Ccircle cx='20' cy='80' r='1.8'/%3E%3Ccircle cx='60' cy='80' r='1.8'/%3E"
    "%3Ccircle cx='40' cy='0' r='1.8'/%3E%3Ccircle cx='40' cy='80' r='1.8'/%3E"
    "%3Ccircle cx='0' cy='40' r='1.8'/%3E%3Ccircle cx='80' cy='40' r='1.8'/%3E"
    "%3C/g%3E%3C/svg%3E"
)

new = '''<style>
/* ============================================================
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
  background-image:url("''' + svg_data + '''");
  background-size:80px 80px;
  opacity:.18;
  transition:opacity .4s;
}
.theme-light::before{opacity:.14}
.theme-light{background:#ffffff}

/* 门页（固定深色） */
#gate{position:fixed;inset:0;background:#111;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Microsoft YaHei",sans-serif}
#gate h1{color:var(--gold);font-size:28px;letter-spacing:4px;margin-bottom:8px}
#gate p{color:#8b7355;font-size:13px;margin-bottom:24px}
#gate input{background:rgba(20,16,10,.9);border:1px solid #555;border-radius:4px;color:var(--gold);padding:10px 16px;font-size:14px;width:240px;text-align:center;outline:none;font-family:inherit}
#gate input:focus{border-color:var(--gold)}
#gate button{margin-top:12px;background:rgba(139,105,20,.3);border:1px solid var(--gold-dim);color:var(--gold);padding:10px 32px;border-radius:4px;cursor:pointer;font-size:14px;font-family:inherit;transition:all .2s}
#gate button:hover{background:var(--gold-dim);color:#000}
#gate .err{color:#e06060;font-size:12px;margin-top:8px;min-height:18px}

*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:"Microsoft YaHei","PingFang SC",sans-serif;overflow:hidden;height:100vh;transition:background .4s,color .4s}
canvas{display:block;cursor:grab}
canvas:active{cursor:grabbing}

.topbar{position:fixed;top:0;left:0;right:0;height:3px;background:var(--topbar-grad);z-index:10;transition:background .4s}
.topbar-text{position:fixed;top:12px;left:50%;transform:translateX(-50%);font-size:11px;color:var(--gold-faint);letter-spacing:4px;text-transform:uppercase;z-index:10;pointer-events:none;transition:color .4s}

#search{position:fixed;top:14px;left:20px;z-index:30;background:var(--panel-bg);border:1px solid var(--border);border-radius:4px;color:var(--gold);padding:8px 14px;font-size:13px;width:220px;outline:none;font-family:inherit;transition:background .4s,border-color .4s,color .4s}
#search::placeholder{color:var(--gold-faint)}
#search:focus{border-color:var(--gold)}

#search-drop{position:fixed;top:52px;left:20px;z-index:30;background:var(--panel-bg);border:1px solid var(--border);border-radius:6px;max-height:60vh;overflow-y:auto;display:none;min-width:320px;box-shadow:0 8px 30px rgba(0,0,0,.5);transition:background .4s,border-color .4s}
#search-drop .drop-section{padding:8px 14px 4px;font-size:10px;color:var(--gold-dim);letter-spacing:3px;text-transform:uppercase;border-bottom:1px solid var(--border)}
#search-drop .drop-item{display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;transition:background .2s;border-bottom:1px solid var(--border)}
#search-drop .drop-item:hover{background:rgba(139,105,20,.15)}
#search-drop .drop-item:last-child{border-bottom:none}
#search-drop .drop-icon{width:8px;height:8px;border-radius:50%;flex-shrink:0}
#search-drop .drop-name{color:var(--gold);font-size:13px}
#search-drop .drop-sub{color:#8b7355;font-size:11px;margin-left:6px}
#search-drop .drop-type{color:var(--gold-faint);font-size:10px;margin-left:auto}

#controls{position:fixed;top:50px;left:20px;z-index:20;display:flex;flex-direction:column;gap:6px}
.btn{background:var(--panel-bg);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px;font-family:inherit;transition:all .2s}
.btn:hover{background:var(--gold-dim);color:#000}

/* 主题切换按钮 */
#btn-theme{
  position:fixed;top:16px;right:70px;z-index:30;
  background:var(--panel-bg);border:1px solid var(--border);
  color:var(--gold);width:40px;height:40px;
  border-radius:8px;cursor:pointer;
  font-size:18px;line-height:40px;text-align:center;
  transition:all .3s;
  box-shadow:0 2px 12px rgba(0,0,0,.4);
}
#btn-theme:hover{background:var(--gold-dim);color:#000;border-color:var(--gold-dim)}

#btn-admin{
  display:none;
  position:fixed;top:16px;right:16px;z-index:30;
  background:rgba(13,26,46,.92);border:1px solid rgba(90,128,176,.5);
  color:#5a80b0;width:40px;height:40px;
  border-radius:8px;cursor:pointer;
  font-size:16px;line-height:40px;text-align:center;
  transition:all .2s;
  box-shadow:0 2px 12px rgba(0,0,0,.5);
}
#btn-admin:hover{background:rgba(90,128,176,.3);color:#fff;border-color:rgba(90,128,176,.8)}
#btn-admin.alt{border-color:rgba(212,168,67,.5);color:var(--gold)}
#btn-admin.alt:hover{background:rgba(212,168,67,.2)}

#detail{position:fixed;top:20px;right:20px;width:380px;max-height:calc(100vh - 40px);background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;overflow:hidden;display:none;z-index:20;box-shadow:0 0 40px rgba(139,105,20,.3);transition:background .4s,border-color .4s}
#detail.show{display:block}
#d-head{background:linear-gradient(135deg,#1a1208,#2a1f0a);padding:20px;border-bottom:1px solid var(--border);position:relative}
#d-head .name{font-size:22px;color:var(--gold);letter-spacing:2px}
#d-head .sub{font-size:13px;color:#8b7355;margin-top:4px}
#d-close{position:absolute;top:16px;right:16px;background:none;border:1px solid var(--border);color:var(--gold-dim);width:28px;height:28px;border-radius:4px;cursor:pointer;font-size:16px;line-height:1}
#d-close:hover{background:var(--gold-dim);color:#000}
#d-body{padding:20px;overflow-y:auto;max-height:calc(100vh - 120px)}
.sec{margin-bottom:18px}
.sec-title{font-size:11px;color:var(--gold-dim);letter-spacing:3px;text-transform:uppercase;margin-bottom:6px}
.sec-text{font-size:14px;line-height:1.8;color:#c0b090}
.quote{font-style:italic;color:var(--gold);border-left:2px solid var(--gold-dim);padding-left:12px;margin-top:6px;display:block}
.rel-item{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border);cursor:pointer;transition:background .2s}
.rel-item:hover{background:rgba(139,105,20,.1)}
.rel-arrow{color:var(--gold-dim);font-size:12px}
.rel-name{color:var(--gold);font-size:13px}
.rel-label{color:#8b7355;font-size:11px;margin-left:auto}
.tag{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;margin:2px;background:rgba(139,105,20,.2);border:1px solid var(--border);color:var(--gold)}

.story-link{display:flex;align-items:center;gap:6px;padding:8px 12px;margin:4px 0;background:rgba(200,60,60,.12);border:1px solid rgba(200,60,60,.3);border-radius:4px;cursor:pointer;transition:all .2s}
.story-link:hover{background:rgba(200,60,60,.25);border-color:#c03c3c}
.story-link .sl-icon{color:#c03c3c;font-size:12px}
.story-link .sl-title{color:#e06060;font-size:13px}
.story-link .sl-time{color:#8b7355;font-size:10px;margin-left:auto}
.story-link .sl-anchor{color:var(--gold-dim);font-size:10px;margin-left:6px;font-style:italic}

#legend{position:fixed;bottom:20px;left:20px;background:var(--panel-bg);border:1px solid var(--border);border-radius:6px;padding:14px 18px;font-size:12px;z-index:10;transition:background .4s,border-color .4s}
#legend .lt{color:var(--gold-dim);letter-spacing:2px;font-size:10px;margin-bottom:10px;text-transform:uppercase}
.li{display:flex;align-items:center;gap:8px;margin:5px 0;color:#8b7355}
.ld{width:10px;height:10px;border-radius:50%;flex-shrink:0}

#hint{position:fixed;bottom:20px;right:20px;font-size:11px;color:var(--gold-faint);z-index:10;transition:color .4s}
#tip{position:fixed;background:var(--panel-bg);border:1px solid var(--border);border-radius:4px;padding:8px 12px;font-size:13px;color:var(--gold);pointer-events:none;display:none;z-index:30;max-width:200px;transition:background .4s,border-color .4s,color .4s}'''

if old in content:
    content = content.replace(old, new, 1)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK")
else:
    idx = content.find('<style>')
    print("NOT FOUND, found <style> at", idx)
    if idx >= 0:
        print(repr(content[idx:idx+200]))
