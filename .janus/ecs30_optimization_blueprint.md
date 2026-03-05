# ECS 3.0 优化升级蓝图

**生成日期**: 2025-02-06
**基于评估**: report1.md (ECS 2.0 深度专业评估报告)
**当前评分**: 78/100
**目标评分**: 90/100
**预计周期**: 9-10周

---

## 执行摘要

本蓝图基于对ECS 2.0的全面评估（11维度严苛分析），识别出**3个严重问题**和**5个重要改进方向**。优化工作分为**5个阶段**，优先解决架构级缺陷，逐步达到生产级标准。

### 核心问题优先级

| 优先级 | 问题 | 影响 | 预期收益 |
|--------|------|------|----------|
| **P0** | 串行执行架构 | 效率损失80% | 5×性能提升 |
| **P0** | 无记忆系统 | 无法自我进化 | 系统可学习 |
| **P0** | 语义相似度过时 | 准确性低 | 30%准确度提升 |
| **P1** | 无实时可视化 | 用户体验差 | 可监控、可调试 |
| **P1** | 无干预能力 | 无法人机协作 | 支持中途调整 |

---

## 阶段一：架构重构（2周）🔴 P0

### 目标
将串行执行架构重构为并行执行，实现5倍效率提升。

### 任务清单

#### 1.1 并行讨论阶段重构
**文件**: `ecs/collaboration.py`

**当前代码（串行）**:
```python
async def _discuss_phase(self, task: str):
    for round_num in range(1, self.config.max_rounds + 1):
        for agent in self.agents:
            response = await agent.discuss(...)
            await asyncio.sleep(0.5)  # 串行等待！
```

**目标代码（并行）**:
```python
async def _discuss_phase(self, task: str):
    """并行讨论阶段 - 所有Agent同时发言"""
    for round_num in range(1, self.config.max_rounds + 1):
        previous_messages = self.discussion_history.get_recent(limit=20)

        # 创建所有Agent的任务
        tasks = [
            agent.discuss(
                task=task,
                env_context=self.environment_context,
                peer_messages=previous_messages,
                round_num=round_num,
                temperature=self._get_discuss_temperature(round_num)
            )
            for agent in self.agents
        ]

        # 使用asyncio.gather并行执行
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理响应
        for agent, response in zip(self.agents, responses):
            if isinstance(response, Exception):
                self.logger.error(f"Agent {agent.agent_id} 失败: {response}")
                continue

            # 创建观点和消息
            viewpoint = create_viewpoint(...)
            message = create_message(...)
            self.viewpoint_space.add_viewpoint(viewpoint)
            self.discussion_history.add_message(message)

        # 检查共识
        if self.config.early_stop:
            consensus = self.viewpoint_space.get_consensus()
            if consensus >= self.config.consensus_threshold:
                break
```

**验证方式**: 5个Agent×3轮从75秒降至15秒

#### 1.2 并行Sense阶段
**文件**: `ecs/collaboration.py`

同样使用`asyncio.gather`并行执行所有Agent的sense操作。

#### 1.3 添加重试机制
**文件**: `ecs/core/agent.py` 或新建 `ecs/utils/retry.py`

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def _call_llm_with_retry(self, messages: List[Dict]) -> str:
    """带重试的LLM调用"""
    return await self._call_llm(messages)
```

**依赖更新**: 在`requirements.txt`中添加`tenacity>=8.2.0`

#### 1.4 修复导入问题
**文件**: `ecs/__init__.py:24-25`

将`from .emergence import EmergenceType, SystemPhase`改为从正确的模块导入。

---

## 阶段二：记忆系统实现（3周）🔴 P0

### 目标
实现三层记忆系统，使系统能够跨任务学习和进化。

### 任务清单

#### 2.1 创建记忆模块架构
**新建文件**:
```
ecs/memory/
├── __init__.py
├── base.py          # 基础接口
├── working.py       # 工作记忆
├── episodic.py      # 情景记忆（向量DB）
├── semantic.py      # 语义记忆（向量DB）
└── manager.py       # 记忆管理器
```

#### 2.2 工作记忆实现
**文件**: `ecs/memory/working.py`

```python
from typing import List, Dict, Any
from collections import deque

class WorkingMemory:
    """工作记忆 - 存储当前会话的临时信息"""

    def __init__(self, max_items: int = 100):
        self.max_items = max_items
        self.messages = deque(maxlen=max_items)
        self.context = {}

    def add_message(self, message: Dict[str, Any]):
        """添加消息"""
        self.messages.append(message)

    def get_recent(self, n: int = 10) -> List[Dict]:
        """获取最近n条消息"""
        return list(self.messages)[-n:]

    def set_context(self, key: str, value: Any):
        """设置上下文"""
        self.context[key] = value

    def get_context(self, key: str, default=None) -> Any:
        """获取上下文"""
        return self.context.get(key, default)

    def clear(self):
        """清空工作记忆"""
        self.messages.clear()
        self.context.clear()
```

#### 2.3 情景记忆实现
**文件**: `ecs/memory/episodic.py`

```python
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path

class EpisodicMemory:
    """情景记忆 - 存储具体的事件和经历"""

    def __init__(self, storage_path: str = "./data/episodic"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.episodes = []

    def add_episode(
        self,
        task: str,
        config: Dict[str, Any],
        result: Dict[str, Any],
        emergence_score: float
    ):
        """添加一个情景（一次完整的协作）"""
        episode = {
            "id": f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "config": config,
            "result": result,
            "emergence_score": emergence_score,
            "task_embedding": self._encode_task(task)  # 需要嵌入模型
        }
        self.episodes.append(episode)
        self._save_episode(episode)

    def _encode_task(self, task: str) -> np.ndarray:
        """编码任务（后续用sentence-transformers）"""
        # 临时用简单的hash，阶段三替换
        return np.array(hash(task) % 10000, dtype=np.float32)

    def _save_episode(self, episode: Dict):
        """保存情景到文件"""
        file_path = self.storage_path / f"{episode['id']}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(episode, f, ensure_ascii=False, indent=2)

    def find_similar_episodes(self, task: str, top_k: int = 3) -> List[Dict]:
        """查找相似的历史情景"""
        # 简化版本：基于关键词匹配
        # 阶段三替换为向量检索
        task_words = set(task.lower().split())
        scored_episodes = []

        for ep in self.episodes:
            ep_words = set(ep['task'].lower().split())
            overlap = len(task_words & ep_words)
            scored_episodes.append((ep, overlap))

        scored_episodes.sort(key=lambda x: x[1], reverse=True)
        return [ep for ep, _ in scored_episodes[:top_k]]

    def get_best_configs(self, task: str) -> List[Dict]:
        """获取针对相似任务的最佳配置"""
        similar = self.find_similar_episodes(task, top_k=5)
        # 按涌现分数排序
        similar.sort(key=lambda ep: ep['emergence_score'], reverse=True)
        return [ep['config'] for ep in similar[:3]]
```

#### 2.4 语义记忆实现
**文件**: `ecs/memory/semantic.py`

```python
from typing import Dict, List, Any
import json
from pathlib import Path

class SemanticMemory:
    """语义记忆 - 存储抽象的知识和模式"""

    def __init__(self, storage_path: str = "./data/semantic"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.patterns = {}
        self._load_patterns()

    def save_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]):
        """保存模式"""
        self.patterns[pattern_name] = {
            **pattern_data,
            "usage_count": self.patterns.get(pattern_name, {}).get("usage_count", 0) + 1
        }
        self._save_patterns()

    def get_pattern(self, pattern_name: str) -> Optional[Dict]:
        """获取模式"""
        return self.patterns.get(pattern_name)

    def _load_patterns(self):
        """加载模式"""
        file_path = self.storage_path / "patterns.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)

    def _save_patterns(self):
        """保存模式"""
        file_path = self.storage_path / "patterns.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)
```

#### 2.5 记忆管理器
**文件**: `ecs/memory/manager.py`

```python
from .working import WorkingMemory
from .episodic import EpisodicMemory
from .semantic import SemanticMemory

class MemoryManager:
    """记忆管理器 - 统一管理三层记忆"""

    def __init__(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def save_collaboration_experience(
        self,
        task: str,
        config: Dict,
        result: Dict,
        emergence_score: float
    ):
        """保存协作经验"""
        self.episodic.add_episode(task, config, result, emergence_score)

        # 如果涌现分数高，保存为成功模式
        if emergence_score > 0.8:
            self.semantic.save_pattern(
                f"success_pattern_{hash(task)}",
                {"task": task, "config": config, "score": emergence_score}
            )

    def recommend_config(self, task: str) -> Dict:
        """基于历史推荐配置"""
        best_configs = self.episodic.get_best_configs(task)
        if best_configs:
            # 返回最佳配置
            return best_configs[0]
        return None

    def cleanup_session(self):
        """清理会话（保留长期记忆）"""
        self.working.clear()
```

#### 2.6 集成到协作引擎
**文件**: `ecs/collaboration.py`

在`CollaborationEngine`中添加记忆支持：

```python
from .memory.manager import MemoryManager

class CollaborationEngine:
    def __init__(self, ...):
        # ... 现有初始化代码
        self.memory = MemoryManager()

    async def collaborate(self, task: str, roles: List[str] = None):
        # 执行前：检查历史配置
        recommended_config = self.memory.recommend_config(task)
        if recommended_config:
            self.logger.info(f"使用历史最佳配置: {recommended_config}")

        # ... 执行协作

        # 执行后：保存经验
        self.memory.save_collaboration_experience(
            task=task,
            config=self.config.__dict__,
            result=result.to_dict(),
            emergence_score=result.emergence_report.metrics.emergence_score
        )

        return result
```

---

## 阶段三：语义相似度升级（1周）🔴 P0

### 目标
将bag-of-words相似度计算升级为基于sentence-transformers的语义相似度。

### 任务清单

#### 3.1 添加依赖
**文件**: `requirements.txt`

```
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
```

#### 3.2 创建语义嵌入模块
**新建文件**: `ecs/core/semantic.py`

```python
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
from functools import lru_cache
from sklearn.metrics.pairwise import cosine_similarity

class SemanticEmbedder:
    """语义嵌入器 - 使用sentence-transformers"""

    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """获取单例模型"""
        if cls._model is None:
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._model

    @classmethod
    @lru_cache(maxsize=1000)
    def encode(cls, text: str) -> np.ndarray:
        """编码文本为向量（带缓存）"""
        model = cls.get_model()
        return model.encode(text)

    @classmethod
    def similarity(cls, text1: str, text2: str) -> float:
        """计算两段文本的语义相似度"""
        emb1 = cls.encode(text1).reshape(1, -1)
        emb2 = cls.encode(text2).reshape(1, -1)
        return float(cosine_similarity(emb1, emb2)[0][0])

    @classmethod
    def similarities(cls, text: str, texts: List[str]) -> List[float]:
        """计算一段文本与多段文本的相似度"""
        emb = cls.encode(text).reshape(1, -1)
        embs = np.array([cls.encode(t) for t in texts])
        sims = cosine_similarity(emb, embs)[0]
        return [float(s) for s in sims]

    @classmethod
    def pairwise_similarities(cls, texts: List[str]) -> np.ndarray:
        """计算多段文本的两两相似度矩阵"""
        embs = np.array([cls.encode(t) for t in texts])
        return cosine_similarity(embs)
```

#### 3.3 更新Viewpoint相似度计算
**文件**: `ecs/core/viewpoint.py`

```python
from .semantic import SemanticEmbedder

class Viewpoint:
    # ... 现有代码

    def similarity_to(self, other: 'Viewpoint') -> float:
        """计算与另一个观点的相似度（使用语义嵌入）"""
        return SemanticEmbedder.similarity(self.content, other.content)
```

#### 3.4 更新情景记忆的检索
**文件**: `ecs/memory/episodic.py`

```python
from ..core.semantic import SemanticEmbedder

class EpisodicMemory:
    # ... 现有代码

    def _encode_task(self, task: str) -> np.ndarray:
        """编码任务（使用语义嵌入）"""
        return SemanticEmbedder.encode(task)

    def find_similar_episodes(self, task: str, top_k: int = 3) -> List[Dict]:
        """查找相似的历史情景（使用向量检索）"""
        if not self.episodes:
            return []

        task_emb = self._encode_task(task)
        similarities = []

        for ep in self.episodes:
            sim = float(cosine_similarity(
                task_emb.reshape(1, -1),
                ep['task_embedding'].reshape(1, -1)
            )[0][0])
            similarities.append((ep, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return [ep for ep, _ in similarities[:top_k]]
```

---

## 阶段四：可视化系统（2周）🟡 P1

### 目标
实现基于Streamlit的实时可视化仪表盘，支持涌现指标监控、Agent交互网络图、讨论回放。

### 任务清单

#### 4.1 添加可视化依赖
**文件**: `requirements.txt`

```
streamlit>=1.28.0
plotly>=5.17.0
networkx>=3.0
```

#### 4.2 创建可视化模块
**新建文件**: `ecs/visualization/`

```
ecs/visualization/
├── __init__.py
├── metrics.py      # 指标可视化
├── network.py      # Agent网络图
└── replay.py       # 讨论回放
```

#### 4.3 实时指标图表
**文件**: `ecs/visualization/metrics.py`

```python
import plotly.graph_objects as go
from typing import List, Dict
from ..emergence import EmergenceReport

def create_emergence_dashboard(reports: List[EmergenceReport]) -> go.Figure:
    """创建涌现指标仪表盘"""
    rounds = list(range(1, len(reports) + 1))

    fig = go.Figure()

    # 添加各指标曲线
    metrics_list = ['diversity', 'consensus', 'novelty', 'integration', 'synergy', 'emergence_score']
    colors = ['blue', 'green', 'orange', 'purple', 'red', 'black']

    for metric, color in zip(metrics_list, colors):
        values = [getattr(r.metrics, metric) for r in reports]
        fig.add_trace(go.Scatter(
            x=rounds,
            y=values,
            mode='lines+markers',
            name=metric,
            line=dict(color=color)
        ))

    fig.update_layout(
        title="涌现指标实时监控",
        xaxis_title="讨论轮次",
        yaxis_title="指标值",
        hovermode='x unified',
        template='plotly_white'
    )

    return fig

def create_phase_timeline(reports: List[EmergenceReport]) -> go.Figure:
    """创建系统阶段时间线"""
    phases = [r.system_phase.value for r in reports]
    rounds = list(range(1, len(reports) + 1))

    # 阶段到数字的映射
    phase_map = {
        '探索期': 1,
        '辩论期': 2,
        '收敛期': 3,
        '共识期': 4,
        '停滞期': 0
    }

    values = [phase_map.get(p, 2) for p in phases]

    fig = go.Figure()

    # 添加阶段色块
    for i, (phase, val) in enumerate(zip(phases, values)):
        fig.add_trace(go.Scatter(
            x=[i+1, i+2],
            y=[val, val],
            mode='lines',
            line=dict(width=20),
            name=phase,
            showlegend=i == 0
        ))

    fig.update_layout(
        title="系统阶段演化",
        xaxis_title="讨论轮次",
        yaxis_title="系统阶段",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4],
            ticktext=['停滞期', '探索期', '辩论期', '收敛期', '共识期']
        )
    )

    return fig
```

#### 4.4 Agent交互网络图
**文件**: `ecs/visualization/network.py`

```python
import networkx as nx
import plotly.graph_objects as go
from typing import List
from ..core.viewpoint import ViewpointSpace

def create_agent_interaction_network(viewpoint_space: ViewpointSpace) -> go.Figure:
    """创建Agent交互网络图"""
    viewpoints = viewpoint_space.get_all_viewpoints()

    # 创建网络
    G = nx.Graph()

    # 添加节点（Agent）
    agents = list(set(vp.agent_id for vp in viewpoints))
    for agent in agents:
        G.add_node(agent, size=10)

    # 添加边（基于相似度）
    for i, vp1 in enumerate(viewpoints):
        for vp2 in viewpoints[i+1:]:
            if vp1.agent_id != vp2.agent_id:
                sim = vp1.similarity_to(vp2)
                if sim > 0.3:  # 只显示较强连接
                    G.add_edge(vp1.agent_id, vp2.agent_id, weight=sim)

    # 计算布局
    pos = nx.spring_layout(G, weight='weight', seed=42)

    # 提取边和节点信息
    edge_x = []
    edge_y = []
    edge_width = []

    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_width.append(edge[2].get('weight', 0.5) * 5)

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = list(G.nodes())

    # 创建图形
    fig = go.Figure()

    # 添加边
    for i in range(0, len(edge_x), 3):
        fig.add_trace(go.Scatter(
            x=edge_x[i:i+3],
            y=edge_y[i:i+3],
            mode='lines',
            line=dict(width=edge_width[i//3], color='gray'),
            showlegend=False,
            hoverinfo='none'
        ))

    # 添加节点
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(size=20, color='lightblue'),
        text=node_text,
        textposition='middle center',
        name='Agents'
    ))

    fig.update_layout(
        title="Agent交互网络",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    return fig
```

#### 4.5 Streamlit仪表盘
**新建文件**: `ecs/ui/dashboard.py`

```python
import streamlit as st
from ..visualization.metrics import create_emergence_dashboard, create_phase_timeline
from ..visualization.network import create_agent_interaction_network
from ... import ECSCoordinator, ECSConfig

st.set_page_config(page_title="ECS 3.0 仪表盘", layout="wide")

st.title("🧠 ECS 3.0 多Agent协作系统")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")

    task = st.text_area("任务描述", height=100)
    agent_count = st.slider("Agent数量", 2, 10, 5)
    max_rounds = st.slider("讨论轮次", 1, 7, 3)
    threshold = st.slider("涌现阈值", 0.5, 0.9, 0.7)

    run_button = st.button("🚀 开始协作")

# 主区域
if run_button:
    with st.spinner("协作进行中..."):
        config = ECSConfig()
        coordinator = ECSCoordinator(config)
        result = coordinator.collaborate(
            task=task,
            agent_count=agent_count,
            max_rounds=max_rounds,
            emergence_threshold=threshold
        )

    # 显示结果
    st.success("协作完成！")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("涌现强度", f"{result.emergence_report.metrics.emergence_score:.2f}")
    with col2:
        st.metric("协同度", f"{result.emergence_report.metrics.synergy:.2f}")
    with col3:
        st.metric("系统阶段", result.emergence_report.system_phase.value)

    # 指标图表
    st.subheader("📊 涌现指标")
    # 这里需要从协作历史中提取各轮次报告
    # fig = create_emergence_dashboard(reports)
    # st.plotly_chart(fig, use_container_width=True)

    # 网络图
    st.subheader("🕸️ Agent交互网络")
    # fig = create_agent_interaction_network(result.viewpoint_space)
    # st.plotly_chart(fig, use_container_width=True)

    # 解决方案
    st.subheader("💡 解决方案")
    st.markdown(result.solution)
```

#### 4.6 启动脚本
**新建文件**: `ecs-ui.py`

```python
"""ECS Web UI 启动脚本"""
import streamlit.cli
from ecs.ui.dashboard import main

if __name__ == "__main__":
    streamlit.cli.main()
```

---

## 阶段五：干预能力实现（1周）🟡 P1

### 目标
实现中途干预能力，支持检查点暂停、人工输入、任务修改。

### 任务清单

#### 5.1 创建干预模块
**新建文件**: `ecs/intervention/`

```
ecs/intervention/
├── __init__.py
├── checkpoint.py   # 检查点管理
├── interrupt.py    # 中断处理
└── handlers.py     # 交互处理器
```

#### 5.2 检查点管理
**文件**: `ecs/intervention/checkpoint.py`

```python
import pickle
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

class CheckpointManager:
    """检查点管理器 - 支持断点续传"""

    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        session_id: str,
        round_num: int,
        state: Dict[str, Any]
    ):
        """保存检查点"""
        checkpoint = {
            "session_id": session_id,
            "round_num": round_num,
            "timestamp": datetime.now().isoformat(),
            "state": state
        }

        file_path = self.checkpoint_dir / f"{session_id}_round{round_num}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(checkpoint, f)

    def load_checkpoint(self, session_id: str, round_num: int) -> Optional[Dict]:
        """加载检查点"""
        file_path = self.checkpoint_dir / f"{session_id}_round{round_num}.pkl"
        if file_path.exists():
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        return None

    def list_checkpoints(self, session_id: str) -> list:
        """列出会话的所有检查点"""
        checkpoints = []
        for file in self.checkpoint_dir.glob(f"{session_id}_*.pkl"):
            checkpoints.append({
                "file": file,
                "round": int(file.stem.split('round')[1])
            })
        return sorted(checkpoints, key=lambda x: x['round'])
```

#### 5.3 中断处理器
**文件**: `ecs/intervention/interrupt.py`

```python
import signal
import sys
from typing import Callable, Optional

class InterruptHandler:
    """中断处理器 - 支持Ctrl+C优雅中断"""

    def __init__(self):
        self.interrupted = False
        self.action_callback: Optional[Callable] = None

    def set_action_callback(self, callback: Callable):
        """设置中断后的回调"""
        self.action_callback = callback

    def _handle_signal(self, signum, frame):
        """处理信号"""
        self.interrupted = True
        print("\n\n⚠️ 检测到中断信号")
        print("可用操作:")
        print("  c - 继续执行")
        print("  m - 修改任务")
        print("  v - 查看当前状态")
        print("  q - 退出并保存")

        if self.action_callback:
            self.action_callback()

    def register(self):
        """注册信号处理器"""
        signal.signal(signal.SIGINT, self._handle_signal)
        # Windows不支持SIGTERM
        if sys.platform != 'win32':
            signal.signal(signal.SIGTERM, self._handle_signal)

    def reset(self):
        """重置中断状态"""
        self.interrupted = False
```

#### 5.4 交互处理器
**文件**: `ecs/intervention/handlers.py`

```python
from typing import Dict, Any, Optional
from .checkpoint import CheckpointManager

class InterventionHandler:
    """干预处理器"""

    def __init__(self):
        self.checkpoint_manager = CheckpointManager()
        self.session_id: Optional[str] = None
        self.current_round = 0
        self.intervention_points = []  # 需要干预的轮次

    def set_intervention_points(self, rounds: list):
        """设置干预点（在这些轮次后暂停）"""
        self.intervention_points = rounds

    def should_intervene(self, round_num: int) -> bool:
        """检查是否需要干预"""
        return round_num in self.intervention_points

    def handle_intervention(
        self,
        session_id: str,
        round_num: int,
        state: Dict[str, Any]
    ) -> Optional[str]:
        """处理干预，返回用户选择的操作"""
        self.session_id = session_id
        self.current_round = round_num

        # 先保存检查点
        self.checkpoint_manager.save_checkpoint(
            session_id, round_num, state
        )

        print(f"\n{'='*60}")
        print(f"🔔 检查点: 第{round_num}轮完成")
        print(f"{'='*60}")
        print(f"涌现强度: {state.get('emergence_score', 0):.2f}")
        print(f"共识度: {state.get('consensus', 0):.2f}")

        print("\n可用操作:")
        print("  1. 继续执行")
        print("  2. 修改任务描述")
        print("  3. 调整涌现阈值")
        print("  4. 添加新的Agent角色")
        print("  5. 查看详细状态")
        print("  0. 退出并保存")

        choice = input("\n请选择 (0-5): ").strip()

        actions = {
            "1": "continue",
            "2": "modify_task",
            "3": "adjust_threshold",
            "4": "add_agent",
            "5": "view_status",
            "0": "exit"
        }

        return actions.get(choice, "continue")

    def get_user_modification(self, prompt: str) -> str:
        """获取用户输入的修改"""
        return input(f"\n{prompt}: ").strip()

    def resume_from_checkpoint(self, session_id: str, round_num: int) -> Optional[Dict]:
        """从检查点恢复"""
        return self.checkpoint_manager.load_checkpoint(session_id, round_num)
```

#### 5.5 集成到协作引擎
**文件**: `ecs/collaboration.py`

```python
from ..intervention.handlers import InterventionHandler
from ..intervention.interrupt import InterruptHandler

class CollaborationEngine:
    def __init__(self, ...):
        # ... 现有初始化代码
        self.intervention_handler = InterventionHandler()
        self.interrupt_handler = InterruptHandler()
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 注册中断处理器
        self.interrupt_handler.register()

    async def _discuss_phase(self, task: str):
        """带干预的讨论阶段"""
        for round_num in range(1, self.config.max_rounds + 1):
            # ... 执行讨论

            # 检查是否需要干预
            if self.intervention_handler.should_intervene(round_num):
                state = {
                    "viewpoint_space": self.viewpoint_space,
                    "discussion_history": self.discussion_history,
                    "emergence_score": self.emergence_detector._history[-1].metrics.emergence_score if self.emergence_detector._history else 0
                }

                action = self.intervention_handler.handle_intervention(
                    self.session_id,
                    round_num,
                    state
                )

                # 处理用户选择
                if action == "modify_task":
                    new_task = self.intervention_handler.get_user_modification("请输入新的任务描述")
                    task = new_task  # 修改任务

                elif action == "adjust_threshold":
                    new_threshold = float(self.intervention_handler.get_user_modification("请输入新的涌现阈值 (0.5-0.9)"))
                    self.config.emergence_threshold = new_threshold

                elif action == "add_agent":
                    # 添加新Agent的逻辑
                    pass

                elif action == "exit":
                    # 保存并退出
                    return
```

---

## 阶段六：生产化（1周）🟢 P2

### 目标
添加Docker支持、部署文档、集成测试。

### 任务清单

#### 6.1 Docker配置
**新建文件**: `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口（Web UI）
EXPOSE 8501

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import ecs; print('OK')"

# 默认运行Web UI
CMD ["streamlit", "run", "ecs/ui/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 6.2 Docker Compose
**新建文件**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  ecs:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data
      - ./checkpoints:/app/checkpoints
    restart: unless-stopped
```

#### 6.3 集成测试
**新建文件**: `tests/integration/test_integration.py`

```python
import pytest
import asyncio
from ecs import ECSCoordinator, ECSConfig

@pytest.mark.integration
async def test_parallel_execution():
    """测试并行执行"""
    config = ECSConfig()
    config.agents.count = 5
    config.collaboration.max_rounds = 2

    coordinator = ECSCoordinator(config)

    import time
    start = time.time()

    result = coordinator.collaborate(
        task="设计一个TODO应用",
        agent_count=5,
        max_rounds=2
    )

    elapsed = time.time() - start

    # 并行执行应该很快（5个Agent并行）
    assert elapsed < 30, f"并行执行耗时{elapsed:.1f}秒，可能未真正并行"
    assert result.emergence_report.metrics.emergence_score > 0

@pytest.mark.integration
def test_memory_system():
    """测试记忆系统"""
    from ecs.memory.manager import MemoryManager

    memory = MemoryManager()

    # 保存经验
    memory.save_collaboration_experience(
        task="设计一个API接口",
        config={"agents": 5, "rounds": 3},
        result={"solution": "..."},
        emergence_score=0.85
    )

    # 检索相似任务
    config = memory.recommend_config("设计一个REST API")
    assert config is not None
    assert config["agents"] == 5

@pytest.mark.integration
def test_semantic_similarity():
    """测试语义相似度"""
    from ecs.core.semantic import SemanticEmbedder

    sim = SemanticEmbedder.similarity(
        "设计一个用户登录系统",
        "创建用户认证功能"
    )

    assert sim > 0.5, "语义相似度应该较高"
```

#### 6.4 部署文档
**新建文件**: `DEPLOYMENT.md`

```markdown
# ECS 3.0 部署指南

## 本地部署

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥
```bash
cp .env.example .env
# 编辑.env文件，添加ANTHROPIC_API_KEY
```

### 3. 运行示例
```bash
python examples.py
```

### 4. 启动Web UI
```bash
streamlit run ecs/ui/dashboard.py
```

## Docker部署

### 1. 构建镜像
```bash
docker build -t ecs:3.0 .
```

### 2. 运行容器
```bash
docker run -d \
  -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  ecs:3.0
```

### 3. 使用Docker Compose
```bash
docker-compose up -d
```

访问 http://localhost:8501

## 生产环境部署

### 环境变量
- `ANTHROPIC_API_KEY`: Claude API密钥（必需）
- `ECS_LOG_LEVEL`: 日志级别（默认INFO）
- `ECS_DATA_DIR`: 数据目录（默认./data）
- `ECS_CHECKPOINT_DIR`: 检查点目录（默认./checkpoints）

### 资源需求
- CPU: 4核心以上
- 内存: 4GB以上
- 磁盘: 10GB以上（用于向量数据库）

### 监控
- 检查点文件用于断点续传
- 日志文件在 `logs/` 目录
- Web UI提供实时监控
```

---

## 版本更新计划

### ECS 2.0 → 2.1 (阶段一完成)
- 并行执行架构
- 重试机制
- 导入问题修复

### ECS 2.1 → 2.5 (阶段二、三完成)
- 三层记忆系统
- 语义相似度升级

### ECS 2.5 → 3.0 (阶段四、五、六完成)
- 可视化系统
- 干预能力
- 生产化支持

---

## 验收标准

### 阶段一完成
- [ ] 5个Agent×3轮讨论耗时 < 20秒
- [ ] 所有导入错误已修复
- [ ] 重试机制正常工作

### 阶段二完成
- [ ] 可以保存协作历史
- [ ] 可以检索相似任务配置
- [ ] 记忆持久化到文件

### 阶段三完成
- [ ] 语义相似度准确率 > 0.8
- [ ] 向量检索正常工作
- [ ] 模型缓存正常

### 阶段四完成
- [ ] Web UI可正常启动
- [ ] 实时指标图表正常显示
- [ ] Agent网络图正确渲染

### 阶段五完成
- [ ] 可以设置检查点
- [ ] 可以从中断恢复
- [ ] 可以中途修改任务

### 阶段六完成
- [ ] Docker镜像构建成功
- [ ] 容器可正常启动
- [ ] 集成测试通过

---

**蓝图状态**: ✅ 已完成，待Dealer生成详细指令
**下一环节**: Dealer → Ralph (Worker)
**预计完成时间**: 9-10周
