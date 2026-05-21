# -*- coding: utf-8 -*-
"""临时测试：CLIXML 剥离逻辑 v2"""
import re
import json
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _strip_clixml(raw_stdout):
    s = raw_stdout.strip()
    if not s.startswith("#< CLIXML"):
        return raw_stdout

    # 策略1: 直接从 CLIXML 中提取 JSON 对象
    json_match = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
    if json_match:
        candidate = json_match.group(1).strip()
        try:
            json.loads(candidate)
            return candidate
        except (json.JSONDecodeError, ValueError):
            pass

    # 策略2: 提取非 Error 节点的文本内容
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


# 测试1: 混合 Error + JSON stdout
clixml1 = """#< CLIXML
<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
  <S S="Error">warning: something happened</S>
  <S S="stdout">{"data":{"notices":[]},"success":true}</S>
</Objs>"""
r1 = _strip_clixml(clixml1)
d1 = json.loads(r1)
print(f"Test1 OK: {d1}")

# 测试2: 正常JSON原样通过
normal = '{"hello":"world"}'
assert _strip_clixml(normal) == normal
print("Test2 OK")

# 测试3: 只有Error没有stdout → 返回空
err_only = "#< CLIXML\n<Objs><S S=\"Error\">boom</S></Objs>"
r3 = _strip_clixml(err_only)
assert r3 == "", f"expected empty, got {repr(r3)}"
print("Test3 OK")

# 测试4: 多个非Error节点拼接
multi = """#< CLIXML
<Objs><S S="Info">line1</S><S S="Info">line2</S></Objs>"""
r4 = _strip_clixml(multi)
assert "line1" in r4 and "line2" in r4
print("Test4 OK")

# 测试5: 空输入
assert _strip_clixml("") == ""
print("Test5 OK")

print("\nAll tests passed!")
