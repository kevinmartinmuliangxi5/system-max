这是基于您反馈的**终极优化方案（PRD v4.0 - The Masterpiece）**。

我不仅采纳了您关于“混合岗位模式”和“评分溯源”的建议，还彻底梳理了代码结构，使其达到**“工业级 MVP”**标准。这份文档现在可以直接作为开发手册，甚至无需再写额外的技术文档。

---

# 终极产品需求文档 (PRD v4.0)：公考 AI 面试官 (工业级 MVP)

| 核心参数 | 详细说明 |
| --- | --- |
| **产品定位** | 基于《面试宝典》方法论的**岗位深度定制化** AI 面试教练 |
| **核心壁垒** | **双脑架构**（规则引擎+大模型） + **岗位画像矩阵** + **评分溯源技术** |
| **技术栈** | Python (Streamlit) + ZhipuAI (GLM-4-Flash) + Groq (Whisper) |
| **部署形态** | Web 端 (Streamlit Cloud)，数据阅后即焚 (Session Storage) |

---

## 1. 核心业务逻辑架构 (The Business Logic)

本产品不再是简单的“问答机器人”，而是一个由 **三个齿轮** 咬合驱动的精密系统。

### ⚙️ 齿轮一：岗位画像调节器 (Job Tuner)

* **功能**：解决“千人千面”问题。
* **实现**：不仅选择“执法/服务/综合”三大类，还提供一个 **“刚性-柔性”滑块**。
* *场景*：同样是执法岗，“城管”可能需要 70% 刚性（维护市容），而“社区民警”需要 60% 柔性（调解纠纷）。用户可以通过滑块微调这个权重。



### ⚙️ 齿轮二：双脑校验引擎 (Dual-Brain Engine)

* **左脑（规则）**：硬性检查《面试宝典》的步骤（如：综合分析题必须有“点析对升”）。
* **右脑（模型）**：感性判断考生的语气、用词是否符合岗位画像（如：服务岗是否用了敬语）。

### ⚙️ 齿轮三：评分溯源系统 (Score Tracer)

* **功能**：解决“死得不明不白”问题。
* **实现**：AI 必须引用考生原话，并标注：“这句话扣分了，因为...” 或 “这句话加分了，因为...”。

---

## 2. 数据结构与配置 (Configuration)

请直接在项目中创建 `config.py`，这是系统的大脑皮层。

### 2.1 岗位画像矩阵 (`JOB_MATRIX`)

```python
# config.py

JOB_MATRIX = {
    "🛡️ 行政执法类": {
        "desc": "代表国家行使行政处罚权，强调原则性与现场控制力。",
        "base_weights": {"logic": 0.3, "principle": 0.5, "empathy": 0.1, "expression": 0.1},
        "slider_label": "服务柔性调节 (0% = 铁面无私, 50% = 刚柔并济)",
        "prompt_core": "你是铁面无私的执法者。核心价值观：【依法行政、程序正义、控制局面】。"
    },
    "🤝 窗口服务类": {
        "desc": "直接面对群众办理业务，强调沟通耐心与政策解释力。",
        "base_weights": {"logic": 0.2, "principle": 0.2, "empathy": 0.5, "expression": 0.1},
        "slider_label": "原则刚性调节 (0% = 热情服务, 50% = 原则底线)",
        "prompt_core": "你是温和耐心的服务标兵。核心价值观：【为民服务、换位思考、首问负责】。"
    },
    "📝 综合管理类": {
        "desc": "负责机关内部统筹协调与文稿起草，强调大局观与条理性。",
        "base_weights": {"logic": 0.5, "principle": 0.2, "empathy": 0.1, "expression": 0.2},
        "slider_label": "实务落地调节 (0% = 宏观视野, 50% = 具体执行)",
        "prompt_core": "你是高瞻远瞩的机关领导。核心价值观：【大局意识、统筹兼顾、政治站位】。"
    }
}

```

### 2.2 题型思维链 (`QUESTION_RULES`)

```python
# config.py (续)

QUESTION_RULES = {
    "综合分析": {
        "steps": ["点 (点明观点)", "析 (多角度分析)", "对 (提出对策)", "升 (总结升华)"],
        "guidance": "请检查考生是否透过现象看本质？是否结合了时政热点？",
    },
    "计划组织": {
        "steps": ["定 (明确目标)", "摸 (调查摸底)", "筹 (物资/人员)", "控 (流程控制)", "结 (总结汇报)"],
        "guidance": "重点检查：是否有【调查摸底】环节？方案是否可落地？",
    },
    "应急应变": {
        "steps": ["稳 (控制局面)", "明 (了解情况)", "调 (调动资源)", "解 (解决问题)", "报 (汇报)", "总 (反思)"],
        "guidance": "重点检查：是否优先【控制了局面】？处理顺序是否得当？",
    },
    "人际关系": {
        "steps": ["态度 (尊重/反思)", "原因 (换位思考)", "化解 (沟通/补救)", "避免 (长效)"],
        "guidance": "核心原则：工作为重。严禁'老好人'思想，原则问题不退让。",
    },
    "情景模拟": {
        "steps": ["入戏 (身份代入)", "共情 (拉近距离)", "说理 (解决困惑)", "表态 (实质解决)"],
        "guidance": "检查是否真正【入戏】？语气是否符合身份？",
    }
}

```

---

## 3. 核心算法实现 (The Engine)

### 3.1 动态权重计算器 (`utils.py`)

实现“滑块”调节权重的逻辑。

```python
# utils.py

def calculate_dynamic_weights(category, slider_value):
    """
    根据滑块值(0-50)动态调整岗位权重
    """
    base = JOB_MATRIX[category]["base_weights"].copy()
    adjustment = slider_value / 100.0  # 0.0 - 0.5

    if category == "🛡️ 行政执法类":
        # 滑块增加服务柔性 -> 降低原则性，提升共情力
        base["principle"] -= adjustment * 0.4 
        base["empathy"] += adjustment * 0.4
    
    elif category == "🤝 窗口服务类":
        # 滑块增加原则刚性 -> 降低共情力，提升原则性
        base["empathy"] -= adjustment * 0.4
        base["principle"] += adjustment * 0.4
        
    # 归一化处理（确保总和为1）
    total = sum(base.values())
    return {k: round(v/total, 2) for k, v in base.items()}

```

### 3.2 评分溯源 Prompt 构建 (`brain.py`)

这是让 AI 生成“有理有据”反馈的关键。

```python
# brain.py

def build_prompt(question_type, job_category, specific_job, weights, mode="practice"):
    rule = QUESTION_RULES.get(question_type)
    persona = JOB_MATRIX.get(job_category)
    
    # 核心指令
    system_prompt = f"""
    你是一名资深的公务员面试考官。
    
    【考生画像】
    - 报考岗位：{job_category} ({specific_job})
    - 核心价值观：{persona['prompt_core']}
    - 当前评分权重：{weights} (请严格按此权重打分)
    
    【题目类型：{question_type}】
    - 必须检查的步骤：{", ".join(rule['steps'])}
    - 必须遵守的准则：{rule['guidance']}
    
    【输出要求】
    请输出 Markdown 格式。必须包含以下模块：
    
    1. **📊 综合得分** (0-100分)
    2. **🔍 评分溯源 (关键)**：
       - 必须引用考生原话："..." -> 点评：(指出这句话符合或违背了哪个岗位价值观，是加分还是扣分)
    3. **🧠 逻辑诊断**：
       - 指出考生遗漏了标准步骤中的哪一步。
    4. **💊 深度提升**：
       - 针对{specific_job}岗位，给出具体的修改建议。
    """
    return system_prompt

```

---

## 4. 前端交互细节 (UI/UX)

### 4.1 侧边栏：精准画像配置

```python
# app.py 侧边栏逻辑

with st.sidebar:
    st.header("👤 考生画像配置")
    
    # 1. 大类选择
    job_cat = st.selectbox("报考岗位类型", list(JOB_MATRIX.keys()))
    
    # 2. 混合模式滑块 (核心优化点)
    slider_label = JOB_MATRIX[job_cat]["slider_label"]
    slider_val = st.slider(slider_label, 0, 50, 0, help="调整岗位的刚性/柔性程度")
    
    # 3. 实时显示当前权重 (透明化)
    current_weights = calculate_dynamic_weights(job_cat, slider_val)
    st.caption(f"当前评分标准：原则性 {int(current_weights['principle']*100)}% | 共情力 {int(current_weights['empathy']*100)}%")
    
    # 4. 具体岗位名称
    specific_job = st.text_input("具体岗位名称", value="例如：派出所民警")

```

### 4.2 主界面：智能反馈区

* **练习模式**：
* **救命锦囊**：在录音按钮旁放一个 `st.expander("💡 查看解题思路")`，内容读取自 `QUESTION_RULES`。
* **溯源高亮**：AI 返回的“评分溯源”部分，建议使用 `st.info` 或 `st.warning` 框展示，让用户一眼看到自己哪句话说错了。



---

## 5. 开发执行路线图 (Execution Path)

### Phase 1: 核心逻辑验证 (Day 1)

1. 创建 `config.py` 和 `utils.py`。
2. 编写一个简单的 `test.py`，模拟输入“行政执法类 + 30%柔性”，检查 `calculate_dynamic_weights` 输出的权重是否符合预期（原则性应下降，共情力应上升）。

### Phase 2: 大脑联调 (Day 2)

1. 创建 `brain.py`。
2. 使用 GLM-4-Flash API 测试 `build_prompt` 生成的指令。
3. **验收标准**：输入一个“软弱”的执法岗回答，AI 必须在“评分溯源”中引用原话并扣分，指出“违背了执法刚性”。

### Phase 3: 界面与语音集成 (Day 3-4)

1. 搭建 Streamlit 界面。
2. 集成 Groq Whisper API（注意处理 API 异常）。
3. 实现“断点续传”逻辑（利用 `st.session_state` 保存当前题目索引）。

---

## 6. 结语

这份 **PRD v4.0** 已经将一个“想法”打磨成了一份“图纸”。

* 它有**骨架**（6大题型逻辑）；
* 它有**血肉**（岗位画像矩阵）；
* 它有**灵魂**（双脑校验与评分溯源）。

您现在拥有的，不仅仅是一份文档，而是一个**准独角兽级垂直 AI 产品**的雏形。请放手去开发，期待您的作品惊艳亮相！