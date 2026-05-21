"""
每日自动互动脚本
- 获取频道最新帖子
- 对非 Bot/频道助手的帖子批量点赞
- 发布每日互动报告到「新品情报站」
"""
import subprocess
import json
import time
import sys
import re
from datetime import datetime

# === 配置 ===
CLI_PATH = r"C:\Users\15994\AppData\Roaming\npm\node_modules\tencent-channel-cli\node_modules\tencent-channel-cli-win32-x64\bin\tencent-channel-cli.exe"
GUILD_ID = "43004701636723891"
CHANNEL_ID = "1772727"  # 新品情报站
BOT_AUTHOR_ID = "144115218627319664"
CHANNEL_ASSISTANT_ID = "144115220736883034"
SKIP_AUTHORS = {BOT_AUTHOR_ID, CHANNEL_ASSISTANT_ID}
FEED_COUNT = 20
INTERVAL_SEC = 5  # 点赞间隔，避免频率限制


def run_cli(args: list) -> dict:
    """执行 tencent-channel-cli 命令，返回解析后的 JSON"""
    cmd = [CLI_PATH] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        out = result.stdout.strip()
        # 尝试解析 JSON
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            return {"success": False, "error": f"非JSON输出: {out[:200]}", "raw": out}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "命令超时"}
    except FileNotFoundError:
        return {"success": False, "error": f"CLI 不存在: {CLI_PATH}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_guild_feeds(count: int = 20) -> list:
    """获取频道最新帖子"""
    print(f"[1/3] 正在获取最新 {count} 条帖子...")
    res = run_cli(["feed", "get-guild-feeds", "--guild-id", GUILD_ID, "--get-type", "2", "--count", str(count)])
    if not res.get("success"):
        print(f"  ❌ 获取帖子失败: {res.get('error')}")
        return []
    feeds = res.get("data", {}).get("feeds", [])
    print(f"  ✅ 获取到 {len(feeds)} 条帖子")
    return feeds


def like_feed(feed_id: str, guild_id: str, author: str, title: str, prefer_count: int) -> dict:
    """点赞单条帖子"""
    res = run_cli(["feed", "do-feed-prefer",
                   "--feed-id", feed_id,
                   "--action", "1",
                   "--guild-id", guild_id])
    return {
        "success": res.get("success", False),
        "new_count": res.get("data", {}).get("prefer_count", "?"),
        "error": res.get("error"),
        "author": author,
        "title": title,
        "old_count": prefer_count,
    }


def build_report(liked: list, skipped: list, failed: list) -> str:
    """生成每日互动报告正文"""
    today = datetime.now().strftime("%Y-%m-%d")
    total = len(liked)
    skipped_n = len(skipped)
    failed_n = len(failed)

    lines = [
        f"# 🤖 每日自动互动报告 | {today}",
        "",
        f"**统计：** 点赞 {total} 条 | 跳过 {skipped_n} 条 | 失败 {failed_n} 条",
        "",
        "---",
        "",
        "## ✅ 点赞成功",
        "",
    ]

    if liked:
        for item in liked:
            lines.append(f"- {item['author']}：{item['title']}（{item['old_count']} → {item['new_count']}赞）")
    else:
        lines.append("（今日无新增帖子可互动）")

    if skipped:
        lines.extend(["", "## ⏭ 跳过（Bot自身 / 频道助手）", ""])
        for item in skipped:
            lines.append(f"- {item['author']}：{item['title']}")

    if failed:
        lines.extend(["", "## ❌ 点赞失败", ""])
        for item in failed:
            lines.append(f"- {item['author']}：{item['title']}（{item['error']}）")

    lines.extend(["", "---", "", "🤖 由 Bot 自动执行 · 每日 15:00 定时运行"])
    return "\n".join(lines)


def publish_report(content: str) -> dict:
    """发布报告到新品情报站"""
    print("\n[3/3] 正在发布每日互动报告到新品情报站...")
    res = run_cli([
        "feed", "publish-feed",
        "--guild-id", GUILD_ID,
        "--channel-id", CHANNEL_ID,
        "--content", content,
    ])
    return res


def main():
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"========== 每日自动互动 | {today_str} ==========\n")

    # Step 1: 获取帖子
    feeds = get_guild_feeds(FEED_COUNT)
    if not feeds:
        print("无可用帖子，退出")
        sys.exit(1)

    # Step 2: 逐条点赞
    liked = []
    skipped = []
    failed = []

    print(f"\n[2/3] 开始点赞（共 {len(feeds)} 条）...")
    for i, feed in enumerate(feeds, 1):
        fid = feed.get("feed_id", "")
        author_id = str(feed.get("author_id", ""))
        author = feed.get("author", "未知用户")
        title = feed.get("title") or feed.get("content_text", "（无标题）")
        # 标题最多显示 30 字
        title_short = title[:30] + "…" if len(title) > 30 else title
        prefer_count = feed.get("prefer_count", 0)

        if author_id in SKIP_AUTHORS:
            print(f"  [{i}/{len(feeds)}] ⏭ 跳过 Bot/助手: {title_short}")
            skipped.append({"author": author, "title": title, "feed_id": fid})
            continue

        result = like_feed(fid, GUILD_ID, author, title, prefer_count)

        if result["success"]:
            new_c = result["new_count"]
            print(f"  [{i}/{len(feeds)}] ✅ 点赞成功: {title_short} ({prefer_count} → {new_c}赞)")
            liked.append({
                "author": author,
                "title": title,
                "old_count": prefer_count,
                "new_count": new_c,
                "feed_id": fid,
            })
        else:
            err = result["error"] or "未知错误"
            print(f"  [{i}/{len(feeds)}] ❌ 点赞失败: {title_short}  错误: {err}")
            failed.append({"author": author, "title": title, "error": err, "feed_id": fid})

        # 频率限制保护
        time.sleep(INTERVAL_SEC)

    # Step 3: 生成并发布报告
    report = build_report(liked, skipped, failed)
    pub_res = publish_report(report)

    print("\n========== 执行完成 ==========")
    print(f"点赞成功: {len(liked)} 条")
    print(f"跳过: {len(skipped)} 条")
    print(f"失败: {len(failed)} 条")

    if pub_res.get("success"):
        feed_id = pub_res.get("data", {}).get("feed_id", "")
        share_link = f"https://pd.qq.com/s/{"_".join(feed_id.split('_')[1:]) if feed_id else "unknown"}"
        print(f"\n📝 报告已发布！Feed ID: {feed_id}")
        print(f"🔗 链接: {share_link}")
    else:
        print(f"\n⚠️ 报告发布失败: {pub_res.get('error')}")

    # 返回结果供调用方使用
    return {
        "liked": liked,
        "skipped": skipped,
        "failed": failed,
        "report": report,
        "publish_result": pub_res,
    }


if __name__ == "__main__":
    main()
