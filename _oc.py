"""OpenClaw 修复工具 v5 - 带 CLIXML 污染剥离"""
import subprocess
import os
import json
import re

OPENCLAW_HOME = r"C:\Users\15994\.openclaw"
CMD_EXE = r"C:\Windows\System32\cmd.exe"
OPENCLAW_CMD = r"C:\Users\15994\AppData\Roaming\npm\openclaw.cmd"


def _strip_clixml(raw_stdout):
    """
    剥离 PowerShell CLIXML 污染。
    
    Windows 上 subprocess.run 执行命令时，若子进程有 stderr 输出，
    PowerShell 会将 stdout 序列化为 CLIXML XML 格式。
    
    策略：
      1. 正则提取 {...} 或 [...] JSON 对象（最可靠）
      2. 提取非 Error 节点的文本内容拼接
      3. 非 CLIXML 输入原样返回
    """
    s = raw_stdout.strip()
    if not s.startswith("#< CLIXML"):
        return raw_stdout

    # 策略1: 提取 JSON 对象
    json_match = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
    if json_match:
        candidate = json_match.group(1).strip()
        try:
            json.loads(candidate)
            return candidate
        except (json.JSONDecodeError, ValueError):
            pass

    # 策略2: 非 Error 文本节点
    non_error_texts = []
    for m in re.finditer(r'<S\s+[^>]*>([^<]*)</S>', s):
        tag_prefix = s[m.start():m.start()+20]
        if 'Error' not in tag_prefix:
            text = m.group(1)
            if text.strip():
                non_error_texts.append(text)

    if non_error_texts:
        return "".join(non_error_texts)

    return ""


def run_openclaw(*args):
    r"""
    cmd.exe /c "full\path\to\openclaw.cmd" arg1 arg2
    自动剥离 CLIXML 污染后解析 JSON
    """
    # 构建命令: cmd.exe /c "C:\...\openclaw.cmd" health
    cmd_parts = [OPENCLAW_CMD] + list(args)
    
    print(f"\n>>> openclaw {' '.join(args)}")
    
    r = subprocess.run(
        [CMD_EXE, "/c"] + cmd_parts,
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        cwd=OPENCLAW_HOME,
        timeout=20,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()

    # ⭐ 关键：剥离 CLIXML 污染
    out = _strip_clixml(out)
    
    if out:
        try:
            data = json.loads(out)
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception:
            print(out[:2000])
    if err:
        print(f"[ERR] {err[:800]}")
    print(f"RC: {r.returncode}")
    return r


if __name__ == "__main__":
    import sys
    
    actions = [
        ("health", ["health"]),
        ("notices-status", ["notices-status", "--json"]),
        ("check-notices", ["check-notices"]),
        ("notices-on", ["notices-on"]),
    ]
    
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        for name, args in actions:
            if target in name.lower():
                print("=" * 50)
                print(name.upper())
                print("=" * 50)
                run_openclaw(*args)
                break
        else:
            print(f"未知目标: {sys.argv[1]}")
    else:
        for name, args in actions:
            print("=" * 50)
            print(name.upper())
            print("=" * 50)
            run_openclaw(*args)
