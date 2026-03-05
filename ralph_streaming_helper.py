#!/usr/bin/env python3
"""
Ralph 流式输出助手
使用 Python 的 subprocess 实现真正的流式输出
"""

import subprocess
import sys
import os
import select
import platform

def run_claude_streaming(instruction_file, log_file):
    """
    以流式方式运行 Claude Code
    实时显示输出并保存到日志
    """
    # 读取指令
    with open(instruction_file, 'r', encoding='utf-8') as f:
        instruction = f.read()

    # 构建命令
    cmd = ['claude', '--dangerously-skip-permissions']

    # Windows 下需要使用特殊处理
    is_windows = platform.system() == 'Windows'

    try:
        # 创建进程，使用 PTY 模式（如果可能）
        if is_windows:
            # Windows: 使用 Popen with PIPE
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True
            )
        else:
            # Unix/Mac: 使用 PTY
            import pty
            master, slave = pty.openpty()
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=slave,
                stderr=slave,
                text=True,
                bufsize=0  # 无缓冲
            )
            os.close(slave)

        # 发送指令
        if process.stdin:
            process.stdin.write(instruction)
            process.stdin.flush()
            process.stdin.close()

        # 打开日志文件
        with open(log_file, 'w', encoding='utf-8') as log:
            if is_windows:
                # Windows: 从 PIPE 读取
                for line in process.stdout:
                    # 实时显示
                    print(line, end='', flush=True)
                    # 写入日志
                    log.write(line)
                    log.flush()
            else:
                # Unix/Mac: 从 PTY 读取
                while True:
                    try:
                        # 使用 select 检查是否有数据可读
                        r, _, _ = select.select([master], [], [], 0.1)
                        if r:
                            data = os.read(master, 1024)
                            if not data:
                                break
                            text = data.decode('utf-8', errors='ignore')
                            # 实时显示
                            print(text, end='', flush=True)
                            # 写入日志
                            log.write(text)
                            log.flush()
                        elif process.poll() is not None:
                            # 进程已退出
                            break
                    except OSError:
                        break

        # 等待进程结束
        return_code = process.wait()
        return return_code

    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python ralph_streaming_helper.py <instruction_file> <log_file>")
        sys.exit(1)

    instruction_file = sys.argv[1]
    log_file = sys.argv[2]

    exit_code = run_claude_streaming(instruction_file, log_file)
    sys.exit(exit_code)
