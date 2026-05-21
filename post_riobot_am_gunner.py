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
    "content": "2027年1月发售 千值练 RIOBOT AM GUNNER 204.99美元\n#超级机器人大战# #微博潮玩家#",
    "file_paths": [
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\3B50A590704CEFF8E8B5EB6130A3E49E.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\031743F39CA4C5C2F64A441BD2DBF55E.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\824A39024A9F2DBA7BA8583877B9139D.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\B62A379D6FA714A2981AE61550B5FCF9.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\9C07178572C734AE25F0EA8B181A9F46.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\ED69A2FDD82E1F045D1309C4413CC797.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\9D54E5DDBFE421C00852B1923E398154.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\DCCDD8C68568C7ADB8500DAEDC5099D7.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\6383DF0DD40DCEDA43288C7D7A69A9DF.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\786AD2A5FB0BF763B05260E454398AD1.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\D5230085A24D5250D42E3D96AFE86E0F.jpg",
        r"C:\Users\15994\AppData\Local\Temp\workbuddy-qqbot-media\inbound\159A2354AE4595DF9940C031D76411B0.jpg"
    ]
})
print(result)
