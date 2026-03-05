# 使用Claude Code构建多Agent系统的技术方案调研报告

> 基于现有系统架构的深入分析与实践指南

---

## 📋 目录

1. [Claude Code CLI工具调用能力](#1-claude-code-cli工具调用能力)
2. [并行运行多个Claude Code实例](#2-并行运行多个claude-code实例)
3. [Agent间通信机制设计](#3-agent间通信机制设计)
4. [文件操作工具使用示例](#4-文件操作工具使用示例)
5. [进程管理和资源控制](#5-进程管理和资源控制)
6. [完整多Agent协作架构](#6-完整多agent协作架构)
7. [实践代码示例](#7-实践代码示例)

---

## 1. Claude Code CLI工具调用能力

### 1.1 核心工具集

Claude Code CLI提供以下工具（通过工具函数调用）：

| 工具名称 | 功能描述 | 使用场景 |
|---------|---------|---------|
| **Bash** | 执行shell命令 | 运行测试、git操作、包管理 |
| **Read** | 读取文件内容 | 代码审查、配置解析 |
| **Edit** | 编辑文件内容 | 代码修改、配置更新 |
| **Write** | 创建新文件 | 生成代码、文档创建 |
| **Glob** | 文件模式匹配 | 查找文件、代码导航 |
| **Grep** | 内容搜索 | 代码搜索、模式匹配 |
| **TaskCreate** | 创建任务 | 任务管理 |
| **TaskUpdate** | 更新任务状态 | 进度跟踪 |
| **WebSearch** | 网页搜索 | 信息检索 |

### 1.2 CLI调用方式

**命令行基本调用**：
```bash
# 标准调用
claude "帮我实现用户登录功能"

# 带参数调用
claude --model glm-4.7 \
       --output-format json \
       --allowed-tools "Write,Read,Edit,Bash(git *)" \
       "实现用户认证模块"

# 会话连续性
claude --continue "继续上次的任务"
```

**Python subprocess调用**：
```python
import subprocess
import json

def call_claude(prompt, model="glm-4.7", output_format="json"):
    """调用Claude Code CLI"""
    cmd = [
        "claude",
        "--model", model,
        "--output-format", output_format,
        prompt
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    if result.returncode == 0:
        if output_format == "json":
            return json.loads(result.stdout)
        return result.stdout
    else:
        raise Exception(f"Claude调用失败: {result.stderr}")

# 使用示例
response = call_claude("分析当前项目结构")
print(response['result'])
```

**asyncio异步调用**：
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def call_claude_async(prompt, executor=None):
    """异步调用Claude Code"""
    loop = asyncio.get_running_loop()
    if executor is None:
        executor = ThreadPoolExecutor(max_workers=4)

    cmd = ["claude", "--output-format", "json", prompt]

    def run_command():
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout) if result.returncode == 0 else None

    return await loop.run_in_executor(executor, run_command)

# 并发调用多个Agent
async def run_parallel_agents():
    executor = ThreadPoolExecutor(max_workers=4)

    tasks = [
        call_claude_async("设计数据库架构", executor),
        call_claude_async("设计API接口", executor),
        call_claude_async("设计前端组件", executor)
    ]

    results = await asyncio.gather(*tasks)
    return results

# 运行
results = asyncio.run(run_parallel_agents())
```

### 1.3 工具权限控制

```bash
# 严格限制工具权限
claude --allowed-tools "Read,Write" "只读任务"

# 允许特定命令模式
claude --allowed-tools "Write,Read,Edit,Bash(git *),Bash(npm install)" "开发任务"

# 完全权限（生产环境慎用）
claude --dangerously-skip-permissions "完全访问"
```

---

## 2. 并行运行多个Claude Code实例

### 2.1 方案概述

| 方案 | 实现方式 | 优点 | 缺点 | 适用场景 |
|------|---------|------|------|---------|
| **多进程** | subprocess + multiprocessing | 完全隔离，崩溃不影响其他 | 资源占用高 | 独立任务 |
| **异步IO** | asyncio + ThreadPoolExecutor | 资源效率高 | 共享状态需同步 | IO密集型 |
| **线程池** | ThreadPoolExecutor | 简单易用 | GIL限制CPU任务 | 混合任务 |
| **消息队列** | Redis/RabbitMQ | 可扩展，解耦 | 架构复杂 | 大规模系统 |

### 2.2 多进程方案

**基于subprocess的多进程管理器**：
```python
import subprocess
import threading
import queue
from typing import List, Dict, Any
import time

class ClaudeAgentProcess:
    """Claude Code Agent进程封装"""

    def __init__(self, agent_id: str, role: str, system_prompt: str):
        self.agent_id = agent_id
        self.role = role
        self.system_prompt = system_prompt
        self.process = None
        self.output_queue = queue.Queue()
        self.status = "idle"

    def start(self):
        """启动Agent进程"""
        cmd = [
            "claude",
            "--model", "glm-4.7",
            "--output-format", "json",
            "--continue"
        ]

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.status = "running"

    def send_task(self, task: str):
        """发送任务给Agent"""
        if self.process and self.process.poll() is None:
            full_prompt = f"{self.system_prompt}\n\n任务: {task}"
            try:
                self.process.stdin.write(full_prompt + "\n")
                self.process.stdin.flush()
                return True
            except Exception as e:
                print(f"发送任务失败: {e}")
                return False
        return False

    def read_output(self):
        """读取Agent输出"""
        if self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    return line.strip()
            except Exception as e:
                print(f"读取输出失败: {e}")
        return None

    def stop(self):
        """停止Agent进程"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.status = "stopped"

class MultiAgentOrchestrator:
    """多Agent编排器"""

    def __init__(self):
        self.agents: Dict[str, ClaudeAgentProcess] = {}
        self.task_queue = queue.Queue()
        self.results = {}

    def create_agent(self, agent_id: str, role: str, system_prompt: str):
        """创建新Agent"""
        agent = ClaudeAgentProcess(agent_id, role, system_prompt)
        agent.start()
        self.agents[agent_id] = agent
        print(f"✅ Agent {agent_id} ({role}) 已启动")
        return agent

    def assign_task(self, agent_id: str, task: str):
        """分配任务给指定Agent"""
        if agent_id in self.agents:
            success = self.agents[agent_id].send_task(task)
            if success:
                print(f"📤 任务已分配给 {agent_id}: {task[:50]}...")
            return success
        return False

    def collect_results(self):
        """收集所有Agent的结果"""
        for agent_id, agent in self.agents.items():
            while True:
                output = agent.read_output()
                if output:
                    if agent_id not in self.results:
                        self.results[agent_id] = []
                    self.results[agent_id].append(output)
                else:
                    break
        return self.results

    def shutdown_all(self):
        """关闭所有Agent"""
        for agent_id, agent in self.agents.items():
            agent.stop()
            print(f"🛑 Agent {agent_id} 已停止")

# 使用示例
if __name__ == "__main__":
    orchestrator = MultiAgentOrchestrator()

    # 创建多个不同角色的Agent
    agents_config = [
        ("architect", "架构师", "你是系统架构师，负责整体设计"),
        ("frontend", "前端工程师", "你是前端工程师，负责UI实现"),
        ("backend", "后端工程师", "你是后端工程师，负责API开发"),
        ("tester", "测试工程师", "你是测试工程师，负责质量保证")
    ]

    for agent_id, role, prompt in agents_config:
        orchestrator.create_agent(agent_id, role, prompt)

    # 分配并行任务
    tasks = {
        "architect": "设计用户认证系统的整体架构",
        "frontend": "实现登录页面UI",
        "backend": "实现登录API接口",
        "tester": "编写登录功能的测试用例"
    }

    for agent_id, task in tasks.items():
        orchestrator.assign_task(agent_id, task)

    # 等待并收集结果
    time.sleep(10)
    results = orchestrator.collect_results()

    # 打印结果
    for agent_id, outputs in results.items():
        print(f"\n📊 {agent_id} 的输出:")
        for output in outputs:
            print(f"  {output}")

    # 清理
    orchestrator.shutdown_all()
```

### 2.3 异步并发方案

**基于asyncio的高效并发**：
```python
import asyncio
import subprocess
import json
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

class AsyncClaudeAgent:
    """异步Claude Agent"""

    def __init__(self, agent_id: str, role: str, system_prompt: str):
        self.agent_id = agent_id
        self.role = role
        self.system_prompt = system_prompt
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def process_task(self, task: str) -> Dict[str, Any]:
        """异步处理任务"""
        loop = asyncio.get_running_loop()

        def run_claude():
            cmd = [
                "claude",
                "--model", "glm-4.7",
                "--output-format", "json",
                f"{self.system_prompt}\n\n任务: {task}"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"result": result.stdout}
            else:
                return {"error": result.stderr}

        return await loop.run_in_executor(self.executor, run_claude)

    async def cleanup(self):
        """清理资源"""
        self.executor.shutdown(wait=False)

class AsyncMultiAgentSystem:
    """异步多Agent系统"""

    def __init__(self):
        self.agents: Dict[str, AsyncClaudeAgent] = {}
        self.task_history = []

    def add_agent(self, agent_id: str, role: str, system_prompt: str):
        """添加Agent"""
        agent = AsyncClaudeAgent(agent_id, role, system_prompt)
        self.agents[agent_id] = agent
        return agent

    async def execute_parallel(self, task_assignments: Dict[str, str]) -> Dict[str, Any]:
        """并行执行多个任务"""
        # 创建任务列表
        tasks = []
        agent_ids = []

        for agent_id, task in task_assignments.items():
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                tasks.append(agent.process_task(task))
                agent_ids.append(agent_id)

        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 整理结果
        final_results = {}
        for agent_id, result in zip(agent_ids, results):
            if isinstance(result, Exception):
                final_results[agent_id] = {"error": str(result)}
            else:
                final_results[agent_id] = result

        # 记录历史
        self.task_history.append({
            "timestamp": time.time(),
            "assignments": task_assignments,
            "results": final_results
        })

        return final_results

    async def collaborate(self, main_task: str, rounds: int = 3) -> Dict[str, Any]:
        """多轮协作完成任务"""
        all_results = {}

        for round_num in range(1, rounds + 1):
            print(f"\n🔄 第 {round_num} 轮协作")

            # 每个Agent基于之前的结果提出新想法
            task_assignments = {}
            for agent_id, agent in self.agents.items():
                context = json.dumps(all_results, ensure_ascii=False)
                task = f"基于以下上下文，完成你的职责：\n{context}\n\n当前轮次: {round_num}"
                task_assignments[agent_id] = task

            # 并行执行
            round_results = await self.execute_parallel(task_assignments)
            all_results.update(round_results)

            # 打印本轮结果
            for agent_id, result in round_results.items():
                if "error" not in result:
                    print(f"✅ {agent_id}: {result.get('result', '')[:100]}...")
                else:
                    print(f"❌ {agent_id}: {result['error']}")

        return all_results

    async def cleanup(self):
        """清理所有Agent"""
        for agent in self.agents.values():
            await agent.cleanup()

# 使用示例
async def main():
    system = AsyncMultiAgentSystem()

    # 添加Agent
    system.add_agent("architect", "架构师", "负责系统设计和架构决策")
    system.add_agent("coder", "程序员", "负责代码实现")
    system.add_agent("critic", "评审者", "负责代码审查和问题发现")

    # 方式1：并行执行不同任务
    parallel_tasks = {
        "architect": "设计RESTful API架构",
        "coder": "实现用户登录功能",
        "critic": "审查现有代码质量"
    }

    print("🚀 并行执行任务...")
    results = await system.execute_parallel(parallel_tasks)

    # 方式2：多轮协作
    print("\n🤝 多轮协作模式...")
    collaboration_results = await system.collaborate("实现一个博客系统", rounds=3)

    # 清理
    await system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2.4 基于消息队列的分布式方案

**Redis作为消息代理**：
```python
import redis
import json
import subprocess
import threading
from typing import Dict, Any

class RedisAgent:
    """基于Redis的Agent"""

    def __init__(self, agent_id: str, role: str,
                 redis_host='localhost', redis_port=6379):
        self.agent_id = agent_id
        self.role = role
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.task_channel = f"tasks:{agent_id}"
        self.result_channel = f"results:{agent_id}"
        self.running = False

    def start(self):
        """启动Agent监听"""
        self.running = True
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.task_channel)

        print(f"🎧 Agent {self.agent_id} 开始监听任务...")

        for message in pubsub.listen():
            if not self.running:
                break

            if message['type'] == 'message':
                task_data = json.loads(message['data'])
                self.process_task(task_data)

    def process_task(self, task_data: Dict[str, Any]):
        """处理任务"""
        task = task_data.get('task', '')
        task_id = task_data.get('task_id', '')

        print(f"📥 {self.agent_id} 收到任务: {task}")

        # 调用Claude处理
        result = self.call_claude(task)

        # 发送结果
        response = {
            'task_id': task_id,
            'agent_id': self.agent_id,
            'result': result,
            'timestamp': time.time()
        }

        self.redis.publish(self.result_channel, json.dumps(response))
        print(f"📤 {self.agent_id} 任务完成")

    def call_claude(self, prompt: str) -> str:
        """调用Claude Code"""
        cmd = ["claude", "--model", "glm-4.7", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def stop(self):
        """停止Agent"""
        self.running = False

class MultiAgentCoordinator:
    """多Agent协调器"""

    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.agents = {}
        self.task_counter = 0

    def register_agent(self, agent_id: str, role: str):
        """注册Agent"""
        agent = RedisAgent(agent_id, role)
        thread = threading.Thread(target=agent.start, daemon=True)
        thread.start()
        self.agents[agent_id] = agent
        return agent

    def assign_task(self, agent_id: str, task: str, timeout=30):
        """分配任务给Agent"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"

        task_data = {
            'task_id': task_id,
            'task': task,
            'timestamp': time.time()
        }

        # 发布任务
        self.redis.publish(f"tasks:{agent_id}", json.dumps(task_data))

        # 等待结果
        pubsub = self.redis.pubsub()
        pubsub.subscribe(f"results:{agent_id}")

        start_time = time.time()
        for message in pubsub.listen():
            if message['type'] == 'message':
                result_data = json.loads(message['data'])
                if result_data.get('task_id') == task_id:
                    return result_data.get('result', '')

            if time.time() - start_time > timeout:
                return {"error": "任务超时"}

        return {"error": "未收到结果"}

# 使用示例
if __name__ == "__main__":
    coordinator = MultiAgentCoordinator()

    # 注册多个Agent
    coordinator.register_agent("architect", "架构师")
    coordinator.register_agent("coder", "程序员")
    coordinator.register_agent("tester", "测试员")

    # 分配任务
    result1 = coordinator.assign_task("architect", "设计系统架构")
    result2 = coordinator.assign_task("coder", "实现登录功能")
    result3 = coordinator.assign_task("tester", "编写测试用例")

    print(f"架构师结果: {result1}")
    print(f"程序员结果: {result2}")
    print(f"测试员结果: {result3}")
```

---

## 3. Agent间通信机制设计

### 3.1 通信模式

#### 3.1.1 共享文件系统通信

```python
import json
import os
from pathlib import Path
from datetime import datetime
import threading
import time

class FileSystemCommunication:
    """基于文件系统的Agent通信"""

    def __init__(self, comm_dir=".agent_comm"):
        self.comm_dir = Path(comm_dir)
        self.comm_dir.mkdir(exist_ok=True)
        self.message_file = self.comm_dir / "messages.json"
        self.lock_file = self.comm_dir / "lock"
        self._init_message_store()

    def _init_message_store(self):
        """初始化消息存储"""
        if not self.message_file.exists():
            with open(self.message_file, 'w') as f:
                json.dump([], f)

    def _acquire_lock(self, timeout=10):
        """获取文件锁"""
        start = time.time()
        while time.time() - start < timeout:
            try:
                self.lock_file.mkdir(exist_ok=False)
                return True
            except FileExistsError:
                time.sleep(0.1)
        return False

    def _release_lock(self):
        """释放文件锁"""
        if self.lock_file.exists():
            self.lock_file.rmdir()

    def send_message(self, sender: str, receiver: str, content: str, msg_type: str = "task"):
        """发送消息"""
        if not self._acquire_lock():
            raise Exception("无法获取文件锁")

        try:
            with open(self.message_file, 'r') as f:
                messages = json.load(f)

            message = {
                'id': f"{sender}_{int(time.time()*1000)}",
                'sender': sender,
                'receiver': receiver,
                'content': content,
                'type': msg_type,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }

            messages.append(message)

            with open(self.message_file, 'w') as f:
                json.dump(messages, f, indent=2)

        finally:
            self._release_lock()

    def receive_messages(self, agent_id: str, unread_only=True) -> list:
        """接收消息"""
        if not self._acquire_lock():
            return []

        try:
            with open(self.message_file, 'r') as f:
                messages = json.load(f)

            # 过滤消息
            filtered = []
            for msg in messages:
                if msg['receiver'] == agent_id:
                    if not unread_only or msg['status'] == 'pending':
                        filtered.append(msg)

            # 标记为已读
            if unread_only:
                for msg in messages:
                    if msg['receiver'] == agent_id and msg['status'] == 'pending':
                        msg['status'] = 'read'

                with open(self.message_file, 'w') as f:
                    json.dump(messages, f, indent=2)

            return filtered

        finally:
            self._release_lock()

    def broadcast(self, sender: str, content: str, exclude: list = None):
        """广播消息"""
        if exclude is None:
            exclude = []

        # 获取所有Agent ID（从消息历史推断）
        with open(self.message_file, 'r') as f:
            messages = json.load(f)

        all_agents = set()
        for msg in messages:
            all_agents.add(msg['sender'])
            all_agents.add(msg['receiver'])

        # 广播
        for agent_id in all_agents:
            if agent_id != sender and agent_id not in exclude:
                self.send_message(sender, agent_id, content, "broadcast")

# 使用示例
class CommunicatingAgent:
    """可通信的Agent"""

    def __init__(self, agent_id: str, role: str, comm_system: FileSystemCommunication):
        self.agent_id = agent_id
        self.role = role
        self.comm = comm_system
        self.running = False

    def start(self):
        """启动Agent"""
        self.running = True
        while self.running:
            # 检查新消息
            messages = self.comm.receive_messages(self.agent_id)

            for msg in messages:
                print(f"📨 {self.agent_id} 收到来自 {msg['sender']} 的消息")
                self.handle_message(msg)

            time.sleep(1)

    def handle_message(self, message: dict):
        """处理消息"""
        content = message['content']
        msg_type = message.get('type', 'task')

        if msg_type == 'task':
            # 处理任务
            result = self.process_task(content)

            # 回复结果
            self.comm.send_message(
                self.agent_id,
                message['sender'],
                json.dumps({'result': result}),
                'result'
            )

        elif msg_type == 'result':
            # 处理结果
            print(f"✅ 收到结果: {content}")

    def process_task(self, task: str) -> str:
        """处理任务（调用Claude）"""
        import subprocess
        cmd = ["claude", f"{self.role}: {task}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def collaborate_with(self, other_agent_id: str, task: str):
        """与其他Agent协作"""
        self.comm.send_message(self.agent_id, other_agent_id, task, 'collaboration')

# 使用示例
if __name__ == "__main__":
    comm = FileSystemCommunication()

    # 创建Agent
    architect = CommunicatingAgent("architect", "架构师", comm)
    coder = CommunicatingAgent("coder", "程序员", comm)
    tester = CommunicatingAgent("tester", "测试员", comm)

    # 启动Agent（实际应该在独立线程）
    import threading
    agents = [architect, coder, tester]
    threads = []

    for agent in agents:
        t = threading.Thread(target=agent.start, daemon=True)
        t.start()
        threads.append(t)

    # 模拟协作
    time.sleep(1)

    # 架构师发起设计
    architect.collaborate_with("coder", "设计用户认证API")
    architect.collaborate_with("tester", "准备认证API的测试计划")

    # 等待
    time.sleep(5)
```

#### 3.1.2 共享内存通信

```python
import multiprocessing
from multiprocessing import shared_memory, Value, Array
import json
import time

class SharedMemoryCommunication:
    """基于共享内存的通信"""

    def __init__(self, buffer_size=4096):
        self.buffer_size = buffer_size
        # 创建共享内存
        self.shm = shared_memory.SharedMemory(create=True, size=buffer_size)
        self.message_count = Value('i', 0)

    def write_message(self, message: dict):
        """写入消息到共享内存"""
        with self.message_count.get_lock():
            msg_str = json.dumps(message)
            msg_bytes = msg_str.encode('utf-8')

            if len(msg_bytes) > self.buffer_size:
                raise ValueError("消息太大")

            # 写入
            self.shm.buf[:len(msg_bytes)] = msg_bytes
            self.message_count.value += 1

            return self.message_count.value

    def read_message(self) -> dict:
        """读取消息"""
        with self.message_count.get_lock():
            if self.message_count.value > 0:
                # 读取
                msg_bytes = bytes(self.shm.buf).rstrip(b'\x00')
                msg_str = msg_bytes.decode('utf-8')
                return json.loads(msg_str)
        return None

    def cleanup(self):
        """清理资源"""
        self.shm.close()
        self.shm.unlink()
```

#### 3.1.3 管道通信

```python
from multiprocessing import Process, Pipe

def agent_process(conn, agent_id, role):
    """Agent进程"""
    conn.send(f"{agent_id} ({role}) 已启动")

    while True:
        try:
            message = conn.recv()
            if message == "STOP":
                break

            # 处理消息
            result = f"{agent_id} 处理: {message}"
            conn.send(result)

        except EOFError:
            break

    conn.close()

class PipelineCommunication:
    """基于管道的通信"""

    def __init__(self):
        self.agents = {}

    def create_agent(self, agent_id: str, role: str):
        """创建Agent进程"""
        parent_conn, child_conn = Pipe()

        process = Process(target=agent_process, args=(child_conn, agent_id, role))
        process.start()

        self.agents[agent_id] = {
            'process': process,
            'connection': parent_conn
        }

        # 等待启动确认
        msg = parent_conn.recv()
        print(f"✅ {msg}")

        return parent_conn

    def send(self, agent_id: str, message: str):
        """发送消息"""
        if agent_id in self.agents:
            self.agents[agent_id]['connection'].send(message)

    def receive(self, agent_id: str, timeout=5):
        """接收消息"""
        if agent_id in self.agents:
            conn = self.agents[agent_id]['connection']
            if conn.poll(timeout):
                return conn.recv()
        return None

    def stop_all(self):
        """停止所有Agent"""
        for agent_id, agent_info in self.agents.items():
            agent_info['connection'].send("STOP")
            agent_info['process'].join()

# 使用示例
if __name__ == "__main__":
    comm = PipelineCommunication()

    # 创建Agent
    comm.create_agent("architect", "架构师")
    comm.create_agent("coder", "程序员")
    comm.create_agent("tester", "测试员")

    # 发送任务
    comm.send("coder", "实现用户登录")
    comm.send("architect", "设计系统架构")

    # 接收结果
    time.sleep(1)
    print(f"Coder: {comm.receive('coder')}")
    print(f"Architect: {comm.receive('architect')}")

    # 清理
    comm.stop_all()
```

### 3.2 同步机制

#### 3.2.1 屏障同步（Barrier）

```python
from multiprocessing import Barrier, Process
import time

def agent_with_barrier(agent_id, barrier, tasks):
    """带屏障同步的Agent"""
    print(f"[{agent_id}] 开始工作")

    # 执行任务
    result = f"{agent_id} 的结果"

    # 等待其他Agent
    print(f"[{agent_id}] 等待其他Agent...")
    barrier.wait()

    # 所有Agent都到达后继续
    print(f"[{agent_id}] 继续协作！")

    return result

def barrier_example():
    """屏障同步示例"""
    num_agents = 3
    barrier = Barrier(num_agents)

    processes = []
    for i in range(num_agents):
        p = Process(target=agent_with_barrier, args=(f"Agent-{i}", barrier, []))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
```

#### 3.2.2 事件同步（Event）

```python
from multiprocessing import Event, Process

def producer(agent_id, event):
    """生产者Agent"""
    print(f"[{agent_id}] 正在处理...")
    time.sleep(2)
    print(f"[{agent_id}] 处理完成！")
    event.set()  # 触发事件

def consumer(agent_id, event):
    """消费者Agent"""
    print(f"[{agent_id}] 等待生产者完成...")
    event.wait()  # 等待事件
    print(f"[{agent_id}] 收到通知，开始后续工作！")

def event_example():
    """事件同步示例"""
    event = Event()

    producer_p = Process(target=producer, args=("Producer", event))
    consumer_p = Process(target=consumer, args=("Consumer", event))

    consumer_p.start()
    producer_p.start()

    producer_p.join()
    consumer_p.join()
```

### 3.3 消息序列化协议

```python
import json
from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum

class MessageType(Enum):
    """消息类型枚举"""
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Agent消息协议"""
    id: str
    sender: str
    receiver: str
    type: MessageType
    content: str
    timestamp: float
    reply_to: Optional[str] = None
    metadata: Optional[dict] = None

    def to_json(self) -> str:
        """序列化为JSON"""
        data = asdict(self)
        data['type'] = self.type.value
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'AgentMessage':
        """从JSON反序列化"""
        data = json.loads(json_str)
        data['type'] = MessageType(data['type'])
        return cls(**data)

    def to_dict(self) -> dict:
        """转换为字典"""
        data = asdict(self)
        data['type'] = self.type.value
        return data

# 使用示例
if __name__ == "__main__":
    # 创建消息
    msg = AgentMessage(
        id="msg_001",
        sender="architect",
        receiver="coder",
        type=MessageType.TASK,
        content="实现用户认证API",
        timestamp=time.time()
    )

    # 序列化
    json_str = msg.to_json()
    print(f"序列化: {json_str}")

    # 反序列化
    restored_msg = AgentMessage.from_json(json_str)
    print(f"反序列化: {restored_msg}")
```

---

## 4. 文件操作工具使用示例

### 4.1 Read工具使用

```python
def read_file_example():
    """使用Read工具读取文件"""

    # 方式1：通过Bash调用Claude Code
    import subprocess

    prompt = """
    请使用Read工具读取以下文件并总结内容：
    - README.md
    - .janus/config.json
    """

    result = subprocess.run(
        ["claude", prompt],
        capture_output=True,
        text=True
    )

    print(result.stdout)

# Python直接读取（供Agent内部使用）
def read_file_safely(file_path: str) -> str:
    """安全读取文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"错误：文件 {file_path} 不存在"
    except Exception as e:
        return f"错误：{str(e)}"

def read_multiple_files(file_paths: list) -> dict:
    """批量读取文件"""
    results = {}
    for path in file_paths:
        results[path] = read_file_safely(path)
    return results
```

### 4.2 Write工具使用

```python
def write_file_example():
    """使用Write工具创建文件"""

    prompt = """
    请使用Write工具创建一个Python脚本：
    文件名: utils.py
    内容: 包含一个计算斐波那契数列的函数
    """

    import subprocess
    result = subprocess.run(["claude", prompt], capture_output=True, text=True)
    print(result.stdout)

# Python直接写入
def write_file_safely(file_path: str, content: str) -> bool:
    """安全写入文件"""
    try:
        # 确保目录存在
        import os
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"写入失败: {e}")
        return False
```

### 4.3 Edit工具使用

```python
def edit_file_example():
    """使用Edit工具编辑文件"""

    prompt = """
    请使用Edit工具修改 config.py 文件：
    将 DEBUG = False 改为 DEBUG = True
    """

    import subprocess
    result = subprocess.run(["claude", prompt], capture_output=True, text=True)
    print(result.stdout)

# Python直接编辑
def edit_file_section(file_path: str, old_text: str, new_text: str) -> bool:
    """编辑文件的特定部分"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_text not in content:
            print(f"警告：未找到要替换的文本")
            return False

        new_content = content.replace(old_text, new_text)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"编辑失败: {e}")
        return False
```

### 4.4 完整文件操作示例

```python
class FileOperationsAgent:
    """文件操作Agent"""

    def __init__(self, agent_id: str, work_dir: str):
        self.agent_id = agent_id
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(exist_ok=True)

    def read_project_structure(self) -> dict:
        """读取项目结构"""
        structure = {}

        for item in self.work_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(self.work_dir)
                structure[str(relative_path)] = {
                    'size': item.stat().st_size,
                    'modified': item.stat().st_mtime
                }

        return structure

    def search_files(self, pattern: str) -> list:
        """搜索文件"""
        return list(self.work_dir.rglob(pattern))

    def search_content(self, keyword: str) -> list:
        """搜索文件内容"""
        results = []

        for file_path in self.work_dir.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if keyword in line:
                            results.append({
                                'file': str(file_path),
                                'line': line_num,
                                'content': line.strip()
                            })
            except Exception:
                continue

        return results

    def batch_create_files(self, files: dict) -> dict:
        """批量创建文件"""
        results = {}

        for file_path, content in files.items():
            full_path = self.work_dir / file_path
            success = write_file_safely(str(full_path), content)
            results[file_path] = "成功" if success else "失败"

        return results

# 使用示例
if __name__ == "__main__":
    agent = FileOperationsAgent("file_agent", "./test_project")

    # 读取结构
    structure = agent.read_project_structure()
    print(f"项目结构: {structure}")

    # 搜索Python文件
    py_files = agent.search_files("*.py")
    print(f"Python文件: {py_files}")

    # 搜索内容
    results = agent.search_content("import")
    print(f"搜索结果: {len(results)} 处")

    # 批量创建
    files = {
        "utils/helpers.py": "# Helper functions\ndef helper1():\n    pass",
        "config/settings.py": "# Settings\nDEBUG = True"
    }
    create_results = agent.batch_create_files(files)
    print(f"创建结果: {create_results}")
```

---

## 5. 进程管理和资源控制

### 5.1 进程池管理

```python
from multiprocessing import Pool, Process, Queue
import time
import psutil
import os

class AgentProcessManager:
    """Agent进程管理器"""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.process_pool = Pool(processes=max_workers)
        self.active_processes = {}
        self.resource_monitor = ResourceMonitor()

    def spawn_agent(self, agent_id: str, role: str, task: str):
        """生成Agent进程"""
        process = Process(
            target=run_agent_task,
            args=(agent_id, role, task)
        )
        process.start()

        self.active_processes[agent_id] = {
            'process': process,
            'pid': process.pid,
            'role': role,
            'start_time': time.time()
        }

        print(f"✅ Agent {agent_id} (PID: {process.pid}) 已启动")
        return process

    def monitor_resources(self):
        """监控资源使用"""
        stats = {}

        for agent_id, info in self.active_processes.items():
            if info['process'].is_alive():
                pid = info['pid']
                proc = psutil.Process(pid)

                stats[agent_id] = {
                    'cpu_percent': proc.cpu_percent(),
                    'memory_mb': proc.memory_info().rss / 1024 / 1024,
                    'status': proc.status(),
                    'threads': proc.num_threads()
                }

        return stats

    def terminate_agent(self, agent_id: str):
        """终止Agent"""
        if agent_id in self.active_processes:
            process = self.active_processes[agent_id]['process']
            process.terminate()
            process.join(timeout=5)

            if process.is_alive():
                process.kill()

            del self.active_processes[agent_id]
            print(f"🛑 Agent {agent_id} 已终止")

    def cleanup_all(self):
        """清理所有Agent"""
        for agent_id in list(self.active_processes.keys()):
            self.terminate_agent(agent_id)

        self.process_pool.close()
        self.process_pool.join()

def run_agent_task(agent_id: str, role: str, task: str):
    """Agent任务执行函数"""
    try:
        # 调用Claude Code
        import subprocess
        prompt = f"你是{role}。任务: {task}"
        result = subprocess.run(
            ["claude", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        print(f"[{agent_id}] 任务完成")
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"[{agent_id}] 任务超时")
        return None
    except Exception as e:
        print(f"[{agent_id}] 错误: {e}")
        return None

class ResourceMonitor:
    """资源监控器"""

    def __init__(self, warning_threshold=80, critical_threshold=90):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def check_system_resources(self) -> dict:
        """检查系统资源"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        status = {
            'cpu': {
                'percent': cpu_percent,
                'status': self._get_status(cpu_percent)
            },
            'memory': {
                'percent': memory.percent,
                'available_mb': memory.available / 1024 / 1024,
                'status': self._get_status(memory.percent)
            },
            'disk': {
                'percent': disk.percent,
                'free_gb': disk.free / 1024 / 1024 / 1024,
                'status': self._get_status(disk.percent)
            }
        }

        return status

    def _get_status(self, percent: float) -> str:
        """获取状态"""
        if percent >= self.critical_threshold:
            return "critical"
        elif percent >= self.warning_threshold:
            return "warning"
        else:
            return "ok"

    def should_throttle(self) -> bool:
        """判断是否需要限流"""
        status = self.check_system_resources()

        return any([
            status['cpu']['status'] == 'critical',
            status['memory']['status'] == 'critical'
        ])

# 使用示例
if __name__ == "__main__":
    manager = AgentProcessManager(max_workers=4)
    monitor = ResourceMonitor()

    # 生成多个Agent
    tasks = [
        ("agent1", "架构师", "设计系统架构"),
        ("agent2", "程序员", "实现登录功能"),
        ("agent3", "测试员", "编写测试用例"),
        ("agent4", "文档员", "编写技术文档")
    ]

    for agent_id, role, task in tasks:
        manager.spawn_agent(agent_id, role, task)

    # 监控资源
    for _ in range(10):
        time.sleep(2)

        # 检查系统资源
        sys_status = monitor.check_system_resources()
        print(f"\n系统状态: CPU {sys_status['cpu']['percent']}%, "
              f"内存 {sys_status['memory']['percent']}%")

        # 检查Agent资源
        agent_stats = manager.monitor_resources()
        for agent_id, stats in agent_stats.items():
            print(f"  {agent_id}: CPU {stats['cpu_percent']}%, "
                  f"内存 {stats['memory_mb']:.1f}MB")

        # 资源紧张时终止
        if monitor.should_throttle():
            print("⚠️ 资源紧张，限制新任务")
            break

    # 清理
    manager.cleanup_all()
```

### 5.2 任务队列管理

```python
from queue import Queue, Empty
import threading
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class AgentTask:
    """Agent任务"""
    id: str
    agent_type: str
    task_data: dict
    priority: int = 0
    callback: Optional[Callable] = None

class TaskQueue:
    """优先级任务队列"""

    def __init__(self, max_size=100):
        self.queue = Queue(maxsize=max_size)
        self.lock = threading.Lock()
        self.task_count = 0

    def add_task(self, task: AgentTask):
        """添加任务"""
        with self.lock:
            self.task_count += 1
            if not task.id:
                task.id = f"task_{self.task_count}"

            self.queue.put(task)
            print(f"📥 任务 {task.id} 已加入队列 (优先级: {task.priority})")

    def get_task(self, timeout=1) -> Optional[AgentTask]:
        """获取任务"""
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None

    def task_done(self):
        """标记任务完成"""
        self.queue.task_done()

    def size(self) -> int:
        """队列大小"""
        return self.queue.qsize()

class PriorityTaskQueue:
    """优先级任务队列（使用堆）"""

    def __init__(self):
        import heapq
        self.heap = []
        self.lock = threading.Lock()
        self.counter = 0

    def add_task(self, task: AgentTask):
        """添加任务（按优先级）"""
        with self.lock:
            self.counter += 1
            # 使用（优先级，计数器，任务）作为元组
            # 优先级越小越先执行
            heapq.heappush(self.heap, (task.priority, self.counter, task))

    def get_task(self) -> Optional[AgentTask]:
        """获取最高优先级任务"""
        with self.lock:
            if self.heap:
                _, _, task = heapq.heappop(self.heap)
                return task
        return None

    def peek(self) -> Optional[AgentTask]:
        """查看最高优先级任务（不移除）"""
        with self.lock:
            if self.heap:
                _, _, task = self.heap[0]
                return task
        return None

class WorkerThread(threading.Thread):
    """工作线程"""

    def __init__(self, worker_id: str, task_queue: TaskQueue):
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.running = False

    def run(self):
        """运行工作线程"""
        self.running = True
        print(f"🔄 Worker {self.worker_id} 启动")

        while self.running:
            task = self.task_queue.get_task(timeout=1)

            if task:
                print(f"⚙️ Worker {self.worker_id} 处理任务 {task.id}")
                self.process_task(task)
                self.task_queue.task_done()

    def process_task(self, task: AgentTask):
        """处理任务"""
        try:
            # 执行任务
            result = self.execute_task(task)

            # 回调
            if task.callback:
                task.callback(result)
        except Exception as e:
            print(f"❌ 任务 {task.id} 执行失败: {e}")

    def execute_task(self, task: AgentTask) -> dict:
        """执行具体任务"""
        import subprocess

        prompt = f"你是{task.agent_type}。任务: {task.task_data}"

        result = subprocess.run(
            ["claude", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            'task_id': task.id,
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }

    def stop(self):
        """停止工作线程"""
        self.running = False

class ThreadPool:
    """线程池"""

    def __init__(self, num_workers: int = 4):
        self.task_queue = TaskQueue()
        self.workers = []
        self.num_workers = num_workers

    def start(self):
        """启动线程池"""
        for i in range(self.num_workers):
            worker = WorkerThread(f"worker_{i}", self.task_queue)
            worker.start()
            self.workers.append(worker)

        print(f"✅ 线程池已启动 ({self.num_workers} 个Worker)")

    def submit_task(self, task: AgentTask):
        """提交任务"""
        self.task_queue.add_task(task)

    def shutdown(self):
        """关闭线程池"""
        for worker in self.workers:
            worker.stop()

        for worker in self.workers:
            worker.join()

        print("🛑 线程池已关闭")

# 使用示例
if __name__ == "__main__":
    pool = ThreadPool(num_workers=3)
    pool.start()

    # 提交任务
    tasks = [
        AgentTask("task1", "架构师", {"task": "设计API"}, priority=1),
        AgentTask("task2", "程序员", {"task": "实现登录"}, priority=2),
        AgentTask("task3", "测试员", {"task": "编写测试"}, priority=3),
    ]

    for task in tasks:
        pool.submit_task(task)

    # 等待完成
    time.sleep(10)

    # 关闭
    pool.shutdown()
```

### 5.3 资源限制和配额

```python
import resource
import psutil

class ResourceLimiter:
    """资源限制器"""

    def __init__(self,
                 max_memory_mb: int = 1024,
                 max_cpu_time: int = 60,
                 max_files: int = 100):
        self.max_memory_mb = max_memory_mb
        self.max_cpu_time = max_cpu_time
        self.max_files = max_files

    def set_limits(self):
        """设置资源限制"""
        try:
            # 内存限制（字节）
            memory_limit = self.max_memory_mb * 1024 * 1024
            resource.setrlimit(
                resource.RLIMIT_AS,
                (memory_limit, memory_limit)
            )

            # CPU时间限制（秒）
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (self.max_cpu_time, self.max_cpu_time)
            )

            # 文件描述符限制
            resource.setrlimit(
                resource.RLIMIT_NOFILE,
                (self.max_files, self.max_files)
            )

            print(f"✅ 资源限制已设置: "
                  f"内存 {self.max_memory_mb}MB, "
                  f"CPU {self.max_cpu_time}s, "
                  f"文件 {self.max_files}")

        except Exception as e:
            print(f"⚠️ 无法设置资源限制: {e}")

    @staticmethod
    def get_current_usage() -> dict:
        """获取当前资源使用情况"""
        process = psutil.Process()

        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(),
            'open_files': len(process.open_files()),
            'threads': process.num_threads(),
            'connections': len(process.connections())
        }

class QuotaManager:
    """配额管理器"""

    def __init__(self, daily_api_call_limit: int = 1000):
        self.daily_api_call_limit = daily_api_call_limit
        self.api_calls_today = 0
        self.call_history = []

    def can_make_call(self) -> bool:
        """检查是否可以调用API"""
        self._reset_if_new_day()
        return self.api_calls_today < self.daily_api_call_limit

    def record_call(self, cost: float = 0):
        """记录API调用"""
        self.api_calls_today += 1

        self.call_history.append({
            'timestamp': time.time(),
            'cost': cost
        })

    def get_remaining_calls(self) -> int:
        """获取剩余调用次数"""
        self._reset_if_new_day()
        return max(0, self.daily_api_call_limit - self.api_calls_today)

    def _reset_if_new_day(self):
        """新的一天时重置"""
        if self.call_history:
            last_call_time = self.call_history[-1]['timestamp']
            if time.time() - last_call_time > 86400:  # 24小时
                self.api_calls_today = 0
                self.call_history = []
```

---

## 6. 完整多Agent协作架构

### 6.1 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                  多Agent协作系统架构                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  协调层 (Coordinator)                                    │
│  - 任务分配                                              │
│  - 进程管理                                              │
│  - 资源监控                                              │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
    ┌────────▼────────┐          ┌───────▼──────────┐
    │  通信总线        │          │   存储层          │
    │  - 消息队列      │          │   - 文件系统      │
    │  - 共享内存      │          │   - 数据库        │
    │  - 管道          │          │   - 缓存          │
    └────────┬────────┘          └──────────────────┘
             │
    ┌────────▼──────────────────────────────────────┐
    │              Agent Pool                        │
    ├──────────────┬──────────────┬─────────────────┤
    │  Brain Agent │  Worker Agent │ Monitor Agent   │
    │  - 规划任务  │  - 执行代码  │  - 监控状态     │
    │  - 理解需求  │  - 文件操作  │  - 资源管理     │
    ├──────────────┼──────────────┼─────────────────┤
    │ Architect    │  Coder       │  Tester         │
    │  - 架构设计  │  - 代码实现  │  - 测试验证     │
    ├──────────────┼──────────────┼─────────────────┤
    │ Optimizer    │  Critic      │  Reviewer       │
    │  - 性能优化  │  - 代码审查  │  - 质量检查     │
    └──────────────┴──────────────┴─────────────────┘
             │
    ┌────────▼──────────────────────────────────────┐
    │           工具层 (Tool Layer)                  │
    ├──────────┬──────────┬──────────┬──────────────┤
    │   Bash   │   Read   │  Write  │     Edit      │
    │   Glob   │   Grep   │  Task   │ Async Execute │
    └──────────┴──────────┴──────────┴──────────────┘
             │
    ┌────────▼──────────────────────────────────────┐
    │        资源层 (Resource Layer)                 │
    ├──────────┬──────────┬──────────┬──────────────┤
    │ Process  │  Thread  │ Memory   │    IO        │
    │ Pool     │  Pool    │  Cache   │  Management  │
    └──────────┴──────────┴──────────┴──────────────┘
```

### 6.2 协作流程

```python
class CollaborativeAgentSystem:
    """协作Agent系统"""

    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.communication = FileSystemCommunication()
        self.resource_manager = ResourceManager()
        self.task_queue = PriorityTaskQueue()

    def setup_agents(self):
        """设置Agent"""
        # Brain Agent - 负责任务规划
        self.coordinator.create_agent(
            "brain",
            "Brain",
            "你是任务规划专家，负责理解需求、规划任务、协调其他Agent"
        )

        # Worker Agents - 负责执行
        roles = [
            ("architect", "架构师", "负责系统设计和架构"),
            ("coder", "程序员", "负责代码实现"),
            ("tester", "测试员", "负责测试和质量保证")
        ]

        for agent_id, role, desc in roles:
            self.coordinator.create_agent(agent_id, role, desc)

        # Monitor Agent - 负责监控
        self.coordinator.create_agent(
            "monitor",
            "Monitor",
            "负责监控系统状态、资源使用、任务进度"
        )

    def execute_workflow(self, user_request: str):
        """执行工作流"""

        # Phase 1: 理解需求（Brain）
        print("🧠 Phase 1: 理解需求")
        brain_task = AgentTask(
            "brain_001",
            "Brain",
            {"request": user_request},
            priority=1
        )
        understanding = self.coordinator.execute_task(brain_task)

        # Phase 2: 任务分解（Brain + Architects）
        print("📋 Phase 2: 任务分解")
        tasks = self.decompose_tasks(understanding)

        # Phase 3: 并行执行（Workers）
        print("⚙️ Phase 3: 并行执行")
        execution_results = self.execute_parallel(tasks)

        # Phase 4: 质量检查（Tester + Critic）
        print("✅ Phase 4: 质量检查")
        quality_report = self.quality_check(execution_results)

        # Phase 5: 最终整合（Brain）
        print("🎯 Phase 5: 最终整合")
        final_result = self.integrate_results(quality_report)

        return final_result

    def decompose_tasks(self, understanding: dict) -> list:
        """分解任务"""
        # 使用Brain和Architect协作分解任务
        tasks = []

        # 架构任务
        tasks.append(AgentTask(
            "arch_task",
            "Architect",
            understanding,
            priority=1
        ))

        # 编码任务（依赖架构）
        tasks.append(AgentTask(
            "code_task",
            "Coder",
            {"depends_on": "arch_task"},
            priority=2
        ))

        # 测试任务（依赖编码）
        tasks.append(AgentTask(
            "test_task",
            "Tester",
            {"depends_on": "code_task"},
            priority=3
        ))

        return tasks

    def execute_parallel(self, tasks: list) -> dict:
        """并行执行任务"""
        return self.coordinator.execute_parallel(tasks)

    def quality_check(self, results: dict) -> dict:
        """质量检查"""
        # 使用Tester和Critic进行质量检查
        report = {
            'passed': [],
            'failed': [],
            'suggestions': []
        }

        for task_id, result in results.items():
            # 调用Tester检查
            test_task = AgentTask(
                f"test_{task_id}",
                "Tester",
                {"result": result}
            )
            test_result = self.coordinator.execute_task(test_task)

            if test_result.get('success'):
                report['passed'].append(task_id)
            else:
                report['failed'].append(task_id)
                report['suggestions'].append(test_result.get('suggestion'))

        return report

    def integrate_results(self, report: dict) -> dict:
        """整合结果"""
        # 使用Brain整合所有结果
        integration_task = AgentTask(
            "integrate",
            "Brain",
            {"quality_report": report}
        )

        return self.coordinator.execute_task(integration_task)
```

---

## 7. 实践代码示例

### 7.1 完整的多Agent协作系统

```python
#!/usr/bin/env python3
"""
多Agent协作系统 - 完整实现
支持并发执行、通信、同步、资源管理
"""

import asyncio
import subprocess
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import threading
import queue

# ==================== 消息协议 ====================

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    STATUS = "status"

@dataclass
class Message:
    id: str
    sender: str
    receiver: str
    type: MessageType
    content: Any
    timestamp: float

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'type': self.type.value,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(
            id=data['id'],
            sender=data['sender'],
            receiver=data['receiver'],
            type=MessageType(data['type']),
            content=data['content'],
            timestamp=data['timestamp']
        )

# ==================== Agent实现 ====================

class ClaudeAgent:
    """Claude Code Agent"""

    def __init__(self, agent_id: str, role: str, system_prompt: str):
        self.agent_id = agent_id
        self.role = role
        self.system_prompt = system_prompt
        self.message_queue = queue.Queue()
        self.running = False
        self.thread = None

    def start(self):
        """启动Agent"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"✅ Agent {self.agent_id} ({self.role}) 已启动")

    def _run(self):
        """Agent主循环"""
        while self.running:
            try:
                # 检查消息
                message = self.message_queue.get(timeout=1)
                self._handle_message(message)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Agent {self.agent_id} 错误: {e}")

    def _handle_message(self, message: Message):
        """处理消息"""
        if message.type == MessageType.TASK:
            result = self._execute_task(message.content)
            # 这里应该发送结果给发送者
            print(f"📤 Agent {self.agent_id} 完成任务")

    def _execute_task(self, task: str) -> str:
        """执行任务"""
        full_prompt = f"{self.system_prompt}\n\n任务: {task}"

        try:
            result = subprocess.run(
                ["claude", "--model", "glm-4.7", full_prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return result.stdout
            else:
                return f"错误: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "错误: 任务超时"
        except Exception as e:
            return f"错误: {str(e)}"

    def send_message(self, message: Message):
        """发送消息给Agent"""
        self.message_queue.put(message)

    def stop(self):
        """停止Agent"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

# ==================== 协调器实现 ====================

class AgentCoordinator:
    """Agent协调器"""

    def __init__(self):
        self.agents: Dict[str, ClaudeAgent] = {}
        self.message_bus = queue.Queue()
        self.running = False
        self.monitor_thread = None

    def create_agent(self, agent_id: str, role: str, system_prompt: str):
        """创建Agent"""
        agent = ClaudeAgent(agent_id, role, system_prompt)
        self.agents[agent_id] = agent
        agent.start()
        return agent

    def broadcast_task(self, task: str, sender: str = "coordinator"):
        """广播任务给所有Agent"""
        message = Message(
            id=f"msg_{int(time.time()*1000)}",
            sender=sender,
            receiver="all",
            type=MessageType.TASK,
            content=task,
            timestamp=time.time()
        )

        for agent_id, agent in self.agents.items():
            if agent_id != sender:
                agent.send_message(message)

    def assign_task(self, agent_id: str, task: str, sender: str = "coordinator"):
        """分配任务给指定Agent"""
        if agent_id not in self.agents:
            print(f"❌ Agent {agent_id} 不存在")
            return False

        message = Message(
            id=f"msg_{int(time.time()*1000)}",
            sender=sender,
            receiver=agent_id,
            type=MessageType.TASK,
            content=task,
            timestamp=time.time()
        )

        self.agents[agent_id].send_message(message)
        return True

    def execute_parallel(self, task_assignments: Dict[str, str]) -> Dict[str, Any]:
        """并行执行多个任务"""
        # 分配任务
        for agent_id, task in task_assignments.items():
            self.assign_task(agent_id, task)

        # 等待结果（简化版）
        time.sleep(10)

        # 返回结果（实际应该从消息总线收集）
        results = {}
        for agent_id in task_assignments.keys():
            results[agent_id] = {"status": "completed"}

        return results

    def shutdown(self):
        """关闭协调器"""
        self.running = False
        for agent in self.agents.values():
            agent.stop()

# ==================== 资源管理器 ====================

class ResourceManager:
    """资源管理器"""

    def __init__(self, max_memory_mb: int = 2048, max_workers: int = 4):
        self.max_memory_mb = max_memory_mb
        self.max_workers = max_workers
        self.active_tasks = {}

    def can_spawn_task(self) -> bool:
        """检查是否可以生成新任务"""
        return len(self.active_tasks) < self.max_workers

    def register_task(self, task_id: str):
        """注册任务"""
        if self.can_spawn_task():
            self.active_tasks[task_id] = time.time()
            return True
        return False

    def unregister_task(self, task_id: str):
        """注销任务"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]

    def get_status(self) -> dict:
        """获取状态"""
        return {
            'active_tasks': len(self.active_tasks),
            'max_workers': self.max_workers,
            'utilization': len(self.active_tasks) / self.max_workers * 100
        }

# ==================== 工作流引擎 ====================

class WorkflowEngine:
    """工作流引擎"""

    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.resource_manager = ResourceManager()
        self.workflows = {}

    def setup_brain_workflow(self):
        """设置Brain工作流"""
        # 创建Brain Agent
        self.coordinator.create_agent(
            "brain",
            "Brain",
            """你是任务规划专家。
职责：
1. 理解用户需求
2. 分解任务
3. 协调其他Agent
4. 整合结果
"""
        )

        # 创建Worker Agents
        workers = [
            ("architect", "架构师", "负责系统设计和架构"),
            ("coder", "程序员", "负责代码实现"),
            ("tester", "测试员", "负责测试和质量保证")
        ]

        for agent_id, role, desc in workers:
            self.coordinator.create_agent(
                agent_id,
                role,
                f"你是{role}。\n职责：{desc}"
            )

        # 创建Monitor Agent
        self.coordinator.create_agent(
            "monitor",
            "Monitor",
            "负责监控系统状态和资源使用"
        )

    def execute_brain_workflow(self, user_request: str) -> dict:
        """执行Brain工作流"""
        print(f"\n🚀 开始执行工作流: {user_request}")

        # Phase 1: 理解需求
        print("\n🧠 Phase 1: Brain理解需求")
        self.coordinator.assign_task(
            "brain",
            f"理解并规划以下需求: {user_request}"
        )
        time.sleep(5)

        # Phase 2: 架构设计
        print("\n🏗️ Phase 2: 架构设计")
        self.coordinator.assign_task(
            "architect",
            f"根据需求设计系统架构: {user_request}"
        )
        time.sleep(5)

        # Phase 3: 并行实现
        print("\n⚙️ Phase 3: 并行实现")
        tasks = {
            "coder": "实现核心功能代码",
            "tester": "准备测试方案"
        }
        self.coordinator.execute_parallel(tasks)

        # Phase 4: 整合结果
        print("\n🎯 Phase 4: 整合结果")
        self.coordinator.assign_task(
            "brain",
            "整合所有Agent的工作结果，提供最终方案"
        )
        time.sleep(5)

        return {
            'status': 'completed',
            'message': '工作流执行完成'
        }

    def shutdown(self):
        """关闭引擎"""
        self.coordinator.shutdown()

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("="*60)
    print("多Agent协作系统")
    print("="*60)

    # 创建工作流引擎
    engine = WorkflowEngine()

    try:
        # 设置Brain工作流
        print("\n⚙️ 设置Brain工作流...")
        engine.setup_brain_workflow()

        # 执行用户请求
        user_request = "实现一个用户认证系统"
        result = engine.execute_brain_workflow(user_request)

        print(f"\n✅ 工作流结果: {result['message']}")

        # 保持运行
        print("\n按Ctrl+C退出...")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n👋 正在退出...")
    finally:
        engine.shutdown()

if __name__ == "__main__":
    main()
```

### 7.2 实际应用示例

```python
# ==================== 示例1：代码审查系统 ====================

class CodeReviewSystem:
    """代码审查系统"""

    def __init__(self):
        self.coordinator = AgentCoordinator()

        # 创建Agent
        self.coordinator.create_agent(
            "reviewer",
            "代码审查员",
            "负责审查代码质量、发现潜在问题"
        )

        self.coordinator.create_agent(
            "security",
            "安全专家",
            "负责检查代码安全问题"
        )

        self.coordinator.create_agent(
            "optimizer",
            "性能优化师",
            "负责提出性能优化建议"
        )

    def review_code(self, file_path: str) -> dict:
        """审查代码"""
        # 读取代码
        with open(file_path, 'r') as f:
            code = f.read()

        # 并行审查
        tasks = {
            "reviewer": f"审查以下代码的质量:\n{code[:500]}...",
            "security": f"检查以下代码的安全问题:\n{code[:500]}...",
            "optimizer": f"分析以下代码的性能:\n{code[:500]}..."
        }

        results = self.coordinator.execute_parallel(tasks)

        return {
            'quality': results.get('reviewer'),
            'security': results.get('security'),
            'performance': results.get('optimizer')
        }

# ==================== 示例2：文档生成系统 ====================

class DocumentationSystem:
    """文档生成系统"""

    def __init__(self):
        self.coordinator = AgentCoordinator()

        # 创建Agent
        self.coordinator.create_agent(
            "doc_writer",
            "文档编写员",
            "负责编写技术文档"
        )

        self.coordinator.create_agent(
            "example_gen",
            "示例生成器",
            "负责生成使用示例"
        )

        self.coordinator.create_agent(
            "translator",
            "翻译员",
            "负责翻译文档"
        )

    def generate_docs(self, code_files: List[str]) -> dict:
        """生成文档"""
        tasks = {}

        for file_path in code_files:
            with open(file_path, 'r') as f:
                code = f.read()

            tasks[f"doc_{file_path}"] = f"为以下代码生成文档:\n{code[:300]}..."

        results = self.coordinator.execute_parallel(tasks)

        return results

# ==================== 示例3：测试系统 ====================

class TestingSystem:
    """测试系统"""

    def __init__(self):
        self.coordinator = AgentCoordinator()

        # 创建Agent
        self.coordinator.create_agent(
            "unit_tester",
            "单元测试员",
            "负责编写单元测试"
        )

        self.coordinator.create_agent(
            "integration_tester",
            "集成测试员",
            "负责编写集成测试"
        )

        self.coordinator.create_agent(
            "e2e_tester",
            "E2E测试员",
            "负责编写端到端测试"
        )

    def generate_tests(self, feature_spec: str) -> dict:
        """生成测试"""
        tasks = {
            "unit_tester": f"为以下功能编写单元测试:\n{feature_spec}",
            "integration_tester": f"为以下功能编写集成测试:\n{feature_spec}",
            "e2e_tester": f"为以下功能编写E2E测试:\n{feature_spec}"
        }

        return self.coordinator.execute_parallel(tasks)
```

---

## 8. 最佳实践建议

### 8.1 架构设计原则

1. **单一职责**: 每个Agent只负责一个明确的领域
2. **松耦合**: Agent间通过消息通信，避免直接依赖
3. **可扩展**: 支持动态添加和移除Agent
4. **容错性**: 单个Agent失败不应影响整个系统
5. **可观测**: 提供完整的日志和监控

### 8.2 性能优化

1. **并发控制**: 根据资源限制控制并发度
2. **任务优先级**: 实现优先级队列，确保重要任务优先
3. **缓存策略**: 缓存常用结果，减少重复计算
4. **资源池化**: 使用进程池和线程池复用资源
5. **负载均衡**: 合理分配任务给不同Agent

### 8.3 监控和调试

1. **详细日志**: 记录所有Agent的活动
2. **性能指标**: 跟踪响应时间、资源使用
3. **错误追踪**: 记录和分析错误
4. **状态监控**: 实时查看Agent状态
5. **可视化**: 使用仪表板展示系统状态

### 8.4 安全考虑

1. **权限控制**: 限制Agent的文件和系统访问
2. **输入验证**: 验证所有输入和消息
3. **沙箱隔离**: 在隔离环境中运行不受信任的Agent
4. **资源限制**: 防止Agent耗尽系统资源
5. **审计日志**: 记录所有敏感操作

---

## 9. 总结

本调研报告提供了使用Claude Code构建多Agent系统的完整技术方案，包括：

### 核心能力

1. **工具调用**: Claude Code CLI提供了丰富的工具集（Bash、Read、Write、Edit等）
2. **并发执行**: 支持多进程、异步IO、线程池等多种并发方式
3. **通信机制**: 共享文件系统、管道、消息队列等多种通信方案
4. **进程管理**: 完整的资源监控、限制和管理机制

### 技术方案

1. **多进程方案**: 适合独立任务，完全隔离
2. **异步并发方案**: 资源效率高，适合IO密集型
3. **消息队列方案**: 可扩展性强，适合大规模系统
4. **混合方案**: 结合多种技术，发挥各自优势

### 实践建议

1. **从简单开始**: 先实现基础功能，再逐步扩展
2. **模块化设计**: 保持组件独立，便于维护和扩展
3. **充分测试**: 确保每个Agent和通信机制都经过充分测试
4. **监控完善**: 建立完整的监控和日志系统
5. **文档齐全**: 维护详细的技术文档和使用指南

这个方案可以让多个Claude Code Agent像团队一样协作，同时工作于不同的任务，通过通信机制协调进度，最终实现1+1>2的效果。

---

**文档版本**: v1.0
**最后更新**: 2026-02-05
**作者**: 基于 system-max 代码库的深入调研
