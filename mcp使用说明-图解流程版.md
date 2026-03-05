# MCP 使用说明（图解流程版）

适用对象：第一次用 Codex + MCP 的同学  
目标：用最短路径把 3 个 MCP（`context7` / `chrome-devtools` / `pencil`）用起来

---

## 0) 启动总流程图

```text
打开 Codex
   ↓
输入 /mcp
   ↓
3个服务都 enabled 吗？
   ├─ 否 → 看文末“5) 快速排错”
   └─ 是 → 进入任务
           ↓
先判断任务类型（文档 / 页面 / 设计）
           ↓
调用对应 MCP
           ↓
输出结果 + 验证
```

---

## 1) 任务判断图（先选工具）

```text
你现在要做什么？
   ├─ 查官方文档/API写法 → context7
   ├─ 查网页报错/请求/截图 → chrome-devtools
   └─ 改设计稿/样式统一/变量 → pencil
```

口诀：
- 查“标准答案”用 `context7`
- 查“运行现场”用 `chrome-devtools`
- 查“设计一致性”用 `pencil`

---

## 2) 三个 MCP 的最小操作卡片

## A. context7（文档卡）
1. 说：`用 context7 查 XXX 官方文档，给最小可运行示例。`
2. 追问：`按我当前项目结构改代码。`
3. 验收：`运行测试/构建并给结果。`

---

## B. chrome-devtools（网页卡）
1. 说：`用 chrome-devtools 打开 <url> 并截图。`
2. 说：`抓 console 报错 + network 失败请求。`
3. 验收：`给根因 + 修复建议 + 修复后再验证一次。`

---

## C. pencil（设计卡）
1. 说：`用 pencil 打开文档并读取 style guide。`
2. 说：`批量统一按钮样式（圆角/颜色/字号）。`
3. 验收：`输出变更摘要 + 最新截图。`

---

## 3) 一条龙实战图（推荐）

```text
需求进来
  ↓
context7: 查官方做法
  ↓
chrome-devtools: 在页面复现并验证
  ↓
pencil: 对齐设计规范
  ↓
最终交付：代码 + 截图 + 验证结果
```

---

## 4) 可直接复制的 6 句指令

1. `先用 context7 查官方文档，再改代码。`
2. `用 chrome-devtools 复现这个 bug：<现象>。`
3. `把失败请求和 console 错误都贴出来。`
4. `用 pencil 读取样式规范并统一按钮。`
5. `改完后请截图并说明改动。`
6. `最后给我“结果+证据+剩余风险”。`

---

## 5) 快速排错（30 秒）

### 情况 1：`/mcp` 里某个不是 enabled
- 重启 Codex 再看 `/mcp`
- 先启动 Pencil Desktop（对 `pencil` 特别重要）

### 情况 2：有 enabled，但 AI 没实际调用
- 明确下指令：`必须使用 <mcp名> 完成，不要只给文字建议`

### 情况 3：`pencil` 报路径问题
- 你当前稳定路径是：`D:\AI_Projects\system-max\tools\pencil-mcp-server.exe`

---

## 6) 每次收尾检查

1. 工具是否真的调用了（不是只聊天）
2. 结果是否有证据（截图/日志/请求）
3. 是否做了回归验证（修复后再测一次）

做到这 3 条，MCP 基本就算“用对了”。
