# notice_poller.py — 部署指南

## 是什么
替代 `notify-daemon` 的通知轮询脚本。因为官方 daemon 在 Windows 上秒崩，
用 Python 循环调用 `feed get-notices` 实现相同功能。

## 文件位置
- 脚本: `c:\Users\15994\WorkBuddy\Claw\notice_poller.py`
- 状态文件: `C:\Users\15994\.openclaw\workspace\poller_state.json`
- 日志文件: `C:\Users\15994\.openclaw\workspace\logs\poller.log`

## 快速开始

### 1. 单次检查（调试用）
```bash
python notice_poller.py --once
```

### 2. 常驻运行（前台）
```bash
python notice_poller.py --interval 30
```
Ctrl+C 可安全退出。

### 3. 常驻运行（后台，推荐）

#### 方式 A：start /B（简单）
```bash
cd c:\Users\15994\WorkBuddy\Claw
start /B pythonw.exe notice_poller.py --interval 30 > nul 2>&1
```
`pythonw.exe` 不弹控制台窗口。关闭终端不会杀进程。

#### 方式 B：Windows 计划任务（开机自启）
1. 打开「任务计划程序」
2. 创建基本任务 → 触发器「计算机启动时」
3. 操作「启动程序」:
   ```
   程序: C:\Users\15994\.workbuddy\binaries\python\versions\3.13.12\pythonw.exe
   参数: c:\Users\15994\WorkBuddy\Claw\notice_poller.py --interval 30
   起始目录: c:\Users\15994\WorkBuddy\Claw
   ```

### 4. 开启自动回复
```bash
python notice_poller.py --auto-reply --interval 30
```
当前是模板回复模式（随机选一句）。可替换 `generate_reply_text()` 接入 LLM。

## 参数一览

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--interval N` | 30 | 轮询间隔（秒） |
| `--once` | - | 只检查一次后退出 |
| `--auto-reply` | 关 | 开启自动回复 |
| `--dry-run` | 关 | 试运行，不实际发送 |

## 日志查看
```bash
type C:\Users\15994\.openclaw\workspace\logs\poller.log
```

## 停止运行
- 前台模式: Ctrl+C
- 后台模式: 任务管理器结束 pythonw.exe 进程

## 架构说明

```
[feed get-notices] → 解析通知列表 → 与 poller_state.json 做差集
                                         ↓
                                   新通知？
                                  /       \
                                有         无
                                ↓           ↓
                    handle_new_notice()   sleep(interval)
                                ↓
                   ┌────────────┼────────────┐
                   │            │            │
               评论/@我      私信         点赞
                   │            │            │
              send_comment()  send_dm()    忽略
              send_reply()
```
