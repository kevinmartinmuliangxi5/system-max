# CE代理智能路由策略

## 关键信息

- **Brain**: 使用Claude Pro计划（量少，需最大化价值）
- **GLM**: Coding Plan包月（量足，可大量使用）

---

## 核心原则

**Claude Pro的价值最大化 = 只在最关键环节使用**

---

## 智能路由方案

### Brain层：100% GLM

**原因**:
1. Brain本身不生成代码，只做规划分析
2. 规划任务可以用GLM-4.7很好完成
3. 保留Claude Pro配额给Worker

**实施**:
```python
class BrainV3:
    def __init__(self):
        # Brain的CE代理全部使用GLM
        self.ce_agent = GLMCompoundEngineeringAgent()

        # Brain本身不调用Claude API
        # 只做本地操作：规格生成、任务分解、记忆检索
```

**Brain的工作**（全部本地/GLM）:
```
1. 需求分析 → GLM CE的req_dev_agent
2. 规格生成 → 本地模板 + GLM CE的spec_writer
3. 架构设计 → GLM CE的architect_agent
4. 任务分解 → 本地逻辑
5. 记忆检索 → 本地claude-mem数据库
6. 流程图生成 → 本地draw.io MCP
```

**成本**: 0（GLM包月无额外成本）

---

### Worker层：智能混合

**Claude Pro的最佳使用场景**:
1. **复杂代码生成**（架构级改动）
2. **困难bug修复**（需要深度推理）
3. **创新性设计**（需要创造力）
4. **多文件重构**（需要全局理解）

**GLM的使用场景**:
1. 简单功能添加
2. 配置文件修改
3. 文档编写
4. 测试用例生成
5. 代码审查

**实施策略**:
```python
class SmartRouter:
    def route_task(self, task: Dict) -> str:
        """决定使用哪个模型"""

        complexity_score = self._calculate_complexity(task)

        if complexity_score >= 8:
            # 复杂任务 → Claude Pro
            return "claude-sonnet-4-5"
        elif complexity_score >= 5:
            # 中等任务 → GLM-4.7（优先）
            if self.glm_available():
                return "glm-4.7"
            else:
                return "claude-sonnet-4-5"  # 降级
        else:
            # 简单任务 → GLM-4.5-Air（更快更便宜）
            return "glm-4.5-air"

    def _calculate_complexity(self, task: Dict) -> int:
        """计算任务复杂度 (0-10)"""
        score = 0

        # 文件数量
        files = task.get('target_files', [])
        if len(files) > 5:
            score += 3
        elif len(files) > 2:
            score += 2
        elif len(files) > 0:
            score += 1

        # 关键词检测
        instruction = task.get('instruction', '').lower()

        if any(word in instruction for word in ['架构', 'refactor', '重构', '设计']):
            score += 3

        if any(word in instruction for word in ['bug', '修复', 'fix', '错误']):
            score += 2

        if any(word in instruction for word in ['新增', 'add', '创建', 'create']):
            score += 1

        # CE分析结果
        ce_analysis = task.get('ce_analysis', {})
        risks = ce_analysis.get('risks', [])
        if len(risks) > 2:
            score += 2

        return min(score, 10)
```

---

### REVIEW层：GLM主力 + Claude Pro关键审查

**三层审查体系**:

```
第一层：静态分析（pylint, bandit）
        ↓ 评分 < 5
        ✗ 返回错误

第二层：GLM代码审查
        ↓ 发现security/critical问题
        ⚠️  触发第三层

第三层：Claude Pro深度审查（仅关键情况）
        ↓
        ✓ 最终决策
```

**实施**:
```python
class SmartReviewer:
    def review_code(self, code: str, context: str) -> Dict:
        # 第一层：静态分析（免费）
        static_result = self.run_static_analysis(code)
        if static_result['score'] < 5:
            return static_result  # 直接返回，不浪费AI配额

        # 第二层：GLM审查（包月无限）
        glm_result = self.glm_reviewer.review(code, context)

        # 判断是否需要Claude Pro
        needs_claude = (
            glm_result.get('quality_score', 10) < 7 or
            len(glm_result.get('security_warnings', [])) > 0 or
            'critical' in str(glm_result.get('issues', []))
        )

        if needs_claude:
            # 第三层：Claude Pro（仅关键情况）
            print("⚠️  检测到关键问题，启用Claude Pro深度审查")
            claude_result = self.claude_pro_reviewer.review(code, context)
            return claude_result

        return glm_result
```

**预计Claude Pro使用率**: 5-10%的审查任务

---

## 配额使用预估

### 假设场景：每天10个任务

| 环节 | 使用模型 | 次数/天 | Claude Pro消耗 | GLM消耗 |
|------|---------|---------|----------------|---------|
| Brain规划 | GLM-4.7 | 10次 | 0 | 10次 |
| Worker执行 | 混合 | 10次 | 2-3次 | 7-8次 |
| Code Review | 混合 | 10次 | 0-1次 | 9-10次 |
| **总计** | - | 30次 | **3-4次** | **26-28次** |

**结论**:
- Claude Pro: 每天仅3-4次调用（约10-13%使用率）
- GLM: 承担90%工作量
- Claude Pro配额用在刀刃上

---

## 实施计划

### 第一步：Brain集成GLM CE代理（今天完成）

```bash
# 修改brain_v3.py
- 导入GLMCompoundEngineeringAgent
- 替换CompoundEngineeringAgent
- 测试req_dev_agent、spec_writer_agent

# 验证Brain不消耗Claude Pro配额
```

### 第二步：Worker层智能路由（本周完成）

```bash
# 创建SmartRouter类
# 修改ralph_loop.sh，根据任务复杂度选择模型
# 添加配额监控

# 配置示例：
export SMART_ROUTING=true
export PRIMARY_MODEL="glm-4.7"        # 主力模型
export FALLBACK_MODEL="claude-sonnet-4-5"  # 关键任务
```

### 第三步：Review层智能审查（本周完成）

```bash
# 实现SmartReviewer
# 集成静态分析 + GLM + Claude Pro三层
# 只在关键情况触发Claude Pro
```

---

## 监控指标

```python
# 每日报告
{
    "date": "2026-02-11",
    "claude_pro": {
        "total_calls": 4,
        "by_stage": {
            "brain": 0,      # 目标：保持0
            "worker": 3,     # 目标：<5
            "review": 1      # 目标：<2
        },
        "quota_used": "0.4%",  # 假设月配额1000次
        "estimated_monthly": 120  # 预估月使用量
    },
    "glm": {
        "total_calls": 27,
        "quota_remaining": "充足"
    }
}
```

---

## 优势总结

✅ **Claude Pro配额节省90%**
   从30次/天 → 3-4次/天

✅ **质量不降反升**
   GLM-4.7在代码任务上表现优秀（73.8% SWE-bench）

✅ **智能降级机制**
   GLM不可用时自动切换Claude Pro

✅ **关键环节保障**
   复杂任务、安全审查仍用Claude Pro

✅ **成本可预测**
   GLM包月固定成本，Claude Pro用量可控

---

## 配置文件

`.ralph/routing_config.json`:
```json
{
  "brain": {
    "ce_provider": "glm",
    "ce_model": "glm-4.7",
    "use_claude": false
  },
  "worker": {
    "smart_routing": true,
    "primary_model": "glm-4.7",
    "fallback_model": "claude-sonnet-4-5",
    "complexity_threshold": 8
  },
  "review": {
    "layer1_static": true,
    "layer2_model": "glm-4.7",
    "layer3_model": "claude-sonnet-4-5",
    "layer3_trigger": ["security", "critical", "low_score"]
  },
  "monitoring": {
    "track_usage": true,
    "daily_report": true,
    "alert_threshold": 0.8
  }
}
```

---

**核心思想**: 让GLM做90%的工作，Claude Pro只在最需要的10%场景发挥价值。

**预期效果**: Claude Pro配额节省90%，质量保持甚至提升。
