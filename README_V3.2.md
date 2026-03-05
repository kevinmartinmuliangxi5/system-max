# Ralph v3.2 - 三终端协作架构

> Brain规划 + Worker执行 + Reviewer审查 = 最高质量代码

---

## 架构概览

```
终端1: Brain (Claude Code - 你自己)
  ├─ 模型：Claude Sonnet 4.5 (Claude Pro)
  ├─ 职责：任务规划、需求分析、架构设计
  └─ 输出：规格文档 + 任务蓝图
     ↓
终端2: Reviewer (GLM)
  ├─ 模型：GLM-4.7 + 静态工具
  ├─ 职责：代码审查、质量把关
  └─ 监控：.ralph/queue/pending/
     ↑ 审查反馈
     ↓
终端3: Worker (GLM)
  ├─ 模型：GLM-4.7
  ├─ 职责：代码生成、执行
  ├─ 读取：Brain的蓝图
  └─ 提交：代码到Reviewer
```

---

## 快速启动

### 步骤1：Brain规划任务（你自己）

```bash
# 在Claude Code终端中
# 1. 读取 .ralph/BRAIN_README.md 了解你的职责
# 2. 根据用户需求，创建：
#    - .ralph/specs/<任务名>.md (技术规格)
#    - .janus/project_state.json (任务蓝图)
```

**示例用户需求**:
```
"创建用户登录功能，支持邮箱和密码"
```

**你应该创建**:
- `.ralph/specs/用户登录功能.md` - 详细规格
- `.janus/project_state.json` - 任务蓝图（包含instruction和target_files）

### 步骤2：启动Reviewer（终端2）

```bash
# 打开第二个终端
cd D:\AI_Projects\system-max

# 启动Reviewer（带实时进度）
bash .ralph/reviewer_loop.sh --live
```

**Reviewer会**:
- 监控Worker提交的代码
- 三层审查（静态 + GLM + 综合）
- 记录审查经验
- 给Worker反馈

### 步骤3：启动Worker（终端3）

```bash
# 打开第三个终端
cd D:\AI_Projects\system-max

# 启动Worker
bash .ralph/worker_loop.sh
```

**Worker会**:
- 读取Brain的蓝图
- 使用GLM生成代码
- 提交给Reviewer
- 根据反馈迭代修复

### 步骤4：观察协作

**三个终端同时运行**:
- 终端1（Brain）: 你继续规划下一个任务
- 终端2（Reviewer）: 实时显示审查进度
- 终端3（Worker）: 显示代码生成进度

**自动协作流程**:
```
Worker生成代码 → Reviewer审查 → 反馈 → Worker修复 → 循环直到通过
```

### 停止

在任意Worker或Reviewer终端按 `Ctrl+C` 即可停止

---

## 核心文件说明

### Brain相关（你创建）

| 文件 | 用途 | 谁创建 |
|------|------|--------|
| `.ralph/specs/<任务名>.md` | 技术规格文档 | Brain (你) |
| `.janus/project_state.json` | 任务蓝图 | Brain (你) |
| `.ralph/BRAIN_README.md` | Brain工作手册 | 系统提供 |

### Worker相关

| 文件 | 用途 |
|------|------|
| `.ralph/worker_loop.sh` | Worker主程序 |
| `.ralph/worker_status.json` | Worker状态 |
| `.ralph/logs/worker.log` | Worker日志 |

### Reviewer相关

| 文件 | 用途 |
|------|------|
| `.ralph/reviewer_loop.sh` | Reviewer主程序 |
| `.ralph/reviewer_status.json` | Reviewer状态 |
| `.ralph/review_experience.jsonl` | 审查经验库 |
| `.ralph/logs/reviewer.log` | Reviewer日志 |

### 通信队列

| 目录 | 用途 |
|------|------|
| `.ralph/queue/pending/` | Worker提交的待审查代码 |
| `.ralph/queue/approved/` | 通过审查的代码 |
| `.ralph/queue/rejected/` | 未通过审查的代码 |
| `.ralph/feedback/` | Reviewer给Worker的反馈 |

---

## 工作流程详解

### Brain的工作（你）

1. **理解需求** - 分析用户意图
2. **提出问题** - 澄清不明确的地方
3. **编写规格** - 创建详细的技术规格（`.ralph/specs/*.md`）
4. **生成蓝图** - 创建任务蓝图（`.janus/project_state.json`）

**关键**：你的规划质量决定整个系统的成功率！

详细说明：`.ralph/BRAIN_README.md`

### Worker的工作

1. 读取Brain的蓝图
2. 读取规格文档
3. 使用GLM-4.7生成代码
4. 提交到 `.ralph/queue/pending/`
5. 等待Reviewer反馈
6. 如果不通过，根据反馈修复

### Reviewer的工作

1. 监控 `.ralph/queue/pending/`
2. **第一层**：静态分析（pylint, bandit）
3. **第二层**：GLM AI审查（逻辑、性能、安全）
4. **第三层**：综合决策（评分 >= 7分通过）
5. 记录审查经验到 `.ralph/review_experience.jsonl`
6. 给Worker反馈

---

## 配额和成本

### Brain (Claude Pro)
- **用途**: 仅任务规划
- **每任务**: 1次CLI调用（你自己在终端操作）
- **月度**: 按实际使用
- **成本**: Claude Pro订阅（包月）

### Worker (GLM)
- **用途**: 代码生成
- **每任务**: 10-20次API调用
- **月度**: 3000-6000次
- **成本**: GLM Coding Plan（包月无限）

### Reviewer (GLM)
- **用途**: 代码审查
- **每任务**: 3-5次API调用
- **月度**: 900-1500次
- **成本**: GLM Coding Plan（包月无限）

**总成本**: 双包月订阅，零额外费用

---

## 常见问题

### Q: Brain就是我（Claude Code）？

**A**: 是的！你在终端中打开Claude Code，你就是Brain。你负责：
1. 阅读 `.ralph/BRAIN_README.md` 了解职责
2. 根据用户需求创建规格和蓝图
3. 其他交给Worker和Reviewer

### Q: 必须三个终端吗？

**A**: 是的，推荐三终端：
- 终端1: Claude Code (你) - Brain
- 终端2: Reviewer - 实时审查
- 终端3: Worker - 代码生成

### Q: 能否只用两个终端？

**A**: 可以，但不推荐：
- 终端1: Claude Code (你) + Worker（前台）
- 终端2: Reviewer

但这样你（Brain）就无法继续规划新任务了。

### Q: start_ralph_v3.2.sh 有什么用？

**A**: 可选的便利工具，可以自动：
- 用tmux同时启动Worker + Reviewer
- 分屏显示
- 依赖检查

**但手动启动更简单清晰**：
```bash
# 终端2
bash .ralph/reviewer_loop.sh --live

# 终端3
bash .ralph/worker_loop.sh
```

### Q: 如何查看审查历史？

**A**:
```bash
# 查看所有审查经验
cat .ralph/review_experience.jsonl | jq .

# 查看统计
jq -s 'map(select(.approved == true)) | length' .ralph/review_experience.jsonl
```

### Q: 审查标准是什么？

**A**:
- 静态分析评分: 0-10
- GLM AI评分: 0-10
- 综合评分 = 静态40% + GLM60%
- **通过标准**: >= 7分

### Q: Worker和Reviewer如何通信？

**A**: 基于文件队列：
```
Worker生成代码 → .ralph/queue/pending/
Reviewer发现 → 审查 → .ralph/feedback/<task_id>.json
Worker读反馈 → 修复 → 重新提交
```

---

## 目录结构

```
system-max/
├── README_V3.2.md              # 本文件
├── .ralph/
│   ├── BRAIN_README.md         # Brain工作手册（必读！）
│   ├── worker_loop.sh          # Worker主程序
│   ├── reviewer_loop.sh        # Reviewer主程序
│   ├── specs/                  # Brain创建的规格文档
│   ├── queue/                  # 任务队列
│   │   ├── pending/            # 待审查
│   │   ├── approved/           # 已通过
│   │   └── rejected/           # 未通过
│   ├── feedback/               # 审查反馈
│   ├── logs/                   # 日志
│   └── review_experience.jsonl # 审查经验库
├── .janus/
│   └── project_state.json      # Brain创建的任务蓝图
└── src/                        # 代码（Worker生成）
```

---

## 简化启动流程

### 最简单的方式（手动三终端）

```bash
# 终端1: Brain (Claude Code)
# - 你在这里，规划任务
# - 创建规格和蓝图

# 终端2: Reviewer
bash .ralph/reviewer_loop.sh --live

# 终端3: Worker
bash .ralph/worker_loop.sh
```

### 可选的便利方式（tmux自动化）

```bash
# 一键启动Worker + Reviewer
bash .ralph/start_ralph_v3.2.sh

# 选择tmux模式，自动分屏
# 你（Brain）仍然在终端1工作
```

---

## 优势总结

✅ **分工明确** - Brain规划、Worker执行、Reviewer审查
✅ **质量最高** - Brain用Claude Pro，三层审查
✅ **成本固定** - 双包月订阅，零额外费用
✅ **持续学习** - Reviewer记录经验，越用越智能
✅ **实时可视** - Reviewer --live模式，进度清晰
✅ **独立审查** - Worker不审查自己，客观公正

---

## 下一步

1. **阅读Brain手册** - `.ralph/BRAIN_README.md`（必读）
2. **启动Reviewer** - 终端2运行
3. **启动Worker** - 终端3运行
4. **开始规划** - 你（Brain）创建规格和蓝图
5. **观察协作** - Worker和Reviewer自动完成任务

---

**Ralph v3.2 = 三终端协作 = 最高质量 + 零额外成本**

**Brain (你) → Worker (GLM) → Reviewer (GLM) = 完美配合！** 🎉
