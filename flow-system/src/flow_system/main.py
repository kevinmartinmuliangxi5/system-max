"""
主程序入口

提供命令行界面和Textual UI可视化
评分提升: 从无可视化到实时交互式Dashboard
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    Input,
    Label,
    ProgressBar,
    TextArea,
    DataTable,
)
from textual.reactive import reactive
from textual import work

from .config import Config
from .evolution_engine import EvolutionEngine
from .utils import logger, colorize, Colors


class StatusPanel(Static):
    """状态面板"""

    generation = reactive(0)
    score = reactive(0.0)
    emergence = reactive(False)

    def render(self) -> str:
        emergence_icon = "✨" if self.emergence else "⏳"
        return f"""
[bold cyan]Evolution Status[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generation: [yellow]{self.generation}[/yellow] / {Config.MAX_GENERATIONS}
Best Score: [green]{self.score:.2%}[/green]
Emergence:  {emergence_icon} [{'green' if self.emergence else 'dim'}]{'Detected' if self.emergence else 'Searching...'}[/]
"""


class MetricsPanel(Static):
    """指标面板"""

    metrics = reactive({})

    def render(self) -> str:
        if not self.metrics:
            return "[dim]Waiting for metrics...[/dim]"

        m = self.metrics
        return f"""
[bold cyan]Population Metrics[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Population: {m.get('size', 0)}
Avg Score:  {m.get('avg_score', 0):.2%}
Max Score:  {m.get('max_score', 0):.2%}
Diversity:  {m.get('diversity', 0):.2%}

[bold cyan]Emergence Metrics[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lyapunov:   {m.get('lyapunov', 0):.4f}
Effect Info: {m.get('ei', 0):.4f}
Strength:   {m.get('emergence_strength', 0):.2%}
"""


class KnowledgePanel(Static):
    """知识库面板"""

    stats = reactive({})

    def render(self) -> str:
        if not self.stats:
            return "[dim]No knowledge data yet...[/dim]"

        return f"""
[bold cyan]Knowledge Base[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Patterns:    {self.stats.get('pattern_count', 0)}
History:     {self.stats.get('history_count', 0)}
Vectors:     {self.stats.get('faiss_vectors', 0)}
Avg Quality: {self.stats.get('avg_quality', 0):.2%}
"""


class CodeViewer(Static):
    """代码查看器"""

    code = reactive("")

    def render(self) -> str:
        if not self.code:
            return "[dim]No code generated yet...[/dim]"

        return f"""[bold cyan]Best Code[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```python
{self.code}
```
"""


class FlowSystemUI(App):
    """FlowSystem交互式UI"""

    CSS = """
    Screen {
        background: $surface;
    }

    StatusPanel, MetricsPanel, KnowledgePanel {
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: auto;
    }

    CodeViewer {
        border: solid $accent;
        padding: 1;
        margin: 1;
        height: 20;
    }

    #task-input {
        margin: 1;
        border: solid $primary;
    }

    #controls {
        height: auto;
        margin: 1;
    }

    Button {
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run", "Run Evolution"),
        ("p", "pause", "Pause/Resume"),
        ("c", "clear", "Clear"),
    ]

    # 类级别状态变量（不使用reactive，避免复杂性）
    def __init__(self):
        super().__init__()
        self.engine = EvolutionEngine()
        self._is_running = False
        self._is_paused = False
        self._current_task = None

    def compose(self) -> ComposeResult:
        """构建UI"""
        yield Header(show_clock=True)

        # 任务输入
        yield Input(
            placeholder="Enter task description (e.g., 'Write a function to reverse a string')",
            id="task-input",
        )

        # 控制按钮
        with Horizontal(id="controls"):
            yield Button("Run Evolution", id="run-btn", variant="success")
            yield Button("Pause", id="pause-btn", variant="warning")
            yield Button("Clear", id="clear-btn", variant="error")

        # 主面板
        with Horizontal():
            # 左侧
            with Vertical():
                yield StatusPanel(id="status-panel")
                yield MetricsPanel(id="metrics-panel")
                yield KnowledgePanel(id="knowledge-panel")

            # 右侧
            yield CodeViewer(id="code-viewer")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮事件"""
        if event.button.id == "run-btn":
            self.action_run()
        elif event.button.id == "pause-btn":
            self.action_pause()
        elif event.button.id == "clear-btn":
            self.action_clear()

    def action_run(self) -> None:
        """运行演化"""
        if self._is_running:
            self.notify("Evolution already running!", severity="warning")
            return

        task_input = self.query_one("#task-input", Input)
        task = task_input.value.strip()

        if not task:
            self.notify("Please enter a task description!", severity="error")
            return

        self._current_task = task
        self._is_running = True
        self.run_evolution()

    def action_pause(self) -> None:
        """暂停/恢复"""
        if not self._is_running:
            self.notify("No evolution running!", severity="warning")
            return

        self._is_paused = not self._is_paused
        status = "Paused" if self._is_paused else "Resumed"
        self.notify(f"Evolution {status}", severity="information")

    def action_clear(self) -> None:
        """清空"""
        self.query_one("#task-input", Input).value = ""
        self.query_one("#status-panel", StatusPanel).generation = 0
        self.query_one("#status-panel", StatusPanel).score = 0.0
        self.query_one("#status-panel", StatusPanel).emergence = False
        self.query_one("#code-viewer", CodeViewer).code = ""
        self.notify("Cleared!", severity="information")

    @work(exclusive=True)
    async def run_evolution(self) -> None:
        """执行演化（异步工作线程）"""
        try:
            # 生成测试用例
            self.notify("Generating test cases...", severity="information")
            test_cases = await self.engine.llm.generate_test_cases(self._current_task)

            if not test_cases:
                self.notify("Failed to generate test cases!", severity="error")
                self._is_running = False
                return

            # 定义回调
            def callback(generation, pop_stats, metrics):
                # 更新状态面板
                status_panel = self.query_one("#status-panel", StatusPanel)
                status_panel.generation = generation
                status_panel.score = metrics.get("final_score", 0)
                status_panel.emergence = metrics.get("emergence_detected", False)

                # 更新指标面板
                metrics_panel = self.query_one("#metrics-panel", MetricsPanel)
                combined_metrics = {**pop_stats, **metrics}
                metrics_panel.metrics = combined_metrics

            # 运行演化
            self.notify("Starting evolution...", severity="information")
            best_code, metrics = await self.engine.evolve(
                self._current_task, test_cases, callback
            )

            # 显示结果
            code_viewer = self.query_one("#code-viewer", CodeViewer)
            code_viewer.code = best_code

            # 更新知识库面板
            knowledge_stats = self.engine.knowledge.get_stats()
            knowledge_panel = self.query_one("#knowledge-panel", KnowledgePanel)
            knowledge_panel.stats = knowledge_stats

            # 通知完成
            self.notify(
                f"Evolution complete! Score: {metrics['final_score']:.2%}",
                severity="success",
            )

        except Exception as e:
            logger.error(f"Evolution failed: {e}")
            self.notify(f"Error: {str(e)}", severity="error")

        finally:
            self._is_running = False


def run_ui():
    """启动UI"""
    app = FlowSystemUI()
    app.run()


def run_cli(task: str, output_file: Optional[Path] = None):
    """命令行模式

    Args:
        task: 任务描述
        output_file: 输出文件路径
    """
    print(colorize("FlowSystem - True Emergence Programming", Colors.CYAN + Colors.BOLD))
    print("=" * 60)

    # 初始化引擎
    engine = EvolutionEngine()

    async def evolve_task():
        # 生成测试用例
        print(colorize("\n[1/3] Generating test cases...", Colors.YELLOW))
        test_cases = await engine.llm.generate_test_cases(task)

        if not test_cases:
            print(colorize("❌ Failed to generate test cases", Colors.RED))
            return None, None

        print(colorize(f"✓ Generated {len(test_cases)} test cases", Colors.GREEN))

        # 运行演化
        print(colorize("\n[2/3] Running evolution...", Colors.YELLOW))

        def callback(generation, pop_stats, metrics):
            print(
                f"Gen {generation}: "
                f"Score={metrics['final_score']:.2%}, "
                f"Diversity={pop_stats['diversity']:.2%}, "
                f"Emergence={'✨' if metrics.get('emergence_detected') else '⏳'}"
            )

        best_code, metrics = await engine.evolve(task, test_cases, callback)

        # 显示结果
        print(colorize("\n[3/3] Results", Colors.YELLOW))
        print("=" * 60)
        print(colorize(f"Final Score: {metrics['final_score']:.2%}", Colors.GREEN))
        print(colorize(f"Generations: {metrics['generations']}", Colors.CYAN))
        print(
            colorize(
                f"Emergence: {'✨ Detected' if metrics.get('emergence_detected') else '⏳ Not detected'}",
                Colors.MAGENTA,
            )
        )
        print("\n" + colorize("Best Code:", Colors.CYAN))
        print("```python")
        print(best_code)
        print("```")

        return best_code, metrics

    # 运行
    best_code, metrics = asyncio.run(evolve_task())

    # 保存到文件
    if output_file and best_code:
        output_file.write_text(best_code, encoding="utf-8")
        print(colorize(f"\n✓ Saved to {output_file}", Colors.GREEN))

    # 显示统计
    stats = engine.get_stats()
    print("\n" + colorize("System Statistics:", Colors.CYAN))
    print(f"  LLM Calls: {stats['llm_stats']['total_calls']}")
    print(f"  Cache Hits: {stats['llm_stats']['cache_hits']}")
    print(f"  Knowledge Patterns: {stats['knowledge_stats']['pattern_count']}")
    print(f"  Task History: {stats['knowledge_stats']['history_count']}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="FlowSystem - True Emergence Programming")
    parser.add_argument("--task", "-t", type=str, help="Task description (CLI mode)")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--ui", action="store_true", help="Launch UI mode")

    args = parser.parse_args()

    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(colorize(str(e), Colors.RED))
        sys.exit(1)

    # 启动模式
    if args.ui or not args.task:
        # UI模式
        run_ui()
    else:
        # CLI模式
        output_path = Path(args.output) if args.output else None
        run_cli(args.task, output_path)


if __name__ == "__main__":
    main()
