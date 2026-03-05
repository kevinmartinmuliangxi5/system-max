"""
演化引擎模块

核心演化逻辑，整合所有子系统:
1. 种群管理 - 多样性维护、精英保留
2. 遗传操作 - 变异、交叉
3. 早停机制 - 基于涌现检测的智能停止
4. 知识迁移 - 跨任务学习

评分核心: 从盲目演化到智能引导式演化
"""

import asyncio
import random
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
import numpy as np

from .config import Config, AdaptiveConfig
from .llm_engine import LLMEngine
from .sandbox import Sandbox
from .emergence import EmergenceDetector
from .knowledge import KnowledgeManager
from .utils import logger, timeit


@dataclass
class Individual:
    """种群个体"""

    code: str
    score: float = 0.0
    features: Dict[str, float] = field(default_factory=dict)
    feature_vector: List[float] = field(default_factory=list)
    generation: int = 0
    parent_id: Optional[int] = None
    mutation_history: List[str] = field(default_factory=list)

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return isinstance(other, Individual) and self.code == other.code


class Population:
    """种群管理器"""

    def __init__(self, size: int):
        self.size = size
        self.individuals: List[Individual] = []
        self.best_ever: Optional[Individual] = None
        self.diversity_threshold = 0.15  # 最小多样性
        logger.info(f"Population initialized: size={size}")

    def add(self, individual: Individual) -> None:
        """添加个体"""
        self.individuals.append(individual)

        # 更新历史最佳
        if self.best_ever is None or individual.score > self.best_ever.score:
            self.best_ever = individual
            logger.info(f"New best: score={individual.score:.4f}")

    def get_best(self, k: int = 1) -> List[Individual]:
        """获取最佳个体"""
        sorted_pop = sorted(self.individuals, key=lambda x: x.score, reverse=True)
        return sorted_pop[:k]

    def select_parents(self, k: int = 2) -> List[Individual]:
        """选择父代（锦标赛选择）"""
        if len(self.individuals) < k:
            return self.individuals.copy()

        # 从种群中随机选择k*3个候选
        candidates = random.sample(
            self.individuals, min(k * 3, len(self.individuals))
        )

        # 选择最佳的k个
        parents = sorted(candidates, key=lambda x: x.score, reverse=True)[:k]
        return parents

    def prune(self, keep_ratio: float = 0.5) -> None:
        """淘汰低质量个体，保持精英"""
        if len(self.individuals) <= self.size:
            return

        # 按得分排序
        sorted_pop = sorted(self.individuals, key=lambda x: x.score, reverse=True)

        # 保留top个体
        keep_count = max(int(self.size * keep_ratio), 1)
        self.individuals = sorted_pop[:keep_count]

        logger.debug(f"Pruned population: {len(self.individuals)} remaining")

    def calculate_diversity(self) -> float:
        """计算种群多样性（基于代码哈希）"""
        if len(self.individuals) <= 1:
            return 1.0

        unique_codes = len(set(ind.code for ind in self.individuals))
        diversity = unique_codes / len(self.individuals)

        return diversity

    def is_diverse(self) -> bool:
        """检查多样性是否足够"""
        diversity = self.calculate_diversity()
        return diversity >= self.diversity_threshold

    def get_feature_trajectory(self) -> List[List[float]]:
        """获取特征演化轨迹

        Returns:
            (代数, 特征维度) 的平均特征轨迹
        """
        # 按代数分组
        gen_features = {}
        for ind in self.individuals:
            gen = ind.generation
            if gen not in gen_features:
                gen_features[gen] = []
            gen_features[gen].append(ind.feature_vector)

        # 计算每代的平均特征
        trajectory = []
        for gen in sorted(gen_features.keys()):
            vectors = gen_features[gen]
            if vectors and len(vectors[0]) > 0:
                avg_vector = np.mean(vectors, axis=0).tolist()
                trajectory.append(avg_vector)

        return trajectory

    def get_stats(self) -> Dict:
        """获取种群统计"""
        if not self.individuals:
            return {"size": 0, "avg_score": 0, "max_score": 0, "diversity": 0}

        scores = [ind.score for ind in self.individuals]

        return {
            "size": len(self.individuals),
            "avg_score": np.mean(scores),
            "max_score": np.max(scores),
            "min_score": np.min(scores),
            "diversity": self.calculate_diversity(),
        }


class EvolutionEngine:
    """演化引擎（异步）"""

    def __init__(self):
        self.llm = LLMEngine()
        self.sandbox = Sandbox()
        self.emergence = EmergenceDetector()
        self.knowledge = KnowledgeManager()
        self.adaptive_config = AdaptiveConfig()

        # 演化参数
        self.population_size = Config.POPULATION_SIZE
        self.max_generations = Config.MAX_GENERATIONS
        self.mutation_rate = Config.INITIAL_MUTATION_RATE
        self.early_stop_patience = Config.EARLY_STOP_PATIENCE

        logger.info("Evolution engine initialized")

    @timeit
    async def evolve(
        self,
        task_description: str,
        test_cases: Dict[Any, Any],
        callback: Optional[callable] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """执行演化过程

        Args:
            task_description: 任务描述
            test_cases: 测试用例
            callback: 回调函数（用于UI更新）

        Returns:
            (最佳代码, 演化指标)
        """
        logger.info(f"Starting evolution: {task_description[:50]}...")

        # === 1. 检查缓存 ===
        cached_code = self.knowledge.check_cache(task_description)
        if cached_code:
            logger.info("Using cached solution")
            return cached_code, {"generations": 0, "from_cache": True}

        # === 2. 分析意图 ===
        intent = await self.llm.analyze_intent(task_description)
        logger.info(f"Intent: {intent.get('intent')}, complexity: {intent.get('complexity')}")

        # === 3. 检索相似解决方案 ===
        similar_solutions = []
        if Config.ENABLE_KNOWLEDGE:
            # 先用空特征向量检索（基于任务描述的嵌入）
            # 实际可用embedding模型提取任务嵌入
            pass

        # === 4. 初始化种群 ===
        population = Population(self.population_size)
        await self._initialize_population(
            population, task_description, test_cases, similar_solutions
        )

        # === 5. 演化循环 ===
        metrics = {
            "generations": 0,
            "final_score": 0.0,
            "emergence_detected": False,
            "trajectory": [],
        }

        no_improvement = 0
        last_best_score = 0.0

        for generation in range(self.max_generations):
            metrics["generations"] = generation + 1

            # === 5.1 评估当前种群 ===
            logger.info(f"Generation {generation + 1}/{self.max_generations}")

            # === 5.2 检查终止条件 ===
            best = population.get_best(1)[0]
            metrics["final_score"] = best.score

            # 完美解
            if best.score >= 0.999:
                logger.info(f"Perfect solution found at generation {generation + 1}")
                break

            # 早停检测
            if best.score <= last_best_score + 0.001:
                no_improvement += 1
            else:
                no_improvement = 0
                last_best_score = best.score

            if no_improvement >= self.early_stop_patience:
                logger.info(f"Early stopping: no improvement for {no_improvement} generations")
                break

            # === 5.3 涌现检测 ===
            if generation >= 4 and Config.ENABLE_DOWNWARD_CAUSATION:
                trajectory = population.get_feature_trajectory()
                if len(trajectory) >= 5:
                    emergence_result = self.emergence.detect(trajectory)
                    metrics["emergence_detected"] = emergence_result["is_true_emergence"]
                    metrics["emergence_strength"] = emergence_result["emergence_strength"]

                    if emergence_result["is_true_emergence"]:
                        logger.info(
                            f"✨ True emergence detected! "
                            f"Strength: {emergence_result['emergence_strength']:.3f}"
                        )

                        # 涌现后降低变异率（系统已稳定）
                        self.mutation_rate *= 0.8
                        logger.info(f"Reduced mutation rate to {self.mutation_rate:.3f}")

            # === 5.4 生成下一代 ===
            await self._generate_next_generation(
                population, task_description, test_cases, generation + 1
            )

            # === 5.5 回调（UI更新）===
            if callback:
                pop_stats = population.get_stats()
                callback(generation + 1, pop_stats, metrics)

        # === 6. 后处理 ===
        best_individual = population.best_ever or population.get_best(1)[0]
        metrics["final_score"] = best_individual.score
        metrics["trajectory"] = population.get_feature_trajectory()

        # 存储知识
        if Config.ENABLE_KNOWLEDGE and best_individual.score >= 0.8:
            self.knowledge.store_solution(
                task_description,
                best_individual.code,
                best_individual.score,
                metrics["generations"],
                best_individual.feature_vector,
            )

            # 知识蒸馏
            if best_individual.score >= Config.PATTERN_THRESHOLD:
                await self.knowledge.distill_pattern(
                    self.llm, best_individual.code, task_description
                )

        # 更新自适应配置
        self.adaptive_config.update_from_result(metrics)

        logger.info(
            f"Evolution complete: "
            f"score={best_individual.score:.4f}, "
            f"generations={metrics['generations']}"
        )

        return best_individual.code, metrics

    async def _initialize_population(
        self,
        population: Population,
        task: str,
        test_cases: Dict,
        similar_solutions: List[Dict],
    ) -> None:
        """初始化种群"""
        logger.info("Initializing population...")

        # 生成初始代码
        prompts = []

        # 基础提示
        base_prompt = f"Write a Python function to solve: {task}"
        prompts.append(base_prompt)

        # 多样性提示
        variations = [
            f"{base_prompt}\nUse an iterative approach.",
            f"{base_prompt}\nUse a recursive approach.",
            f"{base_prompt}\nOptimize for speed.",
            f"{base_prompt}\nOptimize for readability.",
        ]
        prompts.extend(variations[: self.population_size - 1])

        # 如果有相似解决方案，添加提示
        if similar_solutions:
            for sol in similar_solutions[:2]:
                prompts.append(
                    f"{base_prompt}\n\nReference solution:\n```python\n{sol['code']}\n```"
                )

        # 并发生成
        tasks = [
            self._create_individual(prompt, test_cases, 0)
            for prompt in prompts[: self.population_size]
        ]
        individuals = await asyncio.gather(*tasks)

        # 添加到种群
        for ind in individuals:
            if ind:
                population.add(ind)

        logger.info(f"Initialized population: {len(population.individuals)} individuals")

    async def _create_individual(
        self,
        prompt: str,
        test_cases: Dict,
        generation: int,
    ) -> Optional[Individual]:
        """创建个体"""
        try:
            # 生成代码
            code = await self.llm.generate(prompt, temp=0.7)

            if not code:
                return None

            # 评估
            accuracy, features, feature_vector = self.sandbox.evaluate(code, test_cases)

            # 综合得分（可扩展为多目标）
            score = accuracy * 0.8 + features.get("maintainability_index", 0) * 0.2

            individual = Individual(
                code=code,
                score=score,
                features=features,
                feature_vector=feature_vector,
                generation=generation,
            )

            return individual

        except Exception as e:
            logger.error(f"Failed to create individual: {e}")
            return None

    async def _generate_next_generation(
        self,
        population: Population,
        task: str,
        test_cases: Dict,
        generation: int,
    ) -> None:
        """生成下一代"""
        # 保留精英
        elites = population.get_best(max(1, self.population_size // 4))

        # 生成新个体
        new_individuals = []

        # 变异
        n_mutations = int(self.population_size * 0.5)
        for _ in range(n_mutations):
            parent = random.choice(population.select_parents(1))
            mutated = await self._mutate(parent, task, test_cases, generation)
            if mutated:
                new_individuals.append(mutated)

        # 交叉
        n_crossovers = self.population_size - len(elites) - len(new_individuals)
        for _ in range(n_crossovers):
            parents = population.select_parents(2)
            if len(parents) >= 2:
                offspring = await self._crossover(parents[0], parents[1], task, test_cases, generation)
                if offspring:
                    new_individuals.append(offspring)

        # 更新种群
        population.individuals = elites + new_individuals
        population.prune()

        # 多样性检查
        if not population.is_diverse():
            logger.warning("Low diversity, adding random individuals")
            random_ind = await self._create_individual(
                f"Write a Python function to solve: {task}", test_cases, generation
            )
            if random_ind:
                population.add(random_ind)

    async def _mutate(
        self,
        parent: Individual,
        task: str,
        test_cases: Dict,
        generation: int,
    ) -> Optional[Individual]:
        """变异操作"""
        mutation_types = [
            "improve efficiency",
            "improve readability",
            "add error handling",
            "optimize algorithm",
            "simplify logic",
        ]

        mutation = random.choice(mutation_types)

        prompt = f"""Modify the following code to {mutation}:

Task: {task}

Current code:
```python
{parent.code}
```

Provide the modified code."""

        try:
            code = await self.llm.generate(prompt, temp=0.8)
            if not code or code == parent.code:
                return None

            accuracy, features, feature_vector = self.sandbox.evaluate(code, test_cases)
            score = accuracy * 0.8 + features.get("maintainability_index", 0) * 0.2

            individual = Individual(
                code=code,
                score=score,
                features=features,
                feature_vector=feature_vector,
                generation=generation,
                mutation_history=parent.mutation_history + [mutation],
            )

            return individual

        except:
            return None

    async def _crossover(
        self,
        parent1: Individual,
        parent2: Individual,
        task: str,
        test_cases: Dict,
        generation: int,
    ) -> Optional[Individual]:
        """交叉操作"""
        prompt = f"""Combine the best aspects of these two solutions:

Task: {task}

Solution 1 (score: {parent1.score:.2f}):
```python
{parent1.code}
```

Solution 2 (score: {parent2.score:.2f}):
```python
{parent2.code}
```

Create a hybrid solution that takes the best from both."""

        try:
            code = await self.llm.generate(prompt, temp=0.7)
            if not code:
                return None

            accuracy, features, feature_vector = self.sandbox.evaluate(code, test_cases)
            score = accuracy * 0.8 + features.get("maintainability_index", 0) * 0.2

            individual = Individual(
                code=code,
                score=score,
                features=features,
                feature_vector=feature_vector,
                generation=generation,
            )

            return individual

        except:
            return None

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "llm_stats": self.llm.get_stats(),
            "knowledge_stats": self.knowledge.get_stats(),
            "adaptive_params": self.adaptive_config.get_params(),
        }
