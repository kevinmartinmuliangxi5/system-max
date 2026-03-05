# Ralph v3.2 最终架构 - 简洁版

## 核心原则

**分工明确，各司其职**
- Brain用Claude Pro做最高质量规划
- Ralph用GLM做大量执行和审查
- Worker和Review都在Ralph层完成

---

## 系统架构

```
用户需求
   ↓
┌──────────────────────────────────────┐
│ Brain层 (brain_v3.py)                 │
│                                       │
│ 使用: Claude Pro (Sonnet 4.5)        │
│ 职责: 规划和设计                      │
│                                       │
│ CE代理:                               │
│  ├─ req_dev      (需求分析)          │
│  ├─ spec_writer  (规格编写)          │
│  ├─ architect    (架构设计)          │
│  └─ brainstorm   (方案探索)          │
│                                       │
│ 产出:                                 │
│  ├─ 蓝图 (.janus/project_state.json) │
│  ├─ 规格 (.ralph/specs/*.md)         │
│  └─ 流程图 (.ralph/diagrams/)        │
│                                       │
│ 用量: 600-900次/月（2000次配额）      │
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Dealer层 (dealer_enhanced.py)        │
│                                       │
│ 职责: 生成详细执行指令                 │
│ 无AI调用，纯本地逻辑                   │
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Ralph层 (ralph_loop.sh)              │
│                                       │
│ 使用: GLM-4.7 + GLM-4.5-Air          │
│ 职责: 执行和审查                      │
│                                       │
│ Worker (代码生成):                    │
│  ├─ 读取蓝图和规格                    │
│  ├─ 调用GLM生成代码                   │
│  ├─ 执行编译/测试                     │
│  └─ 迭代修复                          │
│                                       │
│ Review (质量把关):                    │
│  ├─ 静态分析 (pylint, bandit)        │
│  ├─ GLM代码审查                       │
│  ├─ 安全检查                          │
│  └─ 性能优化建议                      │
│                                       │
│ 用量: GLM包月无限                     │
└──────────────────────────────────────┘
   ↓
完成的代码
```

---

## Brain层实现

### 文件: `brain_v3.py`

**已完成修改**:
```python
from claude_pro_ce_agent import ClaudeProCEAgent

class BrainV3:
    def __init__(self):
        # 使用Claude Pro进行规划
        self.ce_agent = ClaudeProCEAgent()

    def plan_task(self, user_input: str):
        # 1. 需求分析（Claude Pro）
        analysis = self.ce_agent.invoke("req_dev", user_input)

        # 2. 规格编写（Claude Pro）
        spec = self.ce_agent.invoke("spec_writer", analysis)

        # 3. 架构设计（Claude Pro，如果需要）
        if self._needs_architecture(analysis):
            architecture = self.ce_agent.invoke("architect", analysis)

        # 4. 任务分解（本地逻辑）
        phases = self.decompose_to_phases(task_info)

        # 5. 保存蓝图
        self.save_blueprint(phases)
```

**配置**:
- 需要设置环境变量: `ANTHROPIC_API_KEY`（Claude Pro的API key）
- 或使用Claude Code CLI的默认配置

---

## Ralph层实现

### Worker (已有，继续使用GLM)

**文件**: `ralph_loop.sh`

**当前配置**（保持不变）:
```bash
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
```

**工作流程**:
1. 读取Brain生成的蓝图
2. 根据规格文档编写代码
3. 执行测试和验证
4. 如果失败，迭代修复

### Review (需要增强)

**新增**: `glm_reviewer.py`

```python
class GLMReviewer:
    """GLM代码审查器（用于Ralph层）"""

    def __init__(self):
        self.glm_client = Anthropic(
            api_key="434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg",
            base_url="https://open.bigmodel.cn/api/anthropic"
        )
        self.model = "glm-4.7"

    def review_code(self, code: str, context: str) -> Dict:
        """代码审查"""
        # 1. 静态分析
        static_result = self.run_static_analysis(code)
        if static_result['score'] < 5:
            return static_result

        # 2. GLM AI审查
        glm_result = self.run_glm_review(code, context)

        return glm_result

    def run_static_analysis(self, code: str) -> Dict:
        """运行pylint, bandit等工具"""
        # 调用pylint
        # 调用bandit
        # 综合评分
        pass

    def run_glm_review(self, code: str, context: str) -> Dict:
        """GLM AI代码审查"""
        prompt = f"""代码审查：

{code}

请检查安全、性能、规范问题。"""

        response = self.glm_client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return self._parse_review_result(response.content[0].text)
```

---

## 配额管理

### Claude Pro (Brain)

**月配额**: 2000次

**预估使用**:
```
简单任务: 2次调用/任务（req_dev + spec_writer）
复杂任务: 4次调用/任务（req_dev + spec + architect + brainstorm）

平均: 3次/任务
每天10个任务: 30次/天
每月: 900次

使用率: 45%
剩余: 55%（1100次余量）
```

### GLM (Ralph)

**月配额**: 包月无限

**预估使用**:
```
Worker: 10-20次/任务
Review: 3-5次/任务

平均: 15次/任务
每天10个任务: 150次/天
每月: 4500次

成本: 0（包月固定）
```

---

## 实施步骤

### ✅ 已完成

1. Brain层改用Claude Pro CE Agent
2. 创建`claude_pro_ce_agent.py`
3. 更新`brain_v3.py`导入和初始化

### 📋 待完成（本周）

1. **配置Claude Pro API Key**
   ```bash
   # Windows
   setx ANTHROPIC_API_KEY "sk-ant-..."

   # 或在.env文件
   echo ANTHROPIC_API_KEY=sk-ant-... >> .env
   ```

2. **创建GLM Reviewer**
   ```bash
   # 创建.ralph/tools/glm_reviewer.py
   # 实现静态分析 + GLM审查
   ```

3. **集成到Ralph Loop**
   ```bash
   # 修改ralph_loop.sh
   # 在Worker完成后调用GLM Reviewer
   ```

4. **测试完整流程**
   ```bash
   # 测试简单任务
   python brain_v3.py "添加一个hello函数"

   # 测试复杂任务
   python brain_v3.py "重构认证系统，支持OAuth2"

   # 验证配额使用
   # 确认Brain用Claude Pro
   # 确认Ralph用GLM
   ```

---

## 优势总结

### ✅ 质量最高
- Brain用最强模型（Claude Sonnet 4.5）
- 规划质量无损失

### ✅ 成本可控
- Brain: 45%配额使用，55%余量
- Ralph: 包月无限，0额外成本
- 总成本: 固定（两个包月订阅）

### ✅ 架构清晰
- Brain只管规划（不管执行和审查）
- Ralph管执行和审查（不管规划）
- 职责分明，易于维护

### ✅ 无需折腾
- 不需要复杂的路由逻辑
- 不需要动态切换模型
- 配置简单，一次设置，长期使用

---

## 监控建议

创建简单的使用日志：

```python
# .ralph/usage_log.json
{
  "date": "2026-02-11",
  "brain": {
    "provider": "claude_pro",
    "calls": 30,
    "quota_used": "1.5%"
  },
  "ralph": {
    "provider": "glm",
    "calls": 150,
    "quota": "unlimited"
  }
}
```

每天运行：
```bash
python .ralph/tools/check_usage.py
# 输出：今日Brain用量30次，月度累计900次（45%）
```

---

## 下一步行动

**今天**:
1. 设置Claude Pro API Key
2. 测试Brain的Claude Pro集成

**明天**:
1. 创建GLM Reviewer
2. 集成到Ralph Loop

**本周完成**:
- 完整测试
- 文档更新
- 开始使用v3.2！

---

**最简洁的架构 = Brain用Claude Pro规划 + Ralph用GLM执行和审查**

**零折腾，高质量，成本固定！**
