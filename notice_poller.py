# -*- coding: utf-8 -*-
"""
notice_poller.py — 通知轮询脚本（替代 notify-daemon 常驻进程）v2

原理：
  notify-daemon 在 Windows 上秒崩（原因不明），但 API 正常。
  本脚本用 Python 循环 + feed get-notices 实现相同功能。

功能：
  1. 定时调用 feed get-notices 检查新通知（互动消息）
  2. 去重：基于 时间+帖子ID+类型 组合键，状态持久化到 JSON
  3. 对"评论"/"@我"类型可触发自动回复（可选）
  4. 对私信通知可通过 --ref 回复（可选）

用法：
  python notice_poller.py              # 默认 30s 轮询，仅日志模式
  python notice_poller.py --interval 60 # 60s 轮询
  python notice_poller.py --once       # 只检查一次后退出
  python notice_poller.py --auto-reply # 开启自动回复（实验性）
  python notice_poller.py --dry-run    # 试运行，不实际发送
"""

import subprocess
import json
import time
import sys
import os
import argparse
import random
from datetime import datetime
from pathlib import Path

# Windows 控制台 UTF-8 修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── 配置 ──
CLI_EXE = r"C:\Users\15994\AppData\Roaming\npm\node_modules\tencent-channel-cli\node_modules\tencent-channel-cli-win32-x64\bin\tencent-channel-cli.exe"
OPENCLAW_HOME = r"C:\Users\15994\.openclaw"
STATE_FILE = Path(OPENCLAW_HOME) / "workspace" / "poller_state.json"
LOG_FILE = Path(OPENCLAW_HOME) / "workspace" / "logs" / "poller.log"

DEFAULT_INTERVAL = 30  # 秒

# 频道配置
GUILD_ID = "43004701636723891"

# 已处理的通知 ID 集合
processed_notice_ids = set()


# ════════════════════════════════════════════════
# 日志
# ════════════════════════════════════════════════

def log(msg: str, level: str = "INFO"):
    """带时间戳的日志输出（同时写文件和 stdout）"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line, flush=True)
    # 写入日志文件
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # 文件日志失败不阻塞主流程


# ════════════════════════════════════════════════
# 状态持久化
# ════════════════════════════════════════════════

def load_state():
    """加载已处理通知的状态文件"""
    global processed_notice_ids
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text("utf-8"))
            processed_notice_ids = set(data.get("processed_ids", []))
            last_update = data.get("updated_at", "未知")
            log(f"状态已加载：{len(processed_notice_ids)} 条历史记录（上次更新：{last_update}）")
        except Exception as e:
            log(f"状态文件读取失败：{e}", "WARN")
    else:
        log("无历史状态文件，首次运行")


def save_state():
    """保存当前处理状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps({
            "processed_ids": list(processed_notice_ids),
            "updated_at": datetime.now().isoformat()
        }, ensure_ascii=False),
        "utf-8"
    )


def _strip_clixml(raw_stdout: str) -> str:
    """
    剥离 PowerShell CLIXML 污染。

    当 Python subprocess 在 Windows PowerShell 环境中执行命令时，
    如果子进程有 stderr 输出（或某些编码问题），PowerShell 会将整个
    stdout 序列化为 CLIXML 格式，类似：
        #< CLIXML
        <Objs Version="1.1.0.1" xmlns="...">
          <S S="Error">错误信息</S>
          <S S="stdout">{"success":true,...}</S>
        </Objs>

    策略：
      1. 先尝试用正则直接从 CLIXML 中找到 {...} JSON 对象（最可靠）
      2. 若无 JSON，则提取所有非 Error 属性的文本节点拼接
      3. 非 CLIXML 输入原样返回
    """
    s = raw_stdout.strip()
    if not s.startswith("#< CLIXML"):
        return raw_stdout

    import re

    # 策略1: 直接从 CLIXML 中提取 JSON 对象（{...} 或 [...]）
    json_match = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
    if json_match:
        candidate = json_match.group(1).strip()
        # 验证确实是合法 JSON
        try:
            json.loads(candidate)
            return candidate
        except (json.JSONDecodeError, ValueError):
            pass

    # 策略2: 提取非 Error 节点的文本内容
    # 匹配 <S ...>content</S> 中不含 S="Error" 的节点
    non_error_texts = []
    for m in re.finditer(r'<S\s+[^>]*>([^<]*)</S>', s):
        tag_prefix = s[m.start():m.start()+20]  # 取开头部分检查属性
        if 'Error' not in tag_prefix:
            text = m.group(1)
            if text.strip():
                non_error_texts.append(text)

    if non_error_texts:
        return "".join(non_error_texts)

    # 都没找到，返回空字符串（至少不返回原始垃圾）
    return ""


# ════════════════════════════════════════════════
# CLI 调用
# ════════════════════════════════════════════════

def run_cli(*args, timeout=30) -> dict:
    """
    调用 tencent-channel-cli.exe，返回解析后的结果
    成功返回 {"ok": True, "data": ..., "raw": ...}
    失败返回 {"ok": False, "error": ..., "raw": ...}
    """
    cmd = [CLI_EXE] + list(args)
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=OPENCLAW_HOME,
            timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        )
        stdout = (r.stdout or "").strip()
        stderr = (r.stderr or "").strip()

        # 剥离可能的 PowerShell CLIXML 污染
        if stdout.startswith("#< CLIXML"):
            log(f"   ⚠️ 检测到 CLIXML 污染（命令: {' '.join(args)}），正在剥离...", "WARN")
            raw_clixml = stdout[:200]  # 记录原始污染片段
            stdout = _strip_clixml(stdout)
            if stdout:
                log(f"   ✅ CLIXML 剥离成功，恢复 JSON 输出", "INFO")
            else:
                log(f"   ❌ CLIXML 剥离失败，原始内容: {raw_clixml}", "ERROR")

        # 尝试从 stdout 解析 JSON
        result = None
        if stdout:
            try:
                result = json.loads(stdout)
            except json.JSONDecodeError:
                pass

        if r.returncode == 0 and result:
            return {"ok": True, "data": result, "raw": stdout, "stderr": stderr}
        else:
            return {"ok": False, "error": stderr or stdout or f"exit code {r.returncode}", "raw": stdout}

    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"命令超时 ({timeout}s)", "raw": ""}
    except Exception as e:
        return {"ok": False, "error": str(e), "raw": ""}


# ════════════════════════════════════════════════
# 核心逻辑：检查通知
# ════════════════════════════════════════════════

def check_notices_once() -> list:
    """
    执行一次通知检查，返回新通知列表
    使用 feed get-notices 获取全量通知，与已处理集合做差集
    """
    result = run_cli("feed", "get-notices", "--page-num", "20", "-j")

    if not result["ok"]:
        log(f"通知检查失败：{result['error'][:200]}", "ERROR")
        return []

    data = result["data"]
    notices = data.get("data", {}).get("notices", [])
    new_notices = []

    for notice in notices:
        # 用 create_time + feed_id + type 组合作为唯一标识
        nid = f"{notice.get('create_time', '')}::{notice.get('feed_id', '')}::{notice.get('type', '')}"
        if nid not in processed_notice_ids:
            notice["_nid"] = nid
            new_notices.append(notice)
            processed_notice_ids.add(nid)

    return new_notices


# ════════════════════════════════════════════════
# 回复引擎
# ════════════════════════════════════════════════

# 简易回复模板库（后续可接 LLM）
REPLY_TEMPLATES = {
    "评论": [
        "感谢分享！这个确实不错~",
        "学到了，感谢大佬科普！",
        "好东西，收藏了",
        "这个角度有意思，之前没注意到",
    ],
    "@我": [
        "我在！有什么可以帮你的？",
        "收到~ 请说",
        "嗯？叫我干嘛(｀・ω・´)",
    ],
    "回复": [
        "说得对~",
        "有道理",
        "同意楼上",
        "哈哈 确实",
    ],
    "默认": [
        "收到消息了~",
        "看到了！",
        "👍",
    ],
}


def generate_reply_text(notice: dict) -> str:
    """根据通知类型生成回复文本（模板模式，可替换为 LLM 调用）"""
    ntype = notice.get("type", "未知")
    templates = REPLY_TEMPLATES.get(ntype, REPLY_TEMPLATES["默认"])
    return random.choice(templates)


def send_comment(feed_id: str, feed_create_time: str, text: str, dry_run: bool = False) -> bool:
    """
    发表顶层评论
    do_comment 必填：feed_id, feed_create_time, comment_type(1=发表)
    """
    args = [
        "feed", "do_comment",
        "--feed-id", feed_id,
        "--feed-create-time", feed_create_time,
        "--comment-type", "1",
        "--text", text,
        "-j", "-y",
    ]
    if dry_run:
        args.insert(2, "--dry-run")

    log(f"   → 发送评论到帖子 {feed_id}: {text[:30]}...")
    result = run_cli(*args)
    if result["ok"]:
        log(f"   ✅ 评论发送成功")
        return True
    else:
        log(f"   ❌ 评论发送失败：{result['error'][:150]}", "ERROR")
        return False


def send_reply(feed_id: str, feed_create_time: str, feed_author_id: str,
               comment_id: str, comment_author_id: str,
               comment_create_time: str, replier_id: str,
               text: str, dry_run: bool = False) -> bool:
    """
    发表回复（回复某条评论）
    do_reply 必填：feed_id, feed_author_id, feed_create_time,
                   comment_id, comment_author_id, comment_create_time,
                   replier_id, reply_type(1=发表)
    """
    args = [
        "feed", "do_reply",
        "--feed-id", feed_id,
        "--feed-create-time", feed_create_time,
        "--feed-author-id", feed_author_id,
        "--comment-id", comment_id,
        "--comment-author-id", comment_author_id,
        "--comment-create-time", comment_create_time,
        "--replier-id", replier_id,
        "--reply-type", "1",
        "--text", text,
        "-j", "-y",
    ]
    if dry_run:
        args.insert(2, "--dry-run")

    log(f"   → 回复评论 {comment_id}: {text[:30]}...")
    result = run_cli(*args)
    if result["ok"]:
        log(f"   ✅ 回复发送成功")
        return True
    else:
        log(f"   ❌ 回复发送失败：{result['error'][:150]}", "ERROR")
        return False


def send_dm_by_ref(ref_num: int, text: str, dry_run: bool = False) -> bool:
    """
    通过通知编号回复私信
    manage push-group-dm-msg --ref N --text "..."
    """
    args = [
        "manage", "push-group-dm-msg",
        "--ref", str(ref_num),
        "--text", text,
        "-j", "-y",
    ]
    if dry_run:
        args.insert(2, "--dry-run")

    log(f"   → 通过 ref=#{ref_num} 发送私信: {text[:30]}...")
    result = run_cli(*args)
    if result["ok"]:
        log(f"   ✅ 私信发送成功")
        return True
    else:
        log(f"   ❌ 私信发送失败：{result['error'][:150]}", "ERROR")
        return False


def send_dm_direct(peer_tiny_id: str, source_guild_id: str, text: str, dry_run: bool = False) -> bool:
    """
    直接发送私信（需要知道对方的 tiny_id）
    manage push-group-dm-msg --peer-tiny-id ... --source-guild-id ... --text ...
    """
    args = [
        "manage", "push-group-dm-msg",
        "--peer-tiny-id", peer_tiny_id,
        "--source-guild-id", source_guild_id,
        "--text", text,
        "-j", "-y",
    ]
    if dry_run:
        args.insert(2, "--dry-run")

    log(f"   → 直接发送私信给 {peer_tiny_id}: {text[:30]}...")
    result = run_cli(*args)
    if result["ok"]:
        log(f"   ✅ 私信发送成功")
        return True
    else:
        log(f"   ❌ 私信发送失败：{result['error'][:150]}", "ERROR")
        return False


# ════════════════════════════════════════════════
# 通知处理器
# ════════════════════════════════════════════════

def handle_new_notice(notice: dict, auto_reply: bool = False, dry_run: bool = False):
    """处理单条新通知，根据类型分发到不同处理器"""
    ntype = notice.get("type", "未知")
    summary = notice.get("summary", "")
    create_time = notice.get("create_time", "")
    feed_id = notice.get("feed_id", "")
    guild_name = notice.get("guild_name", "")

    log(f"[新通知] [{ntype}] {summary}")
    log(f"   来自: {guild_name} | 帖子: {feed_id} | 时间: {create_time}")

    if ntype in ("回复", "评论", "@我"):
        # 帖子互动类 → 可发评论/回复
        if auto_reply:
            reply_text = generate_reply_text(notice)
            # 尝试发顶层评论（如果 notice 中有足够的信息）
            if feed_id and create_time:
                send_comment(feed_id, create_time, reply_text, dry_run=dry_run)
            else:
                log(f"   ⚠️ 缺少 feed_id 或 feed_create_time，无法自动评论", "WARN")
        else:
            log(f"   → （自动回复未开启，跳过）")

    elif ntype == "私信":
        # 私信 → 通过 ref 或 direct 回复
        if auto_reply:
            reply_text = generate_reply_text(notice)
            # 尝试用 ref 模式回复（notice 中可能有 ref 编号）
            ref_num = notice.get("_ref_num") or notice.get("notice_index")
            peer_tiny_id = notice.get("user_tinyid") or notice.get("tiny_id")
            if ref_num:
                send_dm_by_ref(int(ref_num), reply_text, dry_run=dry_run)
            elif peer_tiny_id:
                send_dm_direct(peer_tiny_id, GUILD_ID, reply_text, dry_run=dry_run)
            else:
                log(f"   ⚠️ 缺少 ref_num 和 peer_tiny_id，无法回复私信", "WARN")
                log(f"   → 通知原始数据: {json.dumps(notice, ensure_ascii=False)[:300]}", "DEBUG")
        else:
            log(f"   → （自动回复未开启，跳过）")

    elif ntype in ("帖子点赞", "评论点赞"):
        log(f"   → 点赞通知，忽略")


# ════════════════════════════════════════════════
# 主循环
# ════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="通知轮询守护脚本 v2")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help=f"轮询间隔（秒），默认 {DEFAULT_INTERVAL}")
    parser.add_argument("--auto-reply", action="store_true", help="开启自动回复（模板模式）")
    parser.add_argument("--once", action="store_true", help="只检查一次后退出")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不实际执行回复操作")
    args = parser.parse_args()

    log("=" * 55)
    log("  通知轮询器 v2 启动")
    log(f"  间隔: {args.interval}s | 自动回复: {'ON' if args.auto_reply else 'OFF'} | 试运行: {'ON' if args.dry_run else 'OFF'}")
    log(f"  模式: {'单次' if args.once else '常驻'}")
    log("=" * 55)

    load_state()

    cycle = 0
    consecutive_errors = 0
    MAX_CONSECUTIVE_ERRORS = 5

    try:
        while True:
            cycle += 1
            log(f"\n--- 第 {cycle} 轮 ({datetime.now().strftime('%H:%M:%S')}) ---")

            try:
                new_notices = check_notices_once()
                consecutive_errors = 0  # 成功则重置错误计数

                if new_notices:
                    log(f"发现 {len(new_notices)} 条新通知")
                    for notice in new_notices:
                        handle_new_notice(
                            notice,
                            auto_reply=args.auto_reply,
                            dry_run=args.dry_run,
                        )
                    save_state()
                else:
                    log("无新通知")

            except Exception as e:
                consecutive_errors += 1
                log(f"本轮异常：{e}", "ERROR")
                if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                    log(f"连续 {MAX_CONSECUTIVE_ERRORS} 次错误，停止运行", "ERROR")
                    break

            if args.once:
                log("单次模式，退出")
                break

            log(f"等待 {args.interval}s...")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        log("\n用户中断，正在保存状态...")
        save_state(log("状态已保存，再见！"))
    except Exception as e:
        log(f"致命错误：{e}", "ERROR")
        save_state()
        sys.exit(1)


if __name__ == "__main__":
    main()
