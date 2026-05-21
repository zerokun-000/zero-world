"""
批量对频道帖子点赞（排除自己 Bot 和频道助手发的帖子）
"""
import sys
import os
import time
import json

sys.path.insert(0, r"C:\Users\15994\.openclaw\workspace\skills\tencent-channel-community\scripts\feed\read")
sys.path.insert(0, r"C:\Users\15994\.openclaw\workspace\skills\tencent-channel-community\scripts\feed\write")
sys.path.insert(0, r"C:\Users\15994\.openclaw\workspace\skills\tencent-channel-community\scripts\feed")

from get_guild_feeds import run as get_feeds
from do_feed_prefer import run as do_prefer

GUILD_ID = "43004701636723891"
BOT_AUTHOR_ID = "144115218627319664"
CHANNEL_ASSISTANT_ID = "144115220736883034"

SKIP_AUTHORS = {BOT_AUTHOR_ID, CHANNEL_ASSISTANT_ID}

def fetch_all_feeds(count=20):
    """拉取最新帖子"""
    result = get_feeds({"guild_id": GUILD_ID, "get_type": 2, "count": count})
    if not result.get("success"):
        print(f"[ERROR] 获取帖子失败: {result.get('error')}")
        return []
    feeds = result["data"].get("feeds", [])
    return feeds

def like_feeds(feeds):
    liked = []
    skipped = []
    failed = []
    
    for feed in feeds:
        fid = feed["feed_id"]
        author = feed["author"]
        author_id = str(feed["author_id"])
        title = feed.get("title", "（无标题）")
        prefer_count = feed.get("prefer_count", 0)
        
        if author_id in SKIP_AUTHORS:
            skipped.append(f"  ⏭ 跳过【{author}】: {title}")
            continue
        
        result = do_prefer({
            "feed_id": fid,
            "action": 1,  # 点赞
            "guild_id": GUILD_ID,
        })
        
        if result.get("success"):
            new_count = result["data"].get("prefer_count", "?")
            liked.append(f"  ✅ 点赞成功【{author}】: {title}  ({prefer_count} → {new_count}赞)")
        else:
            err = result.get("error", "未知错误")
            failed.append(f"  ❌ 点赞失败【{author}】: {title}  错误: {err}")
        
        time.sleep(0.5)  # 避免频率限制
    
    return liked, skipped, failed

if __name__ == "__main__":
    print("=== 批量点赞开始 ===")
    feeds = fetch_all_feeds(count=20)
    print(f"获取到 {len(feeds)} 条帖子")
    
    liked, skipped, failed = like_feeds(feeds)
    
    print(f"\n点赞结果（{len(liked)} 成功 / {len(skipped)} 跳过 / {len(failed)} 失败）：")
    for line in liked:
        print(line)
    if skipped:
        print("\n跳过（Bot自身/频道助手）：")
        for line in skipped:
            print(line)
    if failed:
        print("\n失败：")
        for line in failed:
            print(line)
    
    print("\n=== 批量点赞完成 ===")
