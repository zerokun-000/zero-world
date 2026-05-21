# -*- coding: utf-8 -*-
import sys
import os
os.chdir(r"C:\Users\15994\.openclaw\workspace\skills\tencent-channel-community")
sys.path.insert(0, 'scripts/feed/write')

from publish_feed import run

result = run({
    "guild_id": "43004701636723891",
    "channel_id": "1772727",
    "feed_type": 1,
    "content": "2026年10月发售 SHF 弗利萨 第四形态〈深不可测的宇宙第一力量〉4000日元",
    "file_paths": [
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\B00A6C85DA0A3D97B61C2FD5D5F753D8.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\1D3E60ECDF6D5F8448AE1AE777CDAF69.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\B66B76A39E45B65C7D5E5F022AB94A44.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\503CBC2ACF2EEC5BABEAEF64DEF993AC.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\4909D8199F695CB990135D93248594BF.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\023936F2F693DE031664F09E09D2DC54.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\C49D5E7A5CA356498C356C25937E7B55.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\43FD9D180A55C3AEBD46DDE14FFC05A8.jpg"
    ]
})
print(result)