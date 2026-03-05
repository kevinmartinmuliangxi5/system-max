import json, os, re, math
from collections import Counter, defaultdict
from functools import lru_cache

# 极简版海马体 v2.2：TF-IDF + BM25 + 查询扩展 + 自适应阈值
FILE = ".janus/long_term_memory.json"

# 中英文停用词
CHINESE_STOPWORDS = {
    '的', '了', '是', '在', '和', '与', '或', '等', '及', '也', '都', '就',
    '而', '又', '还', '但', '却', '只', '才', '能', '会', '要', '可以', '这',
    '那', '这个', '那个', '什么', '怎么', '为什么', '哪里', '哪个', '多少',
    '一个', '一些', '一种', '有的', '没有', '不是', '不能', '不会', '不要',
    '可能', '应该', '必须', '需要', '已经', '正在', '将要', '如果', '因为',
    '所以', '但是', '然而', '虽然', '尽管', '无论', '不管', '只要', '只有'
}

ENGLISH_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
}

# 中英文同义词映射（查询扩展）
SYNONYM_MAP = {
    # ===== 认证登录相关 =====
    # 中文 → 英文
    '登录': ['login', 'signin', 'authentication', 'auth', 'sign-in'],
    '认证': ['authentication', 'auth', 'login', 'signin', 'verify'],
    '授权': ['authorization', 'permission', 'access', 'grant', 'privilege'],
    '鉴权': ['authentication', 'verification', 'validate', 'authorize'],
    '注册': ['register', 'signup', 'sign-up', 'registration'],

    # 英文 → 中文
    'login': ['登录', '登入', '认证'],
    'authentication': ['认证', '验证', '鉴权', '登录'],
    'authorization': ['授权', '权限'],
    'signin': ['登录', '登入'],
    'register': ['注册', '注册'],
    'signup': ['注册', '登记'],

    # ===== 性能优化相关 =====
    # 中文 → 英文
    '性能': ['performance', 'efficiency', 'speed', 'throughput'],
    '优化': ['optimize', 'improve', 'enhance', 'boost', 'tune'],
    '加速': ['accelerate', 'speed up', 'faster', 'boost'],
    '缓存': ['cache', 'caching', 'buffer'],
    '索引': ['index', 'indexing'],

    # 英文 → 中文
    'performance': ['性能', '表现', '效率'],
    'optimize': ['优化', '改进', '提升'],
    'efficiency': ['效率', '性能'],
    'cache': ['缓存', '缓冲'],
    'index': ['索引'],

    # ===== 开发实现相关 =====
    # 中文 → 英文
    '实现': ['implement', 'develop', 'create', 'build', 'code'],
    '开发': ['develop', 'development', 'build', 'implement'],
    '创建': ['create', 'build', 'make', 'generate'],
    '设计': ['design', 'architect', 'plan'],
    '构建': ['build', 'construct', 'create'],

    # 英文 → 中文
    'implement': ['实现', '实施', '开发'],
    'develop': ['开发', '开发', '实现'],
    'create': ['创建', '建立', '制作'],
    'design': ['设计', '规划'],
    'build': ['构建', '建立', '创建'],

    # ===== 修复调试相关 =====
    # 中文 → 英文
    '修复': ['fix', 'repair', 'solve', 'debug', 'resolve', 'patch'],
    '调试': ['debug', 'debugging', 'troubleshoot'],
    '错误': ['error', 'bug', 'issue', 'problem', 'fault'],
    '异常': ['exception', 'error', 'abnormal'],
    '崩溃': ['crash', 'failure', 'breakdown'],

    # 英文 → 中文
    'fix': ['修复', '修正', '解决'],
    'bug': ['错误', '缺陷', '故障', 'bug'],
    'debug': ['调试', '排查', '调试'],
    'error': ['错误', '异常', '错误'],
    'issue': ['问题', '议题', '错误'],
    'crash': ['崩溃', '崩溃', '故障'],

    # ===== 测试验证相关 =====
    # 中文 → 英文
    '测试': ['test', 'testing', 'unit test', 'integration test', 'verify'],
    '验证': ['verify', 'validation', 'check', 'validate'],
    '检查': ['check', 'inspect', 'verify', 'validate'],
    '单元测试': ['unit test', 'unittest'],
    '集成测试': ['integration test', 'e2e test'],

    # 英文 → 中文
    'test': ['测试', '检测', '验证'],
    'verify': ['验证', '核实', '检查'],
    'validate': ['验证', '校验'],
    'check': ['检查', '核对', '验证'],

    # ===== 数据库相关 =====
    # 中文 → 英文
    '数据库': ['database', 'db', 'datastore'],
    '查询': ['query', 'search', 'find', 'select'],
    '表': ['table', 'relation'],
    '字段': ['field', 'column', 'attribute'],
    '记录': ['record', 'row', 'entry'],

    # 英文 → 中文
    'database': ['数据库', '数据库'],
    'query': ['查询', '检索', '查找'],
    'table': ['表', '数据表'],
    'field': ['字段', '列'],
    'column': ['列', '字段'],

    # ===== 用户相关 =====
    # 中文 → 英文
    '用户': ['user', 'account', 'member'],
    '账户': ['account', 'user account'],
    '权限': ['permission', 'privilege', 'access'],
    '角色': ['role', 'user role'],

    # 英文 → 中文
    'user': ['用户', '使用者'],
    'account': ['账户', '账号'],
    'permission': ['权限', '许可'],
    'role': ['角色', '身份'],

    # ===== 功能特性相关 =====
    # 中文 → 英文
    '功能': ['feature', 'function', 'capability', 'functionality'],
    '特性': ['feature', 'characteristic', 'property'],
    '模块': ['module', 'component', 'unit'],
    '组件': ['component', 'module', 'widget'],

    # 英文 → 中文
    'feature': ['功能', '特性', '特征'],
    'function': ['功能', '函数', '作用'],
    'module': ['模块', '单元'],
    'component': ['组件', '部件', '模块'],
}


class Hippocampus:
    def __init__(self):
        # jieba 初始化
        try:
            import jieba
            jieba.setLogLevel(jieba.logging.INFO)
            self.jieba = jieba
            self.use_jieba = True
        except ImportError:
            self.jieba = None
            self.use_jieba = False

        # 加载记忆
        self.mem = json.load(open(FILE, 'r', encoding='utf-8')) if os.path.exists(FILE) else []

        # 倒排索引和统计
        self.inverted_index = defaultdict(set)
        self.doc_freq = Counter()
        self.tokenized_cache = {}
        self.doc_length = {}  # 文档长度（用于 BM25）

        # 查询缓存
        self._retrieve_cached = lru_cache(maxsize=50)(self._retrieve_impl)

        # BM25 参数
        self.k1 = 1.5  # 词频饱和参数
        self.b = 0.75  # 长度归一化参数

        self._build_index()
        self._calculate_avg_doc_length()

    def _calculate_avg_doc_length(self):
        """计算平均文档长度（用于 BM25）"""
        if self.doc_length:
            self.avg_doc_length = sum(self.doc_length.values()) / len(self.doc_length)
        else:
            self.avg_doc_length = 0

    def _build_index(self):
        """构建倒排索引"""
        for idx, m in enumerate(self.mem):
            text = m['p'] + " " + m['s']
            words = self._tokenize(text)

            self.tokenized_cache[idx] = words
            self.doc_length[idx] = len(words)

            unique_words = set(words)
            for word in unique_words:
                self.inverted_index[word].add(idx)
                self.doc_freq[word] += 1

    def _tokenize(self, text):
        """智能分词"""
        if not text:
            return []

        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', text))

        if has_chinese and self.use_jieba:
            words = list(self.jieba.cut(text.lower()))
            words = [w.strip() for w in words
                     if len(w.strip()) > 1 and w.strip() not in CHINESE_STOPWORDS]
        else:
            words = re.findall(r'\w+', text.lower())
            words = [w for w in words if w not in ENGLISH_STOPWORDS]

        return words

    def _expand_query(self, words):
        """查询扩展：添加同义词"""
        expanded = set(words)

        for word in words:
            if word in SYNONYM_MAP:
                expanded.update(SYNONYM_MAP[word])

        return list(expanded)

    def _text_to_vector(self, text):
        """文本转词频向量"""
        words = self._tokenize(text)
        if not words:
            return None
        return Counter(words)

    def _calculate_tfidf(self, term_freq, doc_count):
        """计算 TF-IDF"""
        tfidf = {}
        total_docs = len(self.mem)

        for term, tf in term_freq.items():
            df = self.doc_freq.get(term, 0)
            if df > 0:
                idf = math.log((total_docs + 1) / (df + 1)) + 1
                tfidf[term] = tf * idf
            else:
                tfidf[term] = tf

        return tfidf

    def _calculate_bm25(self, q_words, doc_idx):
        """计算 BM25 分数"""
        if doc_idx not in self.tokenized_cache:
            return 0

        doc_words = self.tokenized_cache[doc_idx]
        doc_length = self.doc_length.get(doc_idx, 1)

        score = 0
        doc_tf = Counter(doc_words)

        for word in q_words:
            if word not in doc_tf:
                continue

            tf = doc_tf[word]
            df = self.doc_freq.get(word, 0)

            if df == 0:
                continue

            # IDF 部分
            idf = math.log((len(self.mem) - df + 0.5) / (df + 0.5) + 1)

            # TF 部分（带长度归一化）
            length_norm = 1 - self.b + self.b * (doc_length / self.avg_doc_length)
            tf_component = (tf * (self.k1 + 1)) / (tf + self.k1 * length_norm)

            score += idf * tf_component

        return score

    def _cosine_similarity(self, vec1, vec2):
        """余弦相似度"""
        if not vec1 or not vec2:
            return 0

        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0

        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        return numerator / denominator if denominator else 0

    def store(self, p, s):
        """存储记忆"""
        idx = len(self.mem)
        self.mem.append({"p": p, "s": s})

        text = p + " " + s
        words = self._tokenize(text)
        self.tokenized_cache[idx] = words
        self.doc_length[idx] = len(words)

        unique_words = set(words)
        for word in unique_words:
            self.inverted_index[word].add(idx)
            self.doc_freq[word] += 1

        # 保留最近 100 条
        if len(self.mem) > 100:
            removed_idx = 0
            removed_words = self.tokenized_cache.get(removed_idx, [])

            for word in set(removed_words):
                self.doc_freq[word] -= 1
                if self.doc_freq[word] <= 0:
                    del self.doc_freq[word]

            if removed_idx in self.tokenized_cache:
                del self.tokenized_cache[removed_idx]
            if removed_idx in self.doc_length:
                del self.doc_length[removed_idx]

            self.mem = self.mem[-100:]

            # 重建索引
            self.inverted_index.clear()
            self.doc_freq.clear()
            old_cache = self.tokenized_cache
            old_length = self.doc_length
            self.tokenized_cache = {}
            self.doc_length = {}

            for new_idx, m in enumerate(self.mem):
                old_idx = new_idx + 1
                if old_idx in old_cache:
                    words = old_cache[old_idx]
                    length = old_length.get(old_idx, len(words))
                else:
                    words = self._tokenize(m['p'] + " " + m['s'])
                    length = len(words)

                self.tokenized_cache[new_idx] = words
                self.doc_length[new_idx] = length

                unique_words = set(words)
                for word in unique_words:
                    self.inverted_index[word].add(new_idx)
                    self.doc_freq[word] += 1

        # 重新计算平均长度
        self._calculate_avg_doc_length()

        # 清除查询缓存
        self._retrieve_cached.cache_clear()

        with open(FILE, 'w', encoding='utf-8') as f:
            json.dump(self.mem, f, indent=2, ensure_ascii=False)

    def retrieve(self, q):
        """检索接口"""
        return self._retrieve_cached(q)

    def _retrieve_impl(self, q):
        """混合检索：BM25 + TF-IDF"""
        if not self.mem:
            return []

        # 分词
        q_words = self._tokenize(q)
        if not q_words:
            return []

        # 查询扩展（添加同义词）
        expanded_words = self._expand_query(q_words)

        # 使用倒排索引找候选
        candidate_indices = set()
        for word in expanded_words:
            if word in self.inverted_index:
                candidate_indices.update(self.inverted_index[word])

        if not candidate_indices:
            return []

        # 计算 TF-IDF（用于余弦相似度）
        q_tf = Counter(q_words)
        q_tfidf = self._calculate_tfidf(q_tf, 1)

        # 对候选计算分数
        results = []
        for idx in candidate_indices:
            m = self.mem[idx]

            # BM25 分数
            bm25_score = self._calculate_bm25(expanded_words, idx)

            # TF-IDF 余弦相似度
            if idx in self.tokenized_cache:
                m_words = self.tokenized_cache[idx]
                m_tf = Counter(m_words)
            else:
                m_tf = self._text_to_vector(m['p'] + " " + m['s'])

            m_tfidf = self._calculate_tfidf(m_tf, 1)
            tfidf_score = self._cosine_similarity(q_tfidf, m_tfidf)

            # 混合分数：BM25 (70%) + TF-IDF (30%)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score

            # 自适应阈值：基于查询长度
            threshold = 0.01 if len(q_words) <= 2 else 0.03

            if combined_score > threshold:
                results.append((combined_score, m))

        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results[:2]]

    def clear_cache(self):
        """清除缓存"""
        self._retrieve_cached.cache_clear()

    def get_stats(self):
        """统计信息"""
        return {
            'memory_count': len(self.mem),
            'index_size': len(self.inverted_index),
            'unique_words': len(self.doc_freq),
            'cache_size': len(self.tokenized_cache),
            'use_jieba': self.use_jieba,
            'avg_doc_length': self.avg_doc_length,
            'cache_info': self._retrieve_cached.cache_info()._asdict()
        }
