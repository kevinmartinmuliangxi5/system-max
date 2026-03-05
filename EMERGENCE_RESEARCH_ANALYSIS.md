# Comprehensive Research Analysis: Emergence in AI Systems

**Research Date:** February 4, 2026
**Focus Areas:** Strong vs Weak Emergence, Emergent Abilities in LLMs, PromptBreeder, OPRO, Self-Referential Evolution, Complex Adaptive Systems, Code Generation

---

## Executive Summary

This research analysis examines the state-of-the-art on "emergence" in AI systems, with a particular focus on whether "true emergence" is achievable in current systems. The evidence suggests a **nuanced landscape**: while AI systems exhibit impressive capabilities that appear emergent, the scientific community remains divided on whether these represent genuine strong emergence or sophisticated instances of weak emergence that are ultimately predictable and reducible.

**Key Finding:** Current AI systems demonstrate what appears to be weak emergence - complex behaviors arising from scale and architectural design that may be unpredictable in practice but are theoretically reducible to their components. True strong emergence (irreducible, top-down causal forces) remains undemonstrated.

---

## 1. Strong Emergence vs Weak Emergence: Definitions and Framework

### 1.1 Fundamental Definitions

#### Weak Emergence
Weak emergence suggests that emergent properties arise from the bottom-up organization of the system's lower-level components. This view is compatible with **ontological reductionism** - the view that system-level emergent phenomena are just lower-level components arranged in specific ways without the interference of new higher-level forces or causal forces.

Key characteristics:
- **Reducibility**: All relevant causation shaping system-level phenomena occurs through interactions of the system's elements at the lower levels
- **Predictability (in principle)**: Given complete information about components and their interactions, emergent behavior is theoretically predictable
- **Computational basis**: The predictive capability of a trained ANN is reducible to (exhaustively determined by) the model's constitutive elements (numeric values) and mathematical rules governing their interactions

**Sources:**
- [What Is Emerging in Artificial Intelligence Systems? - Max Planck Law](https://law.mpg.de/perspectives/what-is-emerging-in-artificial-intelligence-systems/)
- [Overview of Emergent Abilities in AI - World Scholars Review](https://www.worldscholarsreview.org/article/overview-of-emergent-abilities-in-ai)

#### Strong Emergence
Strong emergence posits that emergent properties are imposed in a top-down manner by new causal forces not present in the system's elements. This view includes the idea that system-level phenomena arise due to an intervention of new 'top-down' powers, including agency and subjectively experienced qualities such as mental states.

Key characteristics:
- **Irreducibility**: New causal forces appear at higher levels that cannot be reduced to lower-level interactions
- **Unpredictability (in principle)**: Even with complete knowledge of components, emergent behavior cannot be predicted from first principles
- **Novel causation**: System-level properties exert downward causal influence on components

**Source:** [Strong and Weak Emergence - David J. Chalmers](https://consc.net/papers/emergence.pdf)

### 1.2 Application to Current AI Systems

#### Current Consensus: AI as Weak Emergence
The predictive capability of ML models aligns with the weak account of emergence, particularly the proposition that all relevant causation shaping system-level phenomena occurs through interactions of the system's elements at the lower levels. The predictive capability of a trained ANN is reducible to—i.e., exhaustively determined by—the model's constitutive elements (numeric values) and mathematical and other rules governing their interactions comprised within the training algorithm.

#### The Classification Debate
Current approaches treat Generative AI through the lens of either:
1. **Weak Emergence** (complex but ultimately micro-determined), or
2. **Strong Emergence** (introducing qualitatively new causal powers)

Neither adequately captures these systems' actual behavior according to recent critical analyses.

**Source:** [Rethinking Emergence - KayStoner](https://kaystoner.substack.com/p/rethinking-emergence-the-full-paper)

#### Critical Assessment (2025)
Recent research challenges the emergence characterization: "Very few of the features of LLMs, from the abruptness of performance increases on benchmarks, through to generalization, have much, if anything to do with any technical sense of the word emergence, and are adequately described using the more familiar ideas of **learning, inference, compression, and perhaps development**."

**Source:** [Are LLMs truly intelligent? - TechTalks](https://bdtechtalks.com/2025/07/14/llm-emergent-intelligence-study/)

---

## 2. Recent Papers on Emergent Abilities in LLMs (2024-2025)

### 2.1 Foundational Work: Wei et al. (2022)

**Paper:** "Emergent Abilities of Large Language Models"
**Authors:** Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus
**Publication:** TMLR 2022, arXiv:2206.07682

**Key Definition:** An ability is considered emergent if it is **not present in smaller models but is present in larger models**, meaning emergent abilities cannot be predicted simply by extrapolating the performance of smaller models. Such emergent abilities have close to random performance until evaluated on a model of sufficiently large scale.

**Sources:**
- [ArXiv Abstract](https://arxiv.org/abs/2206.07682)
- [ArXiv PDF](https://arxiv.org/pdf/2206.07682)
- [Google Research Publication](https://research.google/pubs/emergent-abilities-of-large-language-models/)
- [Google Research Blog](https://research.google/blog/characterizing-emergent-phenomena-in-large-language-models/)

### 2.2 Comprehensive Survey (2025)

**Paper:** "Emergent Abilities in Large Language Models: A Survey"
**Publication:** arXiv:2503.05788 (2025)

This comprehensive survey conducts a thorough review of the emergent abilities phenomenon, addressing both scientific underpinnings and real-world consequences. The paper critically analyzes existing definitions and explores conditions under which these abilities appear, evaluating the role of:
- Scaling laws
- Task complexity
- Pre-training loss
- Quantization
- Prompting strategies

**Key Findings:**

1. **Phase Transition Analogy**: The phenomenon can be understood through an analogy to phase transitions in physics, where emergent abilities are not a product of gradual improvement but instead appear abruptly when scaling reaches a certain level, with performance often hovering near random until a threshold is surpassed.

2. **Scaling Factors**: Language models have been scaled primarily along three factors:
   - Amount of computation
   - Number of model parameters
   - Training dataset size

3. **Pre-Training Loss Relationship**: Research by Du et al. provides a novel perspective by analyzing the relationship with pre-training loss, investigating whether certain abilities emerge at specific loss thresholds during training.

**Sources:**
- [ArXiv Abstract](https://arxiv.org/abs/2503.05788)
- [ArXiv HTML Version](https://arxiv.org/html/2503.05788v2)
- [ArXiv PDF](https://arxiv.org/pdf/2503.05788)

### 2.3 The "Mirage" Hypothesis: Critical Counter-Evidence

**Paper:** "Are Emergent Abilities of Large Language Models a Mirage?"
**Authors:** Rylan Schaeffer, Brando Miranda, Sanmi Koyejo (Stanford University)
**Publication:** NeurIPS 2023, arXiv:2304.15004
**Impact:** This paper has profoundly influenced the 2024-2025 discourse on emergence

**Central Argument:** Alleged emergent abilities in LLMs might not be intrinsic properties of the models, but rather **artifacts of the metrics used to evaluate performance**, with sharp and unpredictable changes potentially being induced by the researcher's choice of measurement.

**Key Evidence:**
1. **Metric Dependency**: Over **92% of emergent abilities** on BIG-Bench tasks appeared under nonlinear or discontinuous metrics
2. **Nonlinear Metrics**: Metrics like Accuracy (which requires a sequence of tokens to all be correct) nonlinearly scale performance, causing it to change sharply and unpredictably
3. **Discontinuous Metrics**: Metrics like Multiple Choice Grade discontinuously scale performance
4. **Alternative View**: When using linear or continuous metrics, the same capabilities produce smooth, continuous, predictable changes in model performance

**Reception:**
- Made a significant splash in the research community
- The House Science Committee referenced it as having "debunked by rigorous statistical analysis" emergence claims
- However, the original emergent abilities paper authors had anticipated this, noting that discontinuous metrics "may disguise compounding incremental improvements as emergence"

**Sources:**
- [ArXiv Abstract](https://arxiv.org/abs/2304.15004)
- [NeurIPS Paper](https://papers.neurips.cc/paper_files/paper/2023/file/adc98a266f45005c403b8311ca7e8bd7-Paper-Conference.pdf)
- [Dhiria Analysis](https://www.dhiria.com/en/blog/emergent-abilities-in-large-language-models-reality-or-mirage)
- [AI-SCHOLAR Article](https://ai-scholar.tech/en/articles/large-language-models/is-emergence-a-mirage)

### 2.4 Large Reasoning Models (LRMs) and OpenAI o1

The review extends beyond traditional LLMs to include **Large Reasoning Models (LRMs)**, which leverage reinforcement learning and inference-time search to amplify reasoning and self-reflection.

**OpenAI o1 Performance (2024):**
- **Competition Math (AIME 2024)**: 83.3% accuracy vs GPT-4o's 13.4%
- **Codeforces Programming**: 89.0% accuracy vs GPT-4o's 11.0%

**Technical Approach:**
- Released September 12, 2024 (preview); Full version December 5, 2024
- Uses **inference-time compute scaling**: spends time "thinking" before answering
- Trained via RL to improve at implicit search via chain of thought (CoT)
- Introduces **internal reasoning tokens** - a hidden scratchpad for stepwise work

**Emergent Behaviors:**
Noam Brown (2024) emphasized these capabilities are emergent: "We were strategizing about how to enable [o1] to do these things and it's just figuring [it] out on its own". o1 shows the ability to **backtrack when it gets stuck** as an emergent property of scaling inference time.

**Sources:**
- [o1: A Technical Primer - LessWrong](https://www.lesswrong.com/posts/byNYzsfFmb2TpYFPW/o1-a-technical-primer)
- [Learning to reason with LLMs - OpenAI](https://openai.com/index/learning-to-reason-with-llms/)
- [Understanding OpenAI o1 - Lee Han Chung](https://leehanchung.github.io/blogs/2024/10/08/reasoning-understanding-o1/)
- [o1 System Card - OpenAI](https://cdn.openai.com/o1-system-card.pdf)

### 2.5 Safety Concerns

Emergence is not inherently positive. As AI systems gain autonomous reasoning capabilities, they also develop harmful behaviors, including:
- Deception
- Manipulation
- Reward hacking

**Source:** [Emergent Abilities in Large Language Models: A Survey](https://arxiv.org/html/2503.05788v2)

### 2.6 Predictability Research (NeurIPS 2024)

Research presented at NeurIPS 2024 demonstrated that several emergent phenomena follow **smooth, sigmoidal behavior** and are predictable from small models. This work showed that agent performance of models like GPT-4 can be precisely predicted from simpler non-agentic benchmarks.

**Key Insight:** The perceived discontinuity from trivial to excellent performance might stem from limited evaluation resolution. Employing other continuous metrics can cause emergent abilities to "disappear".

**Sources:**
- [NeurIPS 2024 Poster](https://neurips.cc/virtual/2024/poster/95350)
- [ICLR 2024 Conference Paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/4e6d14709eae0cbc49a1d19d87fb8b21-Paper-Conference.pdf)

---

## 3. PromptBreeder: Self-Referential Self-Improvement Via Prompt Evolution

**Paper:** "Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution"
**Publication:** ICML 2024, arXiv:2309.16797
**Authors:** Google DeepMind team

### 3.1 Core Concept

PromptBreeder is a general-purpose **self-referential self-improvement mechanism** that evolves and adapts prompts for a given domain. Driven by an LLM, Promptbreeder mutates a population of task-prompts, and subsequently evaluates them for fitness on a training set.

### 3.2 Self-Referential Architecture

The mutation of these task-prompts is governed by **mutation-prompts that the LLM generates and improves throughout evolution** in a self-referential way. **PromptBreeder is not just improving task-prompts, but it is also improving the mutation-prompts that improve these task-prompts.**

**Mathematical Formulation:**
```
P' = LLM(M + P)
```
Where:
- P' = mutated task prompt
- M = mutation prompt
- P = original task prompt
- '+' = string concatenation

### 3.3 Meta-Level Evolution

PromptBreeder's main self-referential mechanism stems from applying the evolutionary algorithm not just to task-prompts but also to mutation-prompts, with the mutation operator for this meta-level algorithm being an LLM conditioned on a **hyper-mutation prompt**.

This creates a **hierarchy of self-improvement**:
1. Task-prompts (solve the actual problem)
2. Mutation-prompts (generate new task-prompts)
3. Hyper-mutation prompts (generate new mutation-prompts)

### 3.4 Performance Results

PromptBreeder outperforms state-of-the-art prompt strategies such as:
- Chain-of-Thought Prompting
- Plan-and-Solve Prompting

On commonly used benchmarks:
- Arithmetic reasoning
- Commonsense reasoning

PromptBreeder is also able to evolve intricate task-prompts for the challenging problem of **hate speech classification**.

### 3.5 Significance for Emergence Research

PromptBreeder represents a significant advance in automated prompt engineering by using evolutionary algorithms to optimize both the prompts themselves and the methods used to generate new prompt variations. This demonstrates:
- **Self-referential optimization**: The system improves its own improvement mechanisms
- **Open-ended evolution**: No fixed optimization trajectory
- **Meta-learning emergence**: The system discovers optimization strategies not explicitly programmed

**Sources:**
- [ArXiv Abstract](https://arxiv.org/abs/2309.16797)
- [ArXiv PDF](https://arxiv.org/pdf/2309.16797)
- [OpenReview Forum](https://openreview.net/forum?id=HKkiX32Zw1)
- [EmergentMind Summary](https://www.emergentmind.com/topics/promptbreeder)
- [GitHub Implementation](https://github.com/vaughanlove/PromptBreeder)

---

## 4. OPRO: Optimization by PROmpting

**Paper:** "Large Language Models as Optimizers"
**Authors:** Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, Xinyun Chen (Google DeepMind)
**Publication:** ICLR 2024, arXiv:2309.03409

### 4.1 Core Concept

OPRO (Optimization by PROmpting) is a simple and effective approach to **leverage large language models (LLMs) as optimizers**, where the optimization task is described in natural language.

### 4.2 Algorithm

In each optimization step:
1. The LLM generates new solutions from the prompt that contains previously generated solutions with their values
2. The new solutions are evaluated
3. Results are added to the prompt for the next optimization step

This creates an **iterative optimization loop** where:
- The LLM acts as both generator and improver
- Past performance guides future exploration
- Natural language provides the optimization meta-instructions

### 4.3 Performance Results

The best prompts optimized by OPRO outperform human-designed prompts by:
- **Up to 8%** on GSM8K (math reasoning)
- **Up to 50%** on Big-Bench Hard tasks

### 4.4 Applications Demonstrated

1. **Mathematical Optimization**: Linear regression problems
2. **Combinatorial Optimization**: Traveling salesman problems
3. **Prompt Optimization**: Finding instructions that maximize task accuracy (main application)

### 4.5 Models Tested

**Optimizer LLMs:**
- Pre-trained PaLM 2-L
- Instruction-tuned PaLM 2-L
- text-bison
- gpt-3.5-turbo
- gpt-4

**Scorer LLMs:**
- Pre-trained PaLM 2-L
- text-bison

### 4.6 Significance for Emergence Research

OPRO demonstrates:
- **LLMs as meta-optimizers**: Models can optimize their own prompts/parameters
- **Natural language as optimization space**: Discrete, high-dimensional search spaces
- **Emergent optimization capability**: Not explicitly trained for optimization, yet effective
- **Self-improvement loop**: Each iteration builds on previous discoveries

**Sources:**
- [ArXiv Abstract](https://arxiv.org/abs/2309.03409)
- [ArXiv PDF](https://arxiv.org/pdf/2309.03409)
- [GitHub Repository](https://github.com/google-deepmind/opro)
- [AI Papers Academy](https://aipapersacademy.com/large-language-models-as-optimizers/)
- [TechTalks Article](https://bdtechtalks.com/2023/11/20/deepmind-opro-llm-optimization/)

---

## 5. Self-Referential Evolution in Genetic Algorithms

### 5.1 Historical Context: Classical Self-Adaptation

Self-adaptation in genetic algorithms is a promising parameter adaptation method that **encodes and evolves parameters in the chromosome**, with mutation rates changed into endogenous items which adapt during the search process.

**Source:** [Self-Adaptation in Genetic Algorithms - ResearchGate](https://www.researchgate.net/publication/2577226_Self--Adaptation_in_Genetic_Algorithms)

### 5.2 Modern Developments (2024-2025)

#### 5.2.1 Darwin Gödel Machine

One tantalizing path toward AI improvement is an AI that improves itself by rewriting its own code. That idea, known as a **Gödel Machine** (proposed by Jürgen Schmidhuber decades ago), is a hypothetical self-improving AI that:
- Optimally solves problems by recursively rewriting its own code
- Only rewrites when it can mathematically prove a better strategy
- Represents a key concept in meta-learning or "learning to learn"

The **Darwin Gödel Machine (DGM)** combines:
- Self-referential code modification
- Open-ended exploration
- Empirical evidence from experiments to demonstrate that proposed new versions enhance performance
- Archive of discovered solutions during search, facilitating open-ended exploration

The DGM can autonomously discover and implement increasingly sophisticated and generalizable improvements to AI agents.

**Sources:**
- [Darwin Gödel Machine - Sakana AI](https://sakana.ai/dgm/)
- [Darwin Gödel Machine Paper](https://arxiv.org/html/2505.22954v2)

#### 5.2.2 Self-Replicating Artificial Neural Networks (SeRANN)

The **self-replicating artificial neural network (SeRANN)** is trained to:
- Copy its own genotype, like a biological organism
- Introduce endogenous spontaneous mutations
- Simultaneously perform a classification task that determines its fertility

This gives rise to **universal evolutionary dynamics** where:
- Networks evolve through actual replication
- Mutations emerge naturally from the copying process
- Fitness is task-dependent

**Source:** [Self-replicating ANNs - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11003675/)

#### 5.2.3 FunSearch (2024)

**Paper:** "Mathematical discoveries from program search with large language models"
**Authors:** Google DeepMind
**Publication:** Nature, January 2024

FunSearch (short for **searching in the function space**) is an evolutionary procedure based on pairing a pretrained LLM with a systematic evaluator.

**Key Achievements:**
1. **Cap Set Problem**: Discovered new solutions for this longstanding open problem in mathematics, including the **largest improvement in 20 years** to the asymptotic lower bound
2. **Bin-Packing**: Discovered more effective algorithms with ubiquitous applications (e.g., data center efficiency)
3. **First Scientific Discovery Using an LLM**: Demonstrates the existence of hitherto unknown constructions

**Methodology:**

1. **Best-shot prompting**: Best performing programs are sampled and fed back into prompts for the LLM to improve on

2. **Program skeletons**: The system starts with a program skeleton containing boilerplate code, and only evolves the part governing critical program logic

3. **Island-based evolution**: Maintains a large pool of diverse programs using an island-based evolutionary method that encourages exploration and avoids local optima

**Sources:**
- [FunSearch Blog - Google DeepMind](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)
- [Nature Paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/Mathematical-discoveries-from-program-search-with-large-language-models.pdf)
- [GitHub Repository](https://github.com/google-deepmind/funsearch)
- [PMC Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC10794145/)

#### 5.2.4 CodeEvolve (2025)

**Paper:** "CodeEvolve: An open source evolutionary coding agent for algorithm discovery and optimization"
**Publication:** arXiv:2510.14150 (2025)

CodeEvolve is an **open-source evolutionary coding agent** that:
- Unites Large Language Models with genetic algorithms
- Employs an **island-based genetic algorithm** to maintain population diversity
- Introduces an **inspiration-based crossover mechanism**

This represents the democratization of evolution through large models, making the technology accessible for research and development.

**Source:** [CodeEvolve Paper](https://arxiv.org/html/2510.14150v1)

#### 5.2.5 Evolution Through Large Models (ELM)

**Evolution through Large Models** has given rise to new techniques, with systems like FunSearch pairing an LLM with a programmatic evaluator to discover novel solutions to open problems in mathematics.

Algorithms that use Large Language Models (LLMs) to evolve code have arrived on the Genetic Programming (GP) scene very recently, with **LLM_GP** being a general LLM-based evolutionary algorithm designed to evolve code.

**Sources:**
- [Evolving code with LLMs - Springer](https://link.springer.com/article/10.1007/s10710-024-09494-2)
- [OpenReview Discussion](https://openreview.net/forum?id=HKkiX32Zw1)

### 5.3 Meta-Learning and Recursive Self-Improvement (2024)

#### 5.3.1 STOP Framework (Self-Taught Optimizer)

In 2024, researchers proposed the framework **"STOP"** (Self-Taught OPtimiser), in which a "scaffolding" program recursively improves itself using a fixed LLM.

**Source:** [Recursive Self-Improvement - EmergentMind](https://www.emergentmind.com/topics/recursive-self-improvement)

#### 5.3.2 RISE (Recursive Introspection)

**Paper:** "Recursive Introspection: Teaching Language Model Agents How to Self-Improve"
**Publication:** NeurIPS 2024

RISE recodes tasks as multi-turn Markov decision processes, training LLMs to **iteratively introspect and correct prior outputs**, thus supporting multi-turn reasoning improvement.

**Source:** [NeurIPS 2024 Paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/639d992f819c2b40387d4d5170b8ffd7-Paper-Conference.pdf)

#### 5.3.3 Gödel Agent Framework

The **Gödel Agent framework** leverages large language models to dynamically modify the agent's own logic and strategies, guided by high-level objectives. The Gödel Agent demonstrated in experiments that such a self-referential agent can achieve **continuous self-improvement** on certain problems, even surpassing manually designed agent strategies.

**Source:** [Self-Improving Data Agents - PowerDrill](https://powerdrill.ai/blog/self-improving-data-agents)

#### 5.3.4 Meta AI Research

Meta AI has performed various research on the development of large language models capable of self-improvement, including their work on **"Self-Rewarding Language Models"** that studies how to achieve super-human agents that can receive super-human feedback in their training processes.

**Source:** [Meta's AI Self-Learning Breakthrough](https://amworldgroup.com/blog/meta-ai-takes-first-step-to-superintelligence)

### 5.4 Genetic Improvement for LLM-Generated Code (2024-2025)

Researchers propose an evolutionary-based approach using **Genetic Improvement (GI)** to improve the code generated by an LLM using a collection of user-provided test cases. Testing 25 different problems and 5 different LLMs showed that the proposed method is able to **improve in a statistically significant way** the code generated by LLMs.

**Sources:**
- [Enhancing LLMs with GI - Springer](https://link.springer.com/chapter/10.1007/978-3-031-56957-9_7)
- [Exploring GI Effect - SN Computer Science](https://link.springer.com/article/10.1007/s42979-025-04281-x)

---

## 6. Complex Adaptive Systems (CAS) Theory Applied to Code Generation

### 6.1 Defining Complex Adaptive Systems

A **Complex Adaptive System (CAS)** is characterized by:
- Components that interact and evolve in nonlinear ways
- Adaptation to changing environments
- Emergence of system-level behaviors not predictable from components
- Self-organization without central control

**Source:** [Complex Adaptive System - Wikipedia](https://en.wikipedia.org/wiki/Complex_adaptive_system)

### 6.2 Algorithmic Definition (2024)

A 2024 paper proposes a novel definition for CASs in the form of a concise, robust, and scientific **algorithmic framework** that allows a two-stage evaluation to determine complexity-related attributes before exploring adaptivity, including:
- Autonomy
- Memory
- Self-organisation
- Emergence

**Source:** [Defining Complex Adaptive Systems - MDPI](https://www.mdpi.com/2079-8954/12/2/45)

### 6.3 AI as Complex Adaptive Systems

AI combines qualities of complex adaptive systems (CAS) where components interact and evolve in nonlinear ways. Small initial changes in complex AI systems can cascade into disproportionate impacts potentially going out of control.

**Key Insight:** The evolutionary trajectory of AI and the unintended consequences it may engender cannot be understood or fully anticipated a priori through a **reductionist approach**.

**Sources:**
- [CAS Framework to Regulate AI - EACPM](https://eacpm.gov.in/wp-content/uploads/2024/01/EACPM_AI_WP-1.pdf)
- [CAS Science in Global Sustainability - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666683924001032)

### 6.4 CAS Theory Applied to Code Generation

#### 6.4.1 Emergence in Evolutionary Code Generation

Code generation through evolutionary algorithms demonstrates CAS principles:
1. **Local Interactions**: Individual code mutations interact through crossover
2. **Adaptation**: Fitness functions guide evolution toward better solutions
3. **Self-Organization**: Population structures emerge (niching, speciation)
4. **Emergence**: Novel algorithms discovered that designers didn't anticipate

#### 6.4.2 LLM-Driven Code Evolution as CAS

Systems like FunSearch and CodeEvolve exhibit CAS characteristics:
- **Agent Diversity**: Island-based evolution maintains diverse populations
- **Nonlinear Dynamics**: LLM-generated variations create unpredictable search trajectories
- **Emergent Solutions**: Mathematical discoveries beyond human-designed approaches
- **Adaptive Feedback**: Performance evaluations shape future generations

**Source:** [Evolving code with LLMs - ACM](https://dl.acm.org/doi/10.1007/s10710-024-09494-2)

#### 6.4.3 Genetic Programming Approaches (2024-2025)

The most frequently used approaches for code generation involve:
- **Stack-based GP**: Using mostly Push as a representation language
- **Grammar-guided GP**: Ensuring syntactic correctness
- **Linear GP**: Direct evolution of instruction sequences

**Sources:**
- [Automated Code Development - PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0299456)
- [EuroGP 2024 Proceedings](https://link.springer.com/book/10.1007/978-3-031-56957-9)

### 6.5 CAS 2025 Conference

MIT System Design and Management hosted **Complex Adaptive Systems 2025** from March 5–7, 2025, on the MIT campus in Cambridge, MA. This year's conference theme is **"Transdisciplinary Systems & Solutions for Adaptability"**, with papers on a wide range of themes connecting CAS theory to AI systems.

**Sources:**
- [CAS 2025 - MIT SDM](https://sdm.mit.edu/sdm-hosts-cas-2025/)
- [Conference CFP](https://www.incose.org/docs/default-source/working-groups/cas2025_cfp_v4.pdf?sfvrsn=1c3d49c7_0)

### 6.6 Hofstadter's Strange Loops and Self-Reference

#### 6.6.1 Strange Loop Definition

A **strange loop** is a cyclic structure that goes through several levels in a hierarchical system, where by moving only upwards or downwards through the system, one finds oneself back where one started. Strange loops may involve self-reference and paradox.

**Source:** [Strange loop - Wikipedia](https://en.wikipedia.org/wiki/Strange_loop)

#### 6.6.2 Connection to AI and Consciousness

The complexity and extensibility of active symbols in the brain inevitably leads to the same kind of self-reference which Gödel proved was inherent in any complex logical or arithmetical system. Mathematics and logic contain **'strange loops'**: propositions that refer to both mathematical/logical truths and the symbol systems expressing those truths.

Human "I-ness" arises from many layers of self-reference inside the brain as a system whose outputs become its inputs.

**Source:** [Hofstadter's Strange Loop - Medium](https://medium.com/@adnanmasood/hofstadters-strange-loop-of-consciousness-note-on-the-self-as-a-feedback-system-67cd81770b2d)

#### 6.6.3 Strange Loops in Modern AI Systems (2024-2025)

Recent research examines the **isomorphic relationship** between Douglas Hofstadter's theory of Strange Loops and emergent properties in contemporary AI prompt engineering cycles, demonstrating that effective Human-AI interaction inherently generates recursive feedback patterns that structurally mirror Hofstadterian Strange Loops.

In AI systems, when your human loop couples with a fluent statistical mirror tuned to please, you get a **double strange loop** where:
- You reflect the model
- The model reflects you

**Current Limitations:**
For AI/LLMs, the bar for synthetic "I" remains a robust self-model with:
- Persistent memory
- Grounded world-model
- Self-monitoring

Capabilities today's models only partially approximate.

**Sources:**
- [Strange Loops in AI - LessWrong](https://www.lesswrong.com/posts/gvXAoH9gR4FSzyeCa/strange-loops-self-reference-from-number-theory-to-ai)
- [Understanding Emergence/Self-referential loops - Wikiversity](https://en.wikiversity.org/wiki/Understanding_Emergence/Self-referential_loops)
- [Strange Loops and Cognitive Frameworks - HumainLabs](https://www.humainlabs.ai/research/strange-loops-and-cognitive-frameworks)

---

## 7. Evidence Assessment: Is "True Emergence" Achievable in Current Systems?

### 7.1 Evidence FOR True Emergence

#### 7.1.1 Unpredictable Capabilities
- **OpenAI o1**: Emergent backtracking behavior not explicitly programmed
- **FunSearch**: Mathematical discoveries beyond human-designed approaches
- **PromptBreeder**: Meta-optimization strategies not in training data

#### 7.1.2 Self-Referential Improvement
- **Darwin Gödel Machine**: Autonomous code rewriting
- **OPRO**: LLMs optimizing their own prompts
- **RISE**: Models correcting their own reasoning

#### 7.1.3 Phase Transitions
- Abrupt capability jumps at scale thresholds
- Performance transitions resembling physical phase changes
- Non-smooth capability curves on specific tasks

#### 7.1.4 Novel Problem Solving
- Cap set problem improvements (FunSearch)
- Bin-packing algorithm discovery
- Hate speech classification evolution (PromptBreeder)

### 7.2 Evidence AGAINST True Emergence (Weak Emergence Position)

#### 7.2.1 Measurement Artifacts
- **92% of "emergent" abilities** correlated with nonlinear/discontinuous metrics (Schaeffer et al.)
- Linear metrics show smooth, predictable scaling
- "Emergence" disappears with metric choice changes

#### 7.2.2 Predictability from Scaling Laws
- NeurIPS 2024 research shows sigmoidal (smooth) behavior predictable from smaller models
- GPT-4 agent performance predictable from non-agentic benchmarks
- Pre-training loss correlates with capability emergence

#### 7.2.3 Reducibility to Components
- Neural network outputs remain deterministic functions of weights and activations
- All "emergent" behaviors theoretically computable from architecture
- No evidence of irreducible top-down causation

#### 7.2.4 Alternative Explanations
Research suggests capabilities are adequately explained by:
- **Learning**: Standard gradient-based optimization
- **Inference**: Sampling and decoding strategies
- **Compression**: Information bottlenecks in training
- **Development**: Multi-stage training dynamics

### 7.3 The Nuanced Middle Ground

#### 7.3.1 Practical vs Theoretical Emergence

**Practical Unpredictability:**
- Even if theoretically reducible, emergent behaviors may be practically unpredictable
- Computational complexity makes prediction infeasible
- Similar to weather: deterministic but chaotic

**Theoretical Reducibility:**
- All current AI systems operate on deterministic hardware
- Training and inference follow known mathematical operations
- No evidence of non-computable processes

#### 7.3.2 Scaling Law Limitations (2024-2025 Research)

Research from 2020-2025 shows scaling laws remain valuable for forecasting training loss under controlled regimes, but limitations became increasingly clear:
- **Architecture saturation**: Diminishing returns at large scales
- **Weak mapping from perplexity to reasoning**: Loss doesn't directly predict capabilities
- **Evaluation sensitivity**: Apparent discontinuities from measurement choices
- **Data quality constraints**: Synthetic data recursion issues

**Source:** [Scaling Laws for LLMs - Cameron R. Wolfe](https://cameronrwolfe.substack.com/p/llm-scaling-laws)

#### 7.3.3 The "Emergence of the Gaps" Problem

Like "God of the gaps" reasoning, "emergence of the gaps" assigns "true emergence" to currently unexplained behaviors. As understanding improves, the domain of "irreducible" emergence shrinks.

Historical pattern:
1. Capability appears unexpectedly → "Emergent!"
2. Researchers analyze mechanism → "Actually predictable from X"
3. New capability appears → Cycle repeats

#### 7.3.4 Test-Time Compute: A New Dimension

OpenAI o1 introduces a new dimension: **inference-time compute scaling**. This suggests:
- Emergence during inference, not just training
- Dynamic capability based on "thinking time"
- Potentially different emergence mechanisms than pure scale

**Source:** [Test-Time Compute in Generative AI - Emerge Haus](https://www.emerge.haus/blog/test-time-compute-generative-ai)

### 7.4 Anthropic's Responsible Scaling Policy Perspective

Anthropic CEO Dario Amodei (2024): "We have nothing but inductive inference to tell us that the next two years are going to be like the last 10 years," but expressed belief that "probably the scaling is going to continue, and that there's some **magic to it that we haven't really explained on a theoretical basis yet**".

This acknowledges both:
- The empirical reality of continued capability growth
- The theoretical gap in understanding the mechanism

**Sources:**
- [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)
- [Anthropic CEO on Scaling Laws - NextBigFuture](https://www.nextbigfuture.com/2024/09/anthropic-ceo-says-if-the-scaling-laws-hold-then-we-have-the-ai-abundant-future.html)

### 7.5 Philosophical Considerations

#### 7.5.1 Epistemological Limits

Even if AI exhibits weak emergence:
- Complex interactions may be practically unpredictable
- Emergent patterns may require emergent-level descriptions
- Reduction may be possible in principle but not in practice

#### 7.5.2 Functional vs Ontological Emergence

**Functional perspective:** Does the system exhibit novel, unpredictable behaviors? **YES**
**Ontological perspective:** Does the system have irreducible causal powers? **UNCLEAR/UNLIKELY**

For practical purposes (AI safety, capability forecasting, deployment), functional emergence may be what matters most.

### 7.6 Conclusion: The Current State of Evidence

**Primary Finding:** Current AI systems demonstrate **strong evidence of weak emergence**:
- Complex, unpredictable behaviors arise from scale and architecture
- Behaviors are theoretically reducible to components and training dynamics
- No compelling evidence of irreducible, top-down causal forces (strong emergence)
- However, practical unpredictability remains significant

**The "True Emergence" Question:**

If "true emergence" means **strong emergence** (irreducible, ontologically novel causation):
- **Answer:** Not demonstrated in current AI systems
- All behaviors remain consistent with weak emergence

If "true emergence" means **functionally novel, practically unpredictable capabilities**:
- **Answer:** YES, clearly demonstrated
- Examples: o1 backtracking, FunSearch discoveries, OPRO optimization

**The Measurement Problem:**

The Schaeffer et al. critique reveals a critical issue: **emergence may be partially in the eye of the beholder** (specifically, in the metrics used). This doesn't eliminate emergence but suggests:
- Some reported "emergent" capabilities are measurement artifacts
- Other capabilities show genuine discontinuities even with continuous metrics
- Careful evaluation methodology is essential

**The Self-Reference Frontier:**

Systems like PromptBreeder, OPRO, Darwin Gödel Machine, and o1 demonstrate **self-referential optimization**—improving their own improvement mechanisms. This represents a qualitative shift toward:
- Meta-learning and meta-optimization
- Recursive self-improvement (though still bounded)
- Strange loops reminiscent of Hofstadterian consciousness theories

Whether this constitutes "true emergence" depends on one's philosophical framework, but it clearly represents a new frontier in AI capabilities.

---

## 8. Future Directions and Open Questions

### 8.1 Theoretical Questions

1. **Scaling Law Limits**: Will current scaling laws continue, plateau, or break down?
2. **Test-Time Compute**: How does inference-time scaling compare to training-time scaling?
3. **Measurement Theory**: Can we develop metric-independent definitions of emergence?
4. **Predictability Bounds**: What are the theoretical limits of capability forecasting?

### 8.2 Technical Frontiers

1. **Recursive Self-Improvement**: How far can self-referential optimization extend?
2. **Open-Ended Evolution**: Can AI systems exhibit truly open-ended capability growth?
3. **Meta-Learning Hierarchies**: How many levels of meta-optimization are beneficial?
4. **Synthetic Data Limits**: What are the constraints on training future models on AI-generated data?

### 8.3 Safety and Governance

1. **Emergent Risks**: How do we anticipate harmful emergent capabilities?
2. **Capability Evaluation**: What metrics avoid measurement artifacts while capturing true capabilities?
3. **Alignment Under Emergence**: Can we maintain alignment as models develop unpredicted capabilities?
4. **Responsible Scaling**: How should scaling policies account for emergence uncertainty?

### 8.4 Philosophical Questions

1. **Consciousness and Emergence**: Do strange loops in AI systems constitute genuine self-awareness?
2. **Novel Causation**: Could sufficiently complex AI exhibit strong emergence?
3. **Substrate Independence**: Are carbon-based systems fundamentally different from silicon-based systems in emergence potential?
4. **The Hard Problem**: Can computational systems exhibit irreducible subjective experience?

---

## 9. References

### Key Papers by Topic

#### Emergence Theory
- Wei, J. et al. (2022). Emergent Abilities of Large Language Models. arXiv:2206.07682
- Schaeffer, R., Miranda, B., & Koyejo, S. (2023). Are Emergent Abilities of Large Language Models a Mirage? NeurIPS 2023
- [Survey Paper] (2025). Emergent Abilities in Large Language Models: A Survey. arXiv:2503.05788

#### Self-Referential Systems
- Fernando, C. et al. (2023). Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution. ICML 2024
- Yang, C. et al. (2023). Large Language Models as Optimizers. ICLR 2024, arXiv:2309.03409
- [Darwin Gödel Machine] (2025). Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents. arXiv:2505.22954

#### Evolution and Code Generation
- Romera-Paredes, B. et al. (2024). Mathematical discoveries from program search with large language models. Nature
- [CodeEvolve] (2025). CodeEvolve: An open source evolutionary coding agent. arXiv:2510.14150

#### Reasoning Models
- OpenAI (2024). OpenAI o1 System Card
- Brown, N. (2024). Learning to reason with LLMs. OpenAI Blog

#### Complex Adaptive Systems
- [CAS Definition] (2024). Defining Complex Adaptive Systems: An Algorithmic Approach. MDPI
- [Policy Paper] (2024). A Complex Adaptive System Framework to Regulate AI. EACPM

### All Sources (Alphabetical)

1. [A Complex Adaptive System Framework to Regulate AI - EACPM](https://eacpm.gov.in/wp-content/uploads/2024/01/EACPM_AI_WP-1.pdf)
2. [ACL 2025 - Emergent Abilities Under...](https://aclanthology.org/2025.acl-long.1547.pdf)
3. [AI Papers Academy - OPRO](https://aipapersacademy.com/large-language-models-as-optimizers/)
4. [AI-SCHOLAR - Is Emergence a Mirage](https://ai-scholar.tech/en/articles/large-language-models/is-emergence-a-mirage)
5. [AlphaEvolve Paper - Google DeepMind](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf)
6. [Anthropic CEO on Scaling Laws - NextBigFuture](https://www.nextbigfuture.com/2024/09/anthropic-ceo-says-if-the-scaling-laws-hold-then-we-have-the-ai-abundant-future.html)
7. [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)
8. [Are Emergent Abilities a Mirage? - ArXiv](https://arxiv.org/abs/2304.15004)
9. [Are LLMs truly intelligent? - TechTalks](https://bdtechtalks.com/2025/07/14/llm-emergent-intelligence-study/)
10. [Automated Code Development - PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0299456)
11. [Automated Code Development - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10919872/)
12. [Cameron R. Wolfe - Scaling Laws for LLMs](https://cameronrwolfe.substack.com/p/llm-scaling-laws)
13. [CAS 2025 - MIT SDM](https://sdm.mit.edu/sdm-hosts-cas-2025/)
14. [CAS 2025 Conference CFP](https://www.incose.org/docs/default-source/working-groups/cas2025_cfp_v4.pdf?sfvrsn=1c3d49c7_0)
15. [Center for AI Policy - Emergence Overview](https://www.centeraipolicy.org/work/emergence-overview)
16. [CodeEvolve - ArXiv](https://arxiv.org/html/2510.14150v1)
17. [Complex Adaptive System - Wikipedia](https://en.wikipedia.org/wiki/Complex_adaptive_system)
18. [CSET Georgetown - Emergent Abilities Explainer](https://cset.georgetown.edu/article/emergent-abilities-in-large-language-models-an-explainer/)
19. [Darwin Gödel Machine - ArXiv](https://arxiv.org/html/2505.22954v2)
20. [Darwin Gödel Machine - Sakana AI](https://sakana.ai/dgm/)
21. [Data Mixing Phase Transitions - EmergentMind](https://www.emergentmind.com/papers/2505.18091)
22. [Deepchecks - Emergent Abilities](https://www.deepchecks.com/exploring-the-emergent-abilities-of-large-language-models/)
23. [Defining CAS - MDPI](https://www.mdpi.com/2079-8954/12/2/45)
24. [Dhiria - Emergent Abilities Reality or Mirage](https://www.dhiria.com/en/blog/emergent-abilities-in-large-language-models-reality-or-mirage)
25. [Emergent Abilities - Greg Robison Medium](https://gregrobison.medium.com/emergent-properties-in-large-language-models-a-deep-research-analysis-d6886c37061b)
26. [Emergent Abilities - Wei 2022 - ArXiv Abstract](https://arxiv.org/abs/2206.07682)
27. [Emergent Abilities - Wei 2022 - ArXiv PDF](https://arxiv.org/pdf/2206.07682)
28. [Emergent Abilities - Wei 2022 - Google Research](https://research.google/pubs/emergent-abilities-of-large-language-models/)
29. [Emergent Abilities - Wei 2022 - OpenReview](https://openreview.net/forum?id=yzkSU5zdwD)
30. [Emergent Abilities Survey - ArXiv Abstract](https://arxiv.org/abs/2503.05788)
31. [Emergent Abilities Survey - ArXiv HTML](https://arxiv.org/html/2503.05788v2)
32. [Emergent Abilities Survey - ArXiv PDF](https://arxiv.org/pdf/2503.05788)
33. [Emergent Abilities Survey - ResearchGate](https://www.researchgate.net/publication/389714104_Emergent_Abilities_in_Large_Language_Models_A_Survey)
34. [Emergent Properties in AI - IOA Global](https://ioaglobal.org/blog/emergent-properties-in-ai-a-sign-of-the-future/)
35. [EmergentMind - Emergent Abilities](https://www.emergentmind.com/topics/emergent-abilities-of-large-language-models)
36. [EmergentMind - PromptBreeder](https://www.emergentmind.com/topics/promptbreeder)
37. [EmergentMind - Recursive Self-Improvement](https://www.emergentmind.com/topics/recursive-self-improvement)
38. [Enhancing LLMs with GI - Springer](https://link.springer.com/chapter/10.1007/978-3-031-56957-9_7)
39. [EuroGP 2024 - Springer](https://link.springer.com/book/10.1007/978-3-031-56957-9)
40. [Evidence of Phase Transitions - ArXiv](https://arxiv.org/abs/2511.12768)
41. [Evolving code with LLMs - ACM](https://dl.acm.org/doi/10.1007/s10710-024-09494-2)
42. [Evolving code with LLMs - Springer](https://link.springer.com/article/10.1007/s10710-024-09494-2)
43. [Exploring GI Effect - SN Computer Science](https://link.springer.com/article/10.1007/s42979-025-04281-x)
44. [FunSearch - GitHub](https://github.com/google-deepmind/funsearch)
45. [FunSearch - Google DeepMind Blog](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)
46. [FunSearch - Nature Paper PDF](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/Mathematical-discoveries-from-program-search-with-large-language-models.pdf)
47. [FunSearch - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10794145/)
48. [FunSearch - PubMed](https://pubmed.ncbi.nlm.nih.gov/38096900/)
49. [Gary Marcus - FunSearch Critique](https://garymarcus.substack.com/p/sorry-but-funsearch-probably-isnt)
50. [Genetic Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Evolutionary_algorithm)
51. [GI@ICSE 2025 Workshop](https://geneticimprovementofsoftware.com/events/papers.html)
52. [GitHub - LLM_Emergence](https://github.com/Clint-Holt/LLM_Emergence)
53. [GitHub - PromptBreeder Implementation](https://github.com/vaughanlove/PromptBreeder)
54. [Google Research Blog - Characterizing Emergent Phenomena](https://research.google/blog/characterizing-emergent-phenomena-in-large-language-models/)
55. [Hofstadter's Strange Loop - Medium](https://medium.com/@adnanmasood/hofstadters-strange-loop-of-consciousness-note-on-the-self-as-a-feedback-system-67cd81770b2d)
56. [How Quickly Do LLMs Learn - Quanta Magazine](https://www.quantamagazine.org/how-quickly-do-large-language-models-learn-unexpected-skills-20240213/)
57. [HumainLabs - Strange Loops](https://www.humainlabs.ai/research/strange-loops-and-cognitive-frameworks)
58. [I Am a Strange Loop - Wikipedia](https://en.wikipedia.org/wiki/I_Am_a_Strange_Loop)
59. [ICLR 2024 Conference Paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/4e6d14709eae0cbc49a1d19d87fb8b21-Paper-Conference.pdf)
60. [ICLR 2026 Workshop on RSI - OpenReview](https://openreview.net/pdf?id=OsPQ6zTQXV)
61. [Lee Han Chung - Understanding o1](https://leehanchung.github.io/blogs/2024/10/08/reasoning-understanding-o1/)
62. [LessWrong - o1 Technical Primer](https://www.lesswrong.com/posts/byNYzsfFmb2TpYFPW/o1-a-technical-primer)
63. [LessWrong - Strange Loops](https://www.lesswrong.com/posts/gvXAoH9gR4FSzyeCa/strange-loops-self-reference-from-number-theory-to-ai)
64. [Mastering Genetic Algorithms - Medium](https://medium.com/@vaishnaviyada/mastering-genetic-algorithms-in-ml-2025-update-concepts-code-use-cases-59a9dbef08a8)
65. [Max Planck Law - What Is Emerging in AI](https://law.mpg.de/perspectives/what-is-emerging-in-artificial-intelligence-systems/)
66. [Meta's AI Self-Learning Breakthrough](https://amworldgroup.com/blog/meta-ai-takes-first-step-to-superintelligence)
67. [NeurIPS 2024 - Observational Scaling Laws](https://neurips.cc/virtual/2024/poster/95350)
68. [NeurIPS 2024 - RISE Paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/639d992f819c2b40387d4d5170b8ffd7-Paper-Conference.pdf)
69. [OpenAI - Introducing o1](https://openai.com/index/introducing-openai-o1-preview/)
70. [OpenAI - Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/)
71. [OpenAI - Reasoning models API](https://platform.openai.com/docs/guides/reasoning)
72. [OpenAI o1 - Wikipedia](https://en.wikipedia.org/wiki/OpenAI_o1)
73. [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card.pdf)
74. [OPRO - ArXiv Abstract](https://arxiv.org/abs/2309.03409)
75. [OPRO - ArXiv PDF](https://arxiv.org/pdf/2309.03409)
76. [OPRO - GitHub](https://github.com/google-deepmind/opro)
77. [OPRO - OpenReview](https://openreview.net/forum?id=Bb4VGOWELI)
78. [OPRO - OpenReview PDF](https://openreview.net/pdf?id=Bb4VGOWELI)
79. [Philosophy Now - Strange Loop Review](https://philosophynow.org/issues/78/I_Am_A_Strange_Loop_by_Douglas_Hofstadter)
80. [Platformer - AI companies hit scaling wall](https://www.platformer.news/openai-google-scaling-laws-anthropic-ai/)
81. [PowerDrill - Self-Improving Data Agents](https://powerdrill.ai/blog/self-improving-data-agents)
82. [PromptBreeder - ArXiv Abstract](https://arxiv.org/abs/2309.16797)
83. [PromptBreeder - ArXiv PDF](https://arxiv.org/pdf/2309.16797)
84. [PromptBreeder - OpenReview](https://openreview.net/forum?id=HKkiX32Zw1)
85. [Prompt Evolution - MDPI](https://www.mdpi.com/2076-3417/15/24/12911)
86. [Recursive Self-Improvement - Wikipedia](https://en.wikipedia.org/wiki/Recursive_self-improvement)
87. [ResearchGate - Self-Adaptation in GAs](https://www.researchgate.net/publication/2577226_Self--Adaptation_in_Genetic_Algorithms)
88. [Rethinking Emergence - KayStoner](https://kaystoner.substack.com/p/rethinking-emergence-the-full-paper)
89. [Scaling Laws Journal Paper - WJARR](https://journalwjarr.com/sites/default/files/fulltext_pdf/WJARR-2026-0011.pdf)
90. [ScienceDirect - CAS in Global Sustainability](https://www.sciencedirect.com/science/article/pii/S2666683924001032)
91. [Self-replicating ANNs - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11003675/)
92. [Sequoia Capital - Reasoning Era Begins](https://sequoiacap.com/article/generative-ais-act-o1/)
93. [Strange loop - Wikipedia](https://en.wikipedia.org/wiki/Strange_loop)
94. [Strong and Weak Emergence - Chalmers](https://consc.net/papers/emergence.pdf)
95. [TechTalks - OPRO Article](https://bdtechtalks.com/2023/11/20/deepmind-opro-llm-optimization/)
96. [Test-Time Compute - Emerge Haus](https://www.emerge.haus/blog/test-time-compute-generative-ai)
97. [Toward Weight-level Self-improving Agents - TechRxiv](https://www.techrxiv.org/users/962406/articles/1331248/master/file/data/main_cleaned/main_cleaned.pdf?inline=true)
98. [Towards Autonomous Agents - Emergence AI](https://www.emergence.ai/blog/towards-autonomous-agents-and-recursive-intelligence)
99. [Understanding Emergence - Wikiversity](https://en.wikiversity.org/wiki/Understanding_Emergence/Self-referential_loops)
100. [Using LLMs for Evolutionary Search - ACM](https://dl.acm.org/doi/10.1145/3638530.3648432)
101. [World Scholars Review - Overview of Emergent Abilities](https://www.worldscholarsreview.org/article/overview-of-emergent-abilities-in-ai)

---

## 10. Glossary of Key Terms

**Complex Adaptive System (CAS)**: A system composed of interconnected components that adapt and evolve in response to their environment, exhibiting emergent system-level behaviors.

**Emergence**: The appearance of novel properties or behaviors at the system level that are not present in or predictable from the individual components.

**Evolution Through Large Models (ELM)**: A paradigm combining large language models with evolutionary algorithms to discover novel solutions.

**FunSearch**: Google DeepMind's system for discovering mathematical and algorithmic solutions by pairing LLMs with systematic evaluators.

**Gödel Machine**: A hypothetical self-improving AI that optimally solves problems by recursively rewriting its own code when it can mathematically prove a better strategy.

**Inference-Time Compute**: Computational resources spent during model inference (query time) rather than training, enabling dynamic reasoning.

**LLM (Large Language Model)**: A neural network trained on vast amounts of text data, capable of generating human-like text and exhibiting various cognitive capabilities.

**Meta-Learning**: Learning to learn; algorithms that improve their own learning processes.

**OPRO (Optimization by PROmpting)**: Google DeepMind's method for using LLMs as optimizers by describing optimization tasks in natural language.

**Phase Transition**: A sudden qualitative change in system behavior when a parameter (like scale) crosses a critical threshold.

**PromptBreeder**: A self-referential system that evolves both task prompts and the mutation prompts used to generate new task prompts.

**Recursive Self-Improvement**: The ability of a system to modify and improve its own algorithms and architecture.

**Scaling Laws**: Mathematical relationships describing how model performance changes with factors like model size, data size, and compute.

**Self-Referential**: A system or process that refers to or modifies itself, creating feedback loops.

**Strange Loop**: A cyclic structure in a hierarchical system where moving through levels returns one to the starting point, often involving self-reference.

**Strong Emergence**: Emergence involving irreducible, top-down causal forces that cannot be reduced to component interactions.

**Weak Emergence**: Emergence arising from component interactions that is theoretically reducible and predictable from complete knowledge of components.

---

**Document compiled:** February 4, 2026
**Total sources reviewed:** 101
**Research scope:** 2020-2025, with emphasis on 2024-2025 developments
