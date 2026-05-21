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
    "content": "2026年12月发售 千值练 RIOBOT AM BOXER 190.99美元\n#超级机器人大战# #微博潮玩家#",
    "file_paths": [
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\DE70272A17F4D4FF517833901F21F1B5.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\C50794453A17B63D1BEFBF91AAC70EF8.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\527011936B4417381CE4D875516EC0D7.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\5070F6454121CEC1BACAFE4C06E7645C.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\FE2839AD26D70D64A00637C49D4A67C2.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\54EECF8A10B9D2B0BB0A867DBAF2A43F.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\6F6F0F27EDA586C43601A87C003A8675.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\DC63906C102E1FC078A9961F6F520789.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\221BA5D53C24E0B8D9F07E76D09D65EC.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\8C2677030673A85F8B460BD06B225DCF.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\8BB2B3E33C68B5DE832059C725FB8DF1.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\786AD2A5FB0BF763B05260E454398AD1.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\259824BCD6346D552DE0B948F8B817C4.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\DCD594F9A5FFC441D24C6A47AE2D4C12.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\A2A42316915D72E0844DF397D057162F.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\26FDD917A05458C41B7E7BCD90E10760.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\5FFD3C5F00B9332E4B6E0A2AD7AF04EC.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\CB4FDA9F1EF1A3F77E785CFDCF49DD1C.jpg"
    ]
})
print(result)
