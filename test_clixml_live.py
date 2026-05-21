# -*- coding: utf-8 -*-
"""实时检测 CLIXML 污染情况"""
import subprocess, sys, os, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CLI = r'C:\Users\15994\AppData\Roaming\npm\node_modules\tencent-channel-cli\node_modules\tencent-channel-cli-win32-x64\bin\tencent-channel-cli.exe'
HOME = r'C:\Users\15994\.openclaw'

def test_cmd(name, args):
    print(f"\n=== {name} ===")
    try:
        r = subprocess.run(
            [CLI] + args,
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            cwd=HOME, timeout=15,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        )
        stdout = (r.stdout or '').strip()
        stderr = (r.stderr or '').strip()
        is_clixml = stdout.startswith('#< CLIXML')
        print(f"  returncode: {r.returncode}")
        print(f"  is_clixml:  {is_clixml}")
        print(f"  stdout_len:  {len(stdout)}")
        if is_clixml:
            print(f"  clixml_preview: {stdout[:300]}")
        else:
            print(f"  stdout_preview: {stdout[:300]}")
        if stderr:
            print(f"  stderr ({len(stderr)}ch): {stderr[:200]}")
        return {'ok': r.returncode == 0, 'clixml': is_clixml, 'stdout': stdout, 'stderr': stderr}
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return {'ok': False, 'error': str(e)}

# 测试1: get-notices
test_cmd('get-notices', ['feed', 'get-notices', '--page-num', '5', '-j'])

# 测试2: push-group-dm-msg dry-run (私信相关)
test_cmd('push-group-dm-msg dry-run', [
    'manage', 'push-group-dm-msg',
    '--ref', '1',
    '--text', 'test-clixml-check',
    '-j', '-y', '--dry-run'
])

print("\n=== 完成 ===")
