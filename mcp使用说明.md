# MCP 使用说明（小白版）

本文教你在 Codex 里使用 3 个 MCP：
- `pencil`：做设计稿相关操作（读样式、改属性、批量改图层等）
- `chrome-devtools`：控制浏览器（打开网页、截图、看控制台、查网络请求）
- `context7`：查官方文档/API 用法

---

## 1. 先理解 MCP 是什么

把 MCP 理解成“给 AI 装工具箱”：
- 没有 MCP：AI 只能聊天、写代码
- 有 MCP：AI 还能“动手”操作外部工具（浏览器、设计软件、文档检索）

你现在已经连接成功了（`/mcp` 看到 3 个都 `enabled`）。

---

## 2. 使用前检查（每次 10 秒）

1. 进入项目目录：`D:\AI_Projects\system-max`
2. 启动 Codex（你当前这套已可用）
3. 在 Codex 输入：`/mcp`
4. 确认：
- `chrome-devtools` = enabled
- `context7` = enabled
- `pencil` = enabled

如果都 enabled，就可以开始用了。

---

## 3. 三个 MCP 各自怎么用

## 3.1 `context7`（先查文档，再写代码）

适合场景：
- 不确定某个库的最新 API
- 想按官方文档写法实现功能
- 避免“AI 凭记忆瞎写”

你可以直接这样说：
- “用 context7 查 React Router v7 的路由写法，然后给我最小示例。”
- “用 context7 查 FastAPI 文件上传官方示例，按我项目结构改成可运行代码。”
- “用 context7 查 Playwright 如何等待网络空闲，再改我这段测试。”

推荐工作流：
1. 先让它“查文档并给出处”
2. 再让它“按你项目改代码”
3. 最后让它“跑测试/构建验证”

---

## 3.2 `chrome-devtools`（让 AI 直接操作浏览器）

适合场景：
- 打开页面并截图
- 查看 Console 报错
- 查看 Network 请求是否 200/401/500
- 自动填表、点按钮、复现前端问题

你可以直接这样说：
- “用 chrome-devtools 打开 http://localhost:3000，截首页图并保存问题点。”
- “用 chrome-devtools 复现登录失败，抓控制台错误和失败请求。”
- “帮我检查这个页面首屏慢在哪里，给出 3 条优化建议。”

高频能力（你能在 `/mcp` 里看到）：
- `navigate_page`：打开页面
- `take_screenshot`：截图
- `get_console_message` / `list_console_messages`：看报错
- `list_network_requests`：看接口请求
- `fill` / `click` / `fill_form`：自动操作页面

---

## 3.3 `pencil`（让 AI 改设计稿）

适合场景：
- 读取设计规范（颜色、字号、间距）
- 批量统一样式
- 替换图层属性
- 自动截图当前画布

你可以直接这样说：
- “用 pencil 打开当前文档，读取 style guide，告诉我主色和字体规范。”
- “把所有按钮圆角统一成 8，主按钮背景改为 #1677FF。”
- “找出画布上空白区域，新增一个 320x120 的信息卡片。”
- “给首页做快照，并列出不一致的样式点。”

高频能力（你当前可用）：
- `open_document`
- `get_style_guide` / `get_style_guide_tags`
- `search_all_unique_properties`
- `replace_all_matching_properties`
- `set_variables`
- `snapshot_layout` / `get_screenshot`

---

## 4. 小白最实用的 6 个“万能提示词”

1. `先用 context7 查官方文档，再动代码；每一步给我你做了什么。`
2. `用 chrome-devtools 复现这个 bug：<现象>，最后给根因和修复建议。`
3. `用 pencil 读取当前设计规范，并输出可执行的前端样式 token。`
4. `先别改代码，先查文档+看浏览器报错+给排查计划。`
5. `改完后请跑测试/构建，并贴出关键结果。`
6. `请用小白能看懂的话解释你刚才每一步。`

---

## 5. 推荐学习路径（7 天）

Day 1-2：
- 只练 `context7`：问 10 个“官方文档问题”

Day 3-4：
- 只练 `chrome-devtools`：截图、查控制台、查网络请求

Day 5-6：
- 只练 `pencil`：读规范、改样式、导出快照

Day 7：
- 串起来做一次完整任务：
  1) context7 查方案  
  2) chrome-devtools 复现并验证  
  3) pencil 对齐设计  

---

## 6. 常见问题（FAQ）

### Q1：`/mcp` 显示 enabled，但我感觉没生效？
- 先明确说：`请使用 <mcp名> 来完成，不要只给文字答案。`
- 让它输出“已调用了哪些 MCP 工具”。

### Q2：为什么会超时？
- 首次启动常见（尤其 `npx` 下载包）
- 你现在已把超时配置为 60 秒，通常足够

### Q3：`pencil` 报路径错误怎么办？
- 用 ASCII 路径最稳（你现在已经是）
- 当前有效路径：`D:\AI_Projects\system-max\tools\pencil-mcp-server.exe`

### Q4：什么时候该用哪个 MCP？
- 查“正确写法”：`context7`
- 查“页面真实运行问题”：`chrome-devtools`
- 查“设计稿和样式一致性”：`pencil`

---

## 7. 一句话速查

- 文档不会写：先 `context7`
- 页面有 bug：上 `chrome-devtools`
- 设计要统一：用 `pencil`

把这三者连起来，你就不是“只会聊天的 AI”，而是“能查、能看、能改、能验证”的实战工作流。
