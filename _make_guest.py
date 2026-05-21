"""
从 zelo-relationship-graph.html 生成访客版 zelo-guest.html
移除所有管理员相关内容
"""
import re

with open('zelo-relationship-graph.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 移除 btn-admin CSS 块
content = re.sub(
    r'\n#btn-admin\{[^}]*\}#btn-admin:hover[^\n]*\n#btn-admin\.alt[^\n]*\n#btn-admin\.alt:hover[^\n]*\n',
    '\n/* [guest] admin btn removed */\n', content)

# 2. 移除 admin-entry CSS 块
content = re.sub(
    r'\n/\* 管理员入口选择 \*/\n#admin-entry[^{]*\{[^}]*\n#admin-entry\.show[^\n]*\n',
    '\n/* [guest] admin-entry removed */\n', content)

# 3. 移除 admin-panel CSS 块
content = re.sub(
    r'\n/\* 管理局后台面板 \*/\n#admin-panel[^{]*\{[^}]*\n#admin-panel\.show[^\n]*\n',
    '\n/* [guest] admin-panel removed */\n', content)

# 4. 移除 admin-back-btn CSS
content = re.sub(
    r'\n\.admin-back-btn[^\n]*\n\.admin-back-btn:hover[^\n]*\n',
    '\n/* [guest] admin-back-btn removed */\n', content)

# 5. 移除 btn-admin HTML 按钮
content = re.sub(r'\s*<button id="btn-admin"[^>]*>[^<]*</button>\n', '\n', content)

# 6. 移除 btn-admin 移动端 CSS
content = re.sub(r'\s*/\* 管理后台悬浮按钮 \*/\n\s*#btn-admin\{[^}]*\}\n', '\n', content)

# 7. 移除 admin-entry HTML
content = re.sub(
    r'\s*<!-- 管理员入口选择 -->\s*\n<div id="admin-entry">.*?</div>\s*\n',
    '\n<!-- [guest] admin-entry removed -->\n', content, flags=re.DOTALL)

# 8. 移除 admin-panel HTML
content = re.sub(
    r'\s*<!-- 管理局后台面板 -->\s*\n<div id="admin-panel">.*?</div>\s*\n',
    '\n<!-- [guest] admin-panel removed -->\n', content, flags=re.DOTALL)

# 9. 移除 btn-log 的 right:100px 移动端修正（因为 admin 按钮不在了）
content = re.sub(r'#btn-log\{top:12px;right:100px', '#btn-log{top:12px;right:58px', content)

# 10. 移除 JS: isOwner 变量
content = re.sub(r'\nvar isOwner = false;\n', '\n// [guest] isOwner not used\n', content)

# 11. 移除 checkPw 中的 admin 分支
content = re.sub(
    r"\s*if\(input === \"zero000\"\)\{[^}]*isOwner = true;[^\}]*showAdminEntry\(\);[^\}]*\}\n",
    '\n/* [guest] admin login removed */\n', content)

# 12. 移除 showDetail 中的管理员入口
content = re.sub(
    r'\s*// 管理局后台入口（仅 isOwner 可见.*?\n\s*if\(window\.isOwner\)\{[^}]*\}\n',
    '\n/* [guest] admin detail button removed */\n', content)

# 13. 移除 enterMember 中显示管理员按钮的代码
content = re.sub(
    r"\s*// 显示管理局按钮\n\s*var btn = document\.getElementById\('btn-admin'\);[^\n]*\n",
    '\n', content)

# 14. 移除 Ctrl+Shift+A 快捷键
content = re.sub(
    r'\s*// 管理员快捷键：Ctrl\+Shift\+A.*?\}\);\n',
    '\n/* [guest] admin shortcut removed */\n', content, flags=re.DOTALL)

# 15. 移除 window.showAdminEntry 等导出
content = re.sub(r"\s*window\.showAdminEntry = showAdminEntry;\n", '\n', content)
content = re.sub(r"\s*window\.enterMember = enterMember;\n", '\n', content)
content = re.sub(r"\s*window\.enterAdminBackend = enterAdminBackend;\n", '\n', content)
content = re.sub(r"\s*window\.closeAdminPanel = closeAdminPanel;\n", '\n', content)
content = re.sub(r"\s*window\.refreshAdminRecords = refreshAdminRecords;\n", '\n', content)

# 16. 移除 showAdminEntry / enterAdminBackend / closeAdminPanel / refreshAdminRecords 函数定义
content = re.sub(
    r'\s*function showAdminEntry\(\)\{[^}]*\}\n',
    '\n/* [guest] showAdminEntry removed */\n', content)
content = re.sub(
    r'\s*function enterMember\(\)\{[^}]*\}\n',
    '\n/* [guest] enterMember removed */\n', content)
content = re.sub(
    r'\s*function enterAdminBackend\(\)\{[^}]*\}\n',
    '\n/* [guest] enterAdminBackend removed */\n', content)
content = re.sub(
    r'\s*function closeAdminPanel\(\)\{[^}]*\}\n',
    '\n/* [guest] closeAdminPanel removed */\n', content)
content = re.sub(
    r'\s*function refreshAdminRecords\(\)\{[^}]*\}\n',
    '\n/* [guest] refreshAdminRecords removed */\n', content)

# 17. 移除 updateLogButton（如果有的话）
content = re.sub(
    r'\s*function updateLogButton\(\)\{[^}]*\}\n',
    '\n/* [guest] updateLogButton removed */\n', content)

# 18. 更新标题
content = re.sub(r'<title>泽罗 · 角色关系图</title>', '<title>泽罗 · 角色关系图（访客）</title>', content)

with open('zelo-guest.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Guest version written to zelo-guest.html")
