# UI 验收对照（A 风格执行版）

- 执行风格：A 企业稳健（唯一执行版本）
- 设计文件：`ai-image-ui-enterprise-calm.pen`
- 生效页面：
  - `Yhr64` A-Chat Home (Enterprise)
  - `MleJF` A-Editor Fullscreen (Enterprise)
  - `zO1VX` A-Result (Enterprise)
  - `2SL9v` A-State Loading (Standalone)
  - `JVzMt` A-State Error (Standalone)
  - `lzSVO` A-State Empty (Standalone)

## 1. PRD 关键链路对照

1. 首图生成（输入 -> 生成 -> 查看）
- 对应界面：`Yhr64`
- 对应模块：提示词输入区、发送按钮、消息/结果容器
- 验收点：3 步内可完成首图路径

2. 局部重绘（选区 -> 指令 -> 返回）
- 对应界面：`MleJF`
- 对应模块：画布、工具条（Brush/Erase/Undo/Redo）、编辑指令卡
- 验收点：编辑工具可见、提交动作明确、版本条可回看

3. 结果导出与继续编辑
- 对应界面：`zO1VX`
- 对应模块：主预览、保存/继续编辑/重试按钮、合规提示
- 验收点：结果操作路径完整、AIGC 合规信息可见

4. 异常恢复与状态可用
- 对应界面：`2SL9v`、`JVzMt`、`lzSVO`
- 验收点：
  - Loading：进度与动作（后台继续/查看队列）
  - Error：错误原因 + 重试/指南
  - Empty：首图引导 + 示例 Prompt + 快捷主题

## 2. 非功能要求映射

1. 可用性
- 状态闭环：Loading/Error/Empty 均有明确下一步动作。

2. 安全表达
- Chat 首页保留 BYOK 安全提示信息（本地存储、日志脱敏）。

3. 可观测性表达
- 首页 KPI 与结果页成本/状态摘要用于可观测信息展示。

## 3. 版本决策记录

1. B/C 方案仅保留为备选探索稿，已在画布中禁用（`enabled: false`）。
2. 后续 UI 迭代与实现统一以 A 风格页面 ID 为准。
