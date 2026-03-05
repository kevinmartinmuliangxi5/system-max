"""
安全沙箱与特征提取模块

负责代码执行、安全检查、多维度特征提取
评分提升: 从6维特征扩展到18+维，支持真涌现分析
"""

import time
import traceback
import ast
import signal
from typing import Any, Optional, Dict, List, Tuple
from contextlib import contextmanager
from io import StringIO
import sys

from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze

from .config import Config
from .utils import logger, validate_code_syntax, is_safe_code


class TimeoutException(Exception):
    """执行超时异常"""
    pass


@contextmanager
def time_limit(seconds: int):
    """执行时间限制上下文管理器（仅Unix）"""
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    # Windows不支持SIGALRM，使用简单的标志
    if Config.PLATFORM == "Windows":
        yield
    else:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)


class CodeExecutor:
    """安全代码执行器"""

    def __init__(self):
        self.safe_globals = Config.get_safe_globals()
        logger.info("Code executor initialized")

    def execute(
        self,
        code: str,
        test_input: Any,
        timeout: int = Config.SANDBOX_TIMEOUT
    ) -> Tuple[bool, Any, float, Optional[str]]:
        """执行代码并返回结果

        Args:
            code: 待执行代码
            test_input: 测试输入
            timeout: 超时时间（秒）

        Returns:
            (成功标志, 输出结果, 执行时间, 错误信息)
        """
        # 语法验证
        is_valid, syntax_error = validate_code_syntax(code)
        if not is_valid:
            return False, None, 0, f"Syntax error: {syntax_error}"

        # 安全检查
        is_safe, safety_error = is_safe_code(code)
        if not is_safe:
            return False, None, 0, f"Security error: {safety_error}"

        # 提取函数名
        func_name = self._extract_function_name(code)
        if not func_name:
            return False, None, 0, "No function definition found"

        # 执行代码
        start_time = time.time()
        try:
            # 准备执行环境
            local_vars = {}
            exec(code, self.safe_globals.copy(), local_vars)

            # 获取函数
            if func_name not in local_vars:
                return False, None, 0, f"Function '{func_name}' not found"

            func = local_vars[func_name]

            # 执行函数（带超时）
            if Config.PLATFORM == "Windows":
                # Windows简单超时处理
                result = self._execute_with_timeout_windows(func, test_input, timeout)
            else:
                with time_limit(timeout):
                    result = self._call_function(func, test_input)

            elapsed = time.time() - start_time
            return True, result, elapsed, None

        except TimeoutException:
            elapsed = time.time() - start_time
            return False, None, elapsed, "Execution timeout"

        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.debug(f"Execution error: {error_msg}")
            return False, None, elapsed, error_msg

    def _execute_with_timeout_windows(self, func, test_input, timeout):
        """Windows平台简单超时处理"""
        import threading

        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = self._call_function(func, test_input)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            raise TimeoutException("Execution timeout")

        if exception[0]:
            raise exception[0]

        return result[0]

    def _call_function(self, func, test_input):
        """调用函数"""
        if isinstance(test_input, (list, tuple)):
            return func(*test_input)
        else:
            return func(test_input)

    def _extract_function_name(self, code: str) -> Optional[str]:
        """提取函数名"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except:
            pass
        return None

    def batch_execute(
        self,
        code: str,
        test_cases: Dict[Any, Any]
    ) -> Tuple[float, float, List[str]]:
        """批量执行测试用例

        Args:
            code: 待测试代码
            test_cases: 测试用例字典 {input: expected_output}

        Returns:
            (正确率, 平均执行时间, 错误信息列表)
        """
        if not test_cases:
            return 0.0, 0.0, ["No test cases provided"]

        passed = 0
        total = len(test_cases)
        total_time = 0
        errors = []

        for test_input, expected_output in test_cases.items():
            success, result, elapsed, error = self.execute(code, test_input)
            total_time += elapsed

            if success and result == expected_output:
                passed += 1
            else:
                if error:
                    errors.append(f"Input {test_input}: {error}")
                else:
                    errors.append(f"Input {test_input}: Expected {expected_output}, got {result}")

        accuracy = passed / total
        avg_time = total_time / total

        logger.debug(f"Batch execution: {passed}/{total} passed, avg time: {avg_time:.4f}s")
        return accuracy, avg_time, errors


class FeatureExtractor:
    """多维度特征提取器

    从6维扩展到18+维，支持相空间重构
    """

    def __init__(self):
        self.executor = CodeExecutor()
        logger.info("Feature extractor initialized")

    def extract(self, code: str, test_cases: Dict[Any, Any]) -> Dict[str, float]:
        """提取完整特征向量

        Returns:
            18+维特征字典
        """
        features = {}

        # === 基础执行特征 (3维) ===
        accuracy, avg_time, errors = self.executor.batch_execute(code, test_cases)
        features["accuracy"] = accuracy
        features["avg_execution_time"] = avg_time
        features["error_rate"] = len(errors) / max(len(test_cases), 1)

        # === 代码质量特征 (6维) ===
        quality = self._extract_code_quality(code)
        features.update(quality)

        # === 复杂度特征 (4维) ===
        complexity = self._extract_complexity(code)
        features.update(complexity)

        # === 结构特征 (5维) ===
        structure = self._extract_structure(code)
        features.update(structure)

        # === 语义特征 (2维) ===
        semantics = self._extract_semantics(code)
        features.update(semantics)

        logger.debug(f"Extracted {len(features)} features")
        return features

    def _extract_code_quality(self, code: str) -> Dict[str, float]:
        """代码质量特征"""
        try:
            # 可维护性指数 (0-100)
            mi_result = mi_visit(code, multi=True)
            mi_score = mi_result if isinstance(mi_result, (int, float)) else sum(mi_result) / max(len(mi_result), 1)
            mi_normalized = mi_score / 100.0

            # Halstead指标
            h_result = h_visit(code)
            if h_result:
                h_total = h_result[0] if isinstance(h_result, tuple) else h_result
                volume = getattr(h_total, 'volume', 100)
                difficulty = getattr(h_total, 'difficulty', 10)
                effort = getattr(h_total, 'effort', 1000)
            else:
                volume, difficulty, effort = 100, 10, 1000

            # 代码行数分析
            raw = analyze(code)
            loc = raw.loc  # 代码行数
            lloc = raw.lloc  # 逻辑行数
            comments = raw.comments  # 注释行数

            return {
                "maintainability_index": mi_normalized,
                "halstead_volume": min(volume / 1000.0, 1.0),
                "halstead_difficulty": min(difficulty / 50.0, 1.0),
                "halstead_effort": min(effort / 10000.0, 1.0),
                "code_density": lloc / max(loc, 1),
                "comment_ratio": comments / max(loc, 1),
            }
        except Exception as e:
            logger.warning(f"Code quality extraction failed: {e}")
            return {
                "maintainability_index": 0.5,
                "halstead_volume": 0.5,
                "halstead_difficulty": 0.5,
                "halstead_effort": 0.5,
                "code_density": 0.5,
                "comment_ratio": 0.0,
            }

    def _extract_complexity(self, code: str) -> Dict[str, float]:
        """复杂度特征"""
        try:
            # 圈复杂度
            cc_results = cc_visit(code)
            if cc_results:
                avg_complexity = sum(r.complexity for r in cc_results) / len(cc_results)
                max_complexity = max(r.complexity for r in cc_results)
            else:
                avg_complexity = 1
                max_complexity = 1

            # AST节点统计
            tree = ast.parse(code)
            node_count = sum(1 for _ in ast.walk(tree))
            depth = self._ast_depth(tree)

            return {
                "cyclomatic_complexity": min(avg_complexity / 10.0, 1.0),
                "max_complexity": min(max_complexity / 20.0, 1.0),
                "ast_node_count": min(node_count / 100.0, 1.0),
                "ast_depth": min(depth / 20.0, 1.0),
            }
        except Exception as e:
            logger.warning(f"Complexity extraction failed: {e}")
            return {
                "cyclomatic_complexity": 0.5,
                "max_complexity": 0.5,
                "ast_node_count": 0.5,
                "ast_depth": 0.5,
            }

    def _extract_structure(self, code: str) -> Dict[str, float]:
        """结构特征"""
        try:
            tree = ast.parse(code)

            # 统计不同类型的节点
            loops = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While)))
            conditionals = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))
            functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))

            # 归一化
            return {
                "loop_count": min(loops / 5.0, 1.0),
                "conditional_count": min(conditionals / 10.0, 1.0),
                "function_count": min(functions / 5.0, 1.0),
                "class_count": min(classes / 3.0, 1.0),
                "nesting_depth": min(self._max_nesting_depth(tree) / 5.0, 1.0),
            }
        except Exception as e:
            logger.warning(f"Structure extraction failed: {e}")
            return {
                "loop_count": 0.0,
                "conditional_count": 0.0,
                "function_count": 0.0,
                "class_count": 0.0,
                "nesting_depth": 0.0,
            }

    def _extract_semantics(self, code: str) -> Dict[str, float]:
        """语义特征"""
        try:
            tree = ast.parse(code)

            # 变量使用
            names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
            unique_names = len(set(names))
            name_reuse = len(names) / max(unique_names, 1)

            # 操作符使用
            operators = sum(1 for node in ast.walk(tree)
                          if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp)))

            return {
                "variable_reuse": min(name_reuse / 5.0, 1.0),
                "operator_diversity": min(operators / 20.0, 1.0),
            }
        except Exception as e:
            logger.warning(f"Semantics extraction failed: {e}")
            return {
                "variable_reuse": 0.5,
                "operator_diversity": 0.5,
            }

    def _ast_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """计算AST深度"""
        if not hasattr(node, '_fields') or not node._fields:
            return current_depth

        max_child_depth = current_depth
        for child in ast.iter_child_nodes(node):
            child_depth = self._ast_depth(child, current_depth + 1)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def _max_nesting_depth(self, tree: ast.AST) -> int:
        """计算最大嵌套深度"""
        def get_depth(node, depth=0):
            if isinstance(node, (ast.For, ast.While, ast.If, ast.With)):
                depth += 1

            max_depth = depth
            for child in ast.iter_child_nodes(node):
                max_depth = max(max_depth, get_depth(child, depth))

            return max_depth

        return get_depth(tree)

    def extract_vector(self, features: Dict[str, float]) -> List[float]:
        """将特征字典转换为向量

        返回固定顺序的特征向量，用于相空间重构
        """
        # 定义特征顺序
        feature_order = [
            # 基础执行 (3)
            "accuracy", "avg_execution_time", "error_rate",
            # 代码质量 (6)
            "maintainability_index", "halstead_volume", "halstead_difficulty",
            "halstead_effort", "code_density", "comment_ratio",
            # 复杂度 (4)
            "cyclomatic_complexity", "max_complexity", "ast_node_count", "ast_depth",
            # 结构 (5)
            "loop_count", "conditional_count", "function_count", "class_count", "nesting_depth",
            # 语义 (2)
            "variable_reuse", "operator_diversity",
        ]

        return [features.get(key, 0.0) for key in feature_order]


# === 导出接口 ===
class Sandbox:
    """沙箱统一接口"""

    def __init__(self):
        self.executor = CodeExecutor()
        self.extractor = FeatureExtractor()
        logger.info("Sandbox initialized")

    def evaluate(
        self,
        code: str,
        test_cases: Dict[Any, Any]
    ) -> Tuple[float, Dict[str, float], List[float]]:
        """完整评估代码

        Args:
            code: 待评估代码
            test_cases: 测试用例

        Returns:
            (正确率, 特征字典, 特征向量)
        """
        features = self.extractor.extract(code, test_cases)
        vector = self.extractor.extract_vector(features)
        accuracy = features["accuracy"]

        logger.info(f"Code evaluation: accuracy={accuracy:.2%}, features={len(features)}")
        return accuracy, features, vector

    def quick_test(self, code: str, test_input: Any) -> Tuple[bool, Any, Optional[str]]:
        """快速单次测试

        Args:
            code: 待测试代码
            test_input: 测试输入

        Returns:
            (成功标志, 输出结果, 错误信息)
        """
        success, result, _, error = self.executor.execute(code, test_input)
        return success, result, error
