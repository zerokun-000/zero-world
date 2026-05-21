# -*- coding: utf-8 -*-
"""
系统自检脚本 - 测试 Bot 发帖功能
如果返回 auth failed，说明 Token 已过期，需要重新获取
"""
import sys, os, json
os.chdir(r'C:\Users\15994\.openclaw\workspace\skills\tencent-channel-community')
sys.path.insert(0, 'scripts/feed/write')
from publish_feed import run

result = run({
    'guild_id': '43004701636723891',
    'channel_id': '1772727',
    'feed_type': 1,
    'content': '[系统自检] Bot功能验证帖\n#超级机器人大战# #微博潮玩家#',
    'file_paths': []
})
print(json.dumps(result, ensure_ascii=False))