# Compound Engineering 快速参考

## ⚠️ 重要修复

**原命令使用冒号 `:` 分隔符，已全部替换为连字符 `-`**

**请使用新的命令名称**：
- `/workflows-brainstorm` ✅ （不是 `/workflows:brainstorm`）
- `/workflows-plan` ✅
- `/workflows-work` ✅
- `/workflows-review` ✅
- `/workflows-compound` ✅

---

## 核心流程

```
BRAINSTORM → PLAN → WORK → REVIEW → COMPOUND
   ↓          ↓      ↓       ↓         ↓
 探索方案    详细计划  执行开发   多Agent审查   知识积累
```

## 常用命令速查

### 工作流命令（已修复）
```bash
/workflows-brainstorm  # 头脑风暴
/workflows-plan        # 详细规划
/workflows-work        # 执行开发
/workflows-review      # 代码审查
/workflows-compound    # 知识积累
```

### 快捷命令
```bash
/lfg                  # 全自动工作流 ⭐推荐
/slfg                 # 群体模式并行
/technical-review       # 多维度审查
/deepen-plan          # 增强计划
/changelog            # 生成变更日志
```

### 其他实用命令
```bash
/create-agent-skill     # 创建技能
/heal-skill            # 修复技能
/generate-command       # 生成命令
/report-bug            # 报告Bug
/reproduce-bug         # 复现Bug
/resolve-parallel       # 并行解决TODO
/resolve-todo-parallel  # 并行解决待办
/test-browser          # 浏览器测试
/test-xcode           # iOS测试
/feature-video         # 录制演示视频
/triage               # 分类问题
```

## 常用 Agent

### 代码审查
```bash
agent dhh-rails-reviewer              # Rails 代码审查
agent kieran-python-reviewer           # Python 代码审查
agent kieran-typescript-reviewer       # TypeScript 代码审查
agent security-sentinel               # 安全漏洞审查
agent performance-oracle              # 性能分析
agent code-simplicity-reviewer        # 简洁性审查
```

### 研究分析
```bash
agent best-practices-researcher       # 搜索最佳实践
agent framework-docs-researcher       # 框架文档研究
agent learnings-researcher           # 团队历史学习
agent git-history-analyzer           # Git 历史分析
agent pattern-recognition-specialist  # 模式识别
```

### 架构与设计
```bash
agent architecture-strategist         # 架构分析
agent design-implementation-reviewer   # 设计实现审查
agent data-integrity-guardian        # 数据完整性
```

### 数据与部署
```bash
agent data-migration-expert            # 数据迁移
agent schema-drift-detector            # Schema 变更检测
agent deployment-verification-agent    # 部署验证
```

## 常用技能

### 编码风格
```bash
skill dhh-rails-style              # DHH Rails 风格
skill andrew-kane-gem-writer      # Andrew Kane Gem 风格
```

### 前端开发
```bash
skill frontend-design              # 前端界面设计
skill agent-browser               # 浏览器自动化
```

### 知识管理
```bash
skill compound-docs               # 文档化学习
skill brainstorming              # 协作头脑风暴
skill git-worktree              # Git worktree 管理
skill document-review            # 文档审查
```

### 图像生成
```bash
skill gemini-imagegen            # AI 图像生成
```

### 文件传输
```bash
skill rclone                    # 文件上传到云存储
```

## 典型工作流程

### 1. 新功能开发
**推荐方式（使用 /lfg）**：
```bash
/lfg                     # 一键完成全流程
```

**手动方式**：
```bash
/workflows-brainstorm     # 探索方案
/workflows-plan          # 详细计划
/workflows-work          # 执行开发
/workflows-review        # 审查代码
/workflows-compound      # 记录学习
```

### 2. Bug 修复
```bash
/reproduce-bug                    # 复现问题
agent learnings-researcher "搜索历史方案"  # 搜索历史
[修复代码]                        # 修复问题
agent security-sentinel "安全审查"       # 验证修复
skill compound-docs "记录解决方案"        # 记录学习
```

### 3. 代码审查
```bash
# 单一审查
agent kieran-rails-reviewer "审查这段代码"

# 多维度审查
/technical-review

# 群体模式（并行多 Agent）
/slfg
```

### 4. 快速任务
```bash
/lfg                     # 一键完成
```

### 5. 研究阶段（写代码前）
```bash
agent best-practices-researcher "搜索XXX的最佳实践"   # 最佳实践
agent framework-docs-researcher "查找XXX的文档"     # 框架文档
agent learnings-researcher "搜索之前如何解决XXX"    # 历史学习
agent git-history-analyzer "分析XXX的历史变更"      # 代码演进
```

## 时间分配原则

```
40% Plan    - 充分规划，避免返工
20% Work    - 执行开发
40% Review  - 多Agent审查
持续 Compound - 知识积累
```

## 组件统计

| 类型 | 数量 |
|------|------|
| Agents | 29 |
| Commands | 24 |
| Skills | 18 |
| MCP Servers | 1 (Context7) |

## 常见问题

**Q: 命令显示 Unknown skill？**
A: 使用新的命令名称（用连字符代替冒号）
- `/workflows-brainstorm` ✅
- `/workflows-plan` ✅
- `/lfg` ✅

**Q: MCP 服务器不工作？**
```json
// 添加到 ~/.claude/settings.json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

**Q: 如何更新插件？**
```bash
cd ~/.claude/plugins/marketplaces/compound-engineering-plugin
git pull
```

**Q: Agent 调用失败？**
1. 确认 Agent 名称正确（见上方列表）
2. 确认插件已正确安装
3. 检查是否有权限问题

## 资源链接

- GitHub: https://github.com/EveryInc/compound-engineering-plugin
- 博客介绍: https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
- 完整文档: 见 COMPOUND_ENGINEERING_GUIDE.md
