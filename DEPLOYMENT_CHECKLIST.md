# 双脑Ralph系统 v3.0 部署检查清单

**确保系统正确部署和配置**

---

## 📋 部署前检查

### 系统要求

- [ ] **Python版本**: Python >= 3.8
- [ ] **操作系统**: Windows/Linux/macOS
- [ ] **磁盘空间**: >= 50MB
- [ ] **网络**: 可选（仅API调用需要）

### 权限检查

- [ ] 读写 `.janus/` 目录权限
- [ ] 读写 `.ralph/` 目录权限
- [ ] 剪贴板访问权限

---

## 📦 Step 1: 依赖安装

### 1.1 核心依赖（必需）

```bash
pip install pyperclip
```

- [ ] **pyperclip** 安装成功
- [ ] 测试: `python -c "import pyperclip; print('OK')"`

### 1.2 推荐依赖

```bash
pip install colorama
```

- [ ] **colorama** 安装成功（可选，用于彩色输出）
- [ ] 测试: `python -c "import colorama; print('OK')"`

### 1.3 可选增强依赖

```bash
pip install jieba pytest flake8
```

- [ ] **jieba** - 中文分词（可选）
- [ ] **pytest** - 单元测试（可选）
- [ ] **flake8** - 代码检查（可选）

### 1.4 运行依赖检查脚本

```bash
python .ralph/scripts/check_dependencies.py
```

**预期输出**:
```
✓ 核心依赖满足，系统可以运行
```

- [ ] 依赖检查通过

---

## 📁 Step 2: 目录结构验证

### 2.1 核心目录

```bash
# 验证目录存在
ls -ld .janus .ralph
```

- [ ] `.janus/` 目录存在
- [ ] `.ralph/` 目录存在

### 2.2 .janus/ 核心文件

```bash
ls .janus/core/*.py
ls .janus/project_state.json 2>/dev/null || echo "待生成"
```

- [ ] `.janus/core/hippocampus.py` 存在
- [ ] `.janus/core/router.py` 存在
- [ ] `.janus/core/thinkbank.py` 存在
- [ ] `.janus/core/cache_manager.py` 存在
- [ ] `.janus/project_state.json` （待Brain生成）

### 2.3 .ralph/ 工具层

```bash
ls .ralph/tools/*.py
```

- [ ] `.ralph/tools/tools_manager.py` 存在
- [ ] `.ralph/tools/memory_integrator.py` 存在
- [ ] `.ralph/tools/claude_mem_enhanced.py` 存在
- [ ] `.ralph/tools/config.json` 存在
- [ ] `.ralph/tools/superpowers_rules.md` 存在

### 2.4 .ralph/ Context Engineering

```bash
ls .ralph/context/*.md
ls .ralph/context/modules/*.md
```

- [ ] `.ralph/context/project-info.md` 存在
- [ ] `.ralph/context/architecture.md` 存在
- [ ] `.ralph/context/coding-style.md` 存在
- [ ] `.ralph/context/decisions.md` 存在
- [ ] `.ralph/context/dependencies.md` 存在
- [ ] `.ralph/context/modules/brain.md` 存在
- [ ] `.ralph/context/modules/dealer.md` 存在
- [ ] `.ralph/context/modules/worker.md` 存在

### 2.5 核心脚本

```bash
ls brain_v3.py dealer_v3.py
ls .ralph/PROMPT_V3.md
ls .ralph/scripts/*.py
```

- [ ] `brain_v3.py` 存在
- [ ] `dealer_v3.py` 存在
- [ ] `.ralph/PROMPT_V3.md` 存在
- [ ] `.ralph/scripts/check_dependencies.py` 存在
- [ ] `.ralph/scripts/integration_test.py` 存在

---

## ⚙️ Step 3: 配置文件检查

### 3.1 基础配置 (.janus/config.json)

```bash
cat .janus/config.json
```

**最小配置**:
```json
{
  "ZHIPU_API_KEY": "",
  "ANTHROPIC_BASE_URL": "",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": ""
}
```

- [ ] `.janus/config.json` 存在
- [ ] JSON格式正确
- [ ] API配置（可选，仅Worker模式需要）

### 3.2 工具配置 (.ralph/tools/config.json)

```bash
cat .ralph/tools/config.json
```

**检查项**:
```json
{
  "tools": {
    "superpowers": {"enabled": true},
    "claude_mem": {"enabled": true},
    "compound_engineering": {"enabled": true}
  },
  "memory_integrator": {
    "hippocampus_weight": 0.6,
    "claude_mem_weight": 0.4
  }
}
```

- [ ] `.ralph/tools/config.json` 存在
- [ ] JSON格式正确
- [ ] `tools` 配置正确
- [ ] `memory_integrator` 权重配置合理（60/40）

---

## 🧪 Step 4: 功能测试

### 4.1 运行集成测试

```bash
python .ralph/scripts/integration_test.py
```

**必须通过的测试**:
- [ ] ✅ 环境检查
- [ ] ✅ Brain v3功能
- [ ] ✅ Dealer v3功能
- [ ] ✅ 双记忆系统
- [ ] ✅ Context Engineering
- [ ] ✅ 端到端流程
- [ ] ✅ 性能基准

**预期结果**:
```
总测试数: 7
通过: 7 ✅
失败: 0 ❌
通过率: 100.0%

🎉 所有测试通过！系统集成完整，可以投入使用！
```

- [ ] 所有测试通过
- [ ] 生成测试报告 `.ralph/test_report.md`

### 4.2 测试Brain v3

```bash
python brain_v3.py "部署测试任务"
```

**检查生成的文件**:
- [ ] `.janus/project_state.json` 生成成功
- [ ] `.ralph/specs/部署测试任务.md` 生成成功
- [ ] `.ralph/diagrams/task-flow.txt` 生成成功

**检查蓝图内容**:
```bash
cat .janus/project_state.json | grep -A 5 blueprint
```

- [ ] 蓝图包含 `blueprint` 字段
- [ ] 任务分解合理
- [ ] 至少1个Phase

### 4.3 测试Dealer v3

```bash
python dealer_v3.py
```

**检查输出**:
- [ ] 读取蓝图成功
- [ ] 检测操作类型
- [ ] 加载Context Engineering
- [ ] 检索双记忆系统
- [ ] 生成完整指令
- [ ] 复制到剪贴板成功

**验证剪贴板**:
```bash
# Windows
powershell Get-Clipboard | Select-Object -First 10

# Linux/Mac
xclip -o -selection clipboard | head -10  # 或 pbpaste | head -10
```

- [ ] 指令包含 "Superpowers"
- [ ] 指令包含 "质量门控"
- [ ] 指令包含 "双记忆系统"
- [ ] 指令长度 > 3000字符

### 4.4 测试模块导入

```bash
python -c "from brain_v3 import BrainV3; print('Brain OK')"
python -c "from dealer_v3 import DealerV3; print('Dealer OK')"
python -c "import sys; sys.path.append('.ralph/tools'); from tools_manager import get_tools_manager; print('Tools OK')"
python -c "import sys; sys.path.append('.ralph/tools'); from memory_integrator import get_memory_integrator; print('Memory OK')"
```

- [ ] Brain v3 导入成功
- [ ] Dealer v3 导入成功
- [ ] Tools Manager 导入成功
- [ ] Memory Integrator 导入成功

---

## 📖 Step 5: 文档完整性检查

### 5.1 用户文档

- [ ] `README.md` 更新到v3.0
- [ ] `QUICK_START_V3.md` 存在且完整
- [ ] `UPGRADE_GUIDE.md` 存在（从v2.x升级指南）
- [ ] `DEPLOYMENT_CHECKLIST.md` 存在（本文件）

### 5.2 Context Engineering文档

- [ ] `.ralph/context/project-info.md` - 项目信息完整
- [ ] `.ralph/context/architecture.md` - 架构描述完整
- [ ] `.ralph/context/coding-style.md` - 编码规范完整
- [ ] `.ralph/context/decisions.md` - 10个ADR完整
- [ ] `.ralph/context/dependencies.md` - 依赖说明完整

### 5.3 模块文档

- [ ] `.ralph/context/modules/brain.md` (~800行)
- [ ] `.ralph/context/modules/dealer.md` (~600行)
- [ ] `.ralph/context/modules/worker.md` (~650行)

### 5.4 Phase完成报告

- [ ] `PHASE5_COMPLETION.md` - Worker v3
- [ ] `PHASE8_COMPLETION.md` - Context Engineering
- [ ] `PHASE10_COMPLETION.md` - 文档和部署

---

## 🔒 Step 6: 安全检查

### 6.1 敏感信息

- [ ] `.janus/config.json` 中的API Key不泄露
- [ ] 不提交 `.janus/config.json` 到Git
- [ ] `.gitignore` 包含 `.janus/config.json`
- [ ] `.gitignore` 包含 `.ralph/memories/`

**验证 .gitignore**:
```bash
cat .gitignore | grep -E "(config.json|memories)"
```

### 6.2 文件权限

```bash
# Linux/Mac
ls -l .janus/config.json
ls -l .ralph/tools/config.json
```

- [ ] 配置文件权限合理（避免全局可读）

---

## 🚀 Step 7: 性能验证

### 7.1 Brain性能

```bash
time python brain_v3.py "性能测试任务"
```

- [ ] Brain运行时间 < 5秒
- [ ] 内存占用 < 100MB

### 7.2 Dealer性能

```bash
time python dealer_v3.py
```

- [ ] Dealer运行时间 < 3秒
- [ ] 内存占用 < 50MB

### 7.3 双记忆检索性能

```bash
python -c "
import sys, time
sys.path.append('.ralph/tools')
from memory_integrator import get_memory_integrator
mi = get_memory_integrator()
start = time.time()
mi.retrieve_combined('测试查询', top_k=5)
print(f'检索时间: {time.time()-start:.3f}秒')
"
```

- [ ] 检索时间 < 1秒

---

## ✅ Step 8: 最终验证

### 8.1 端到端流程测试

**完整流程**:
```bash
# 1. Brain规划
python brain_v3.py "端到端测试：实现简单的Hello World API"

# 2. Dealer生成指令
python dealer_v3.py

# 3. 检查输出
ls .janus/project_state.json
ls .ralph/specs/*.md
cat .ralph/current_instruction.txt 2>/dev/null || echo "指令在剪贴板"
```

- [ ] Brain生成蓝图成功
- [ ] Dealer生成指令成功
- [ ] 指令包含完整8个维度

### 8.2 文档可访问性

```bash
# 测试所有文档都可读取
cat README.md | head -5
cat .ralph/context/architecture.md | head -5
cat .ralph/context/decisions.md | head -5
cat .ralph/context/modules/brain.md | head -5
```

- [ ] 所有核心文档可读取
- [ ] 文档格式正确（Markdown）
- [ ] 文档内容完整

### 8.3 系统状态检查

```bash
python .ralph/scripts/integration_test.py 2>&1 | tail -20
```

**最终输出应包含**:
```
🎉 所有测试通过！系统集成完整，可以投入使用！
```

- [ ] 最终状态：生产就绪 ✅

---

## 📊 部署成功指标

### 关键指标

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 依赖安装成功率 | 100% | ___ | ☐ |
| 集成测试通过率 | 100% | ___ | ☐ |
| Brain功能正常 | ✅ | ___ | ☐ |
| Dealer功能正常 | ✅ | ___ | ☐ |
| 文档完整性 | 100% | ___ | ☐ |
| 性能达标 | ✅ | ___ | ☐ |

### 完成标准

- [ ] ✅ 所有核心依赖安装成功
- [ ] ✅ 所有目录和文件就位
- [ ] ✅ 所有配置文件正确
- [ ] ✅ 集成测试100%通过
- [ ] ✅ Brain/Dealer功能测试通过
- [ ] ✅ 文档完整且可访问
- [ ] ✅ 性能指标达标
- [ ] ✅ 安全检查通过

---

## 🐛 常见部署问题

### 问题1: 依赖安装失败

**症状**: `pip install pyperclip` 失败

**解决**:
```bash
# 更新pip
python -m pip install --upgrade pip

# 重试安装
pip install pyperclip

# 或使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyperclip
```

### 问题2: 目录权限问题

**症状**: `Permission denied` 写入文件

**解决**:
```bash
# 检查权限
ls -ld .janus .ralph

# 修改权限（Linux/Mac）
chmod -R u+rw .janus .ralph

# Windows: 在文件夹属性中调整权限
```

### 问题3: 模块导入失败

**症状**: `ImportError: No module named ...`

**解决**:
```bash
# 确认文件存在
ls .ralph/tools/tools_manager.py

# 检查Python路径
python -c "import sys; print(sys.path)"

# 使用绝对路径导入
python -c "import sys; sys.path.append('.ralph/tools'); from tools_manager import get_tools_manager"
```

### 问题4: 测试失败

**症状**: 集成测试部分失败

**解决**:
```bash
# 查看详细错误
python .ralph/scripts/integration_test.py 2>&1 | tee test.log

# 针对性修复
cat test.log | grep "❌"

# 单独测试失败模块
python -c "from brain_v3 import BrainV3; b = BrainV3(); print('OK')"
```

---

## 📚 部署后操作

### 建议步骤

1. **熟悉系统**
   - 阅读 `README.md`
   - 阅读 `QUICK_START_V3.md`
   - 查看 `.ralph/context/architecture.md`

2. **定制配置**
   - 根据项目更新 `.ralph/context/project-info.md`
   - 调整 `.ralph/tools/config.json` 工具配置
   - 定制 `.ralph/context/coding-style.md` 编码规范

3. **实战演练**
   - 规划一个简单任务测试Brain v3
   - 生成指令测试Dealer v3
   - 使用Worker v3执行任务
   - 体验质量自检流程

4. **持续优化**
   - 定期更新Context Engineering文档
   - 积累双记忆系统经验
   - 调整工具配置优化体验
   - 添加新的ADR记录决策

---

## ✨ 部署完成

**恭喜！双脑Ralph系统v3.0已成功部署！**

### 系统状态

- ✅ 核心依赖已安装
- ✅ 目录结构完整
- ✅ 配置文件就绪
- ✅ 集成测试通过
- ✅ 功能验证成功
- ✅ 文档体系完整
- ✅ 性能达标
- ✅ 生产就绪

### 下一步

1. 使用Brain v3规划第一个任务
2. 使用Dealer v3生成执行指令
3. 体验Worker v3的质量保证
4. 查看系统自动生成的文档
5. 享受高质量的AI开发体验

---

**部署版本**: v3.0.0
**部署日期**: 2026-02-11
**部署状态**: ✅ 生产就绪

🚀 **开始享受智能、高质量的AI驱动开发！**
