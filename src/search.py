"""funNLP 资源检索（v2）。

v1 在 scripts/search.py 里把硬编码 RESOURCES + search 函数 + CLI 全部
塞在一个文件里，没法单测、没法库调用。v2 拆出：

- src/search.py: 检索逻辑（输入 query / category，输出结果）
- 资源数据从 v1 的 6 类扩展到 12+ 类（覆盖原 funNLP README 主要类目）
- 支持 fuzzy match（按词组拆分计算 token overlap），不局限于 substring
- 支持按 stars 排序
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


@dataclass
class Resource:
    name: str
    desc: str
    url: str
    stars: str = "N/A"
    category: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name, "desc": self.desc, "url": self.url,
            "stars": self.stars, "category": self.category,
        }


# --- 数据库（扩展自 v1 的 6 类 → 12 类）---------------------------

RESOURCES: Dict[str, List[Dict[str, str]]] = {
    "LLM/ChatGPT": [
        {"name": "LLM Survey", "desc": "大语言模型综述论文",
         "url": "https://github.com/RUCAIBox/LLMSurvey", "stars": "9.5k"},
        {"name": "Awesome-LLM", "desc": "LLM 资源汇总",
         "url": "https://github.com/Hannibal046/Awesome-LLM", "stars": "17k"},
        {"name": "Chinese-LLaMA-Alpaca",
         "desc": "中文 LLaMA & Alpaca 预训练 + 指令精调",
         "url": "https://github.com/ymcui/Chinese-LLaMA-Alpaca",
         "stars": "18k"},
    ],
    "中文分词": [
        {"name": "jieba", "desc": "结巴中文分词",
         "url": "https://github.com/fxsjy/jieba", "stars": "33k"},
        {"name": "pkuseg", "desc": "北大中文分词工具",
         "url": "https://github.com/lancopku/pkuseg-python", "stars": "6.5k"},
        {"name": "HanLP", "desc": "面向生产环境的多语言 NLP",
         "url": "https://github.com/hankcs/HanLP", "stars": "33k"},
    ],
    "知识图谱": [
        {"name": "OpenKG", "desc": "中文开放知识图谱",
         "url": "http://openkg.cn", "stars": "N/A"},
        {"name": "Agriculture_KnowledgeGraph", "desc": "农业知识图谱",
         "url": "https://github.com/qq547276542/Agriculture_KnowledgeGraph",
         "stars": "3.5k"},
        {"name": "OwnThink", "desc": "中文知识图谱（含 1.4 亿三元组）",
         "url": "https://github.com/ownthink/KnowledgeGraphData", "stars": "5k"},
    ],
    "预训练模型": [
        {"name": "BERT", "desc": "Google BERT 预训练模型",
         "url": "https://github.com/google-research/bert", "stars": "38k"},
        {"name": "Chinese-BERT-wwm", "desc": "中文 BERT-wwm 预训练模型",
         "url": "https://github.com/ymcui/Chinese-BERT-wwm", "stars": "9k"},
        {"name": "ERNIE", "desc": "百度持续学习语义理解框架",
         "url": "https://github.com/PaddlePaddle/ERNIE", "stars": "6k"},
    ],
    "情感分析": [
        {"name": "SnowNLP", "desc": "中文情感分析库",
         "url": "https://github.com/isnowfy/snownlp", "stars": "6.5k"},
        {"name": "FinBERT", "desc": "金融领域 BERT 情感模型",
         "url": "https://github.com/ProsusAI/finBERT", "stars": "1.8k"},
        {"name": "VADER", "desc": "英文社交媒体情感分析（基于词典）",
         "url": "https://github.com/cjhutto/vaderSentiment", "stars": "4.5k"},
    ],
    "词库": [
        {"name": "funNLP 词库", "desc": "30 万词典、停用词、人名库、公司名等",
         "url": "https://github.com/fighting41love/funNLP/tree/master/data",
         "stars": "79k"},
        {"name": "Synonyms", "desc": "中文近义词工具包",
         "url": "https://github.com/chatopera/Synonyms", "stars": "5k"},
    ],
    "命名实体识别": [
        {"name": "BERT-NER", "desc": "Pytorch BERT-NER",
         "url": "https://github.com/kamalkraj/BERT-NER", "stars": "1.2k"},
        {"name": "LTP", "desc": "哈工大 LTP 语言技术平台",
         "url": "https://github.com/HIT-SCIR/ltp", "stars": "5k"},
    ],
    "文本分类": [
        {"name": "TextCNN", "desc": "CNN 文本分类",
         "url": "https://github.com/dennybritz/cnn-text-classification-tf",
         "stars": "5.5k"},
        {"name": "FastText", "desc": "Facebook 文本分类 + 词向量",
         "url": "https://github.com/facebookresearch/fastText",
         "stars": "26k"},
    ],
    "机器翻译": [
        {"name": "OpenNMT", "desc": "开源神经机器翻译框架",
         "url": "https://github.com/OpenNMT/OpenNMT-py", "stars": "6.5k"},
        {"name": "fairseq", "desc": "Facebook seq2seq 工具包",
         "url": "https://github.com/facebookresearch/fairseq", "stars": "30k"},
    ],
    "问答系统": [
        {"name": "DuReader", "desc": "百度中文阅读理解数据集",
         "url": "https://github.com/baidu/DuReader", "stars": "1.5k"},
        {"name": "Haystack", "desc": "端到端 QA / RAG 框架",
         "url": "https://github.com/deepset-ai/haystack", "stars": "15k"},
    ],
    "文本摘要": [
        {"name": "PageRank-textrank", "desc": "TextRank 文本摘要",
         "url": "https://github.com/letiantian/TextRank4ZH", "stars": "3k"},
        {"name": "Sumy", "desc": "多算法文本摘要库",
         "url": "https://github.com/miso-belica/sumy", "stars": "3.5k"},
    ],
    "数据集": [
        {"name": "CLUE", "desc": "中文语言理解测评基准",
         "url": "https://github.com/CLUEbenchmark/CLUE", "stars": "4k"},
        {"name": "datasets (HuggingFace)", "desc": "通用 NLP 数据集",
         "url": "https://github.com/huggingface/datasets", "stars": "19k"},
    ],
}


# --- 搜索 ---------------------------------------------------------

def _parse_stars(s: str) -> float:
    """把 '17k' / '3.5k' / 'N/A' 转成浮点（用于排序）。"""
    if not s or s.lower() in ("n/a", "na", ""):
        return 0.0
    s = s.strip().lower().replace(",", "")
    multiplier = 1.0
    if s.endswith("k"):
        multiplier = 1e3
        s = s[:-1]
    elif s.endswith("m"):
        multiplier = 1e6
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return 0.0


def _resource_objects() -> List[Resource]:
    out = []
    for cat, items in RESOURCES.items():
        for it in items:
            out.append(Resource(
                name=it["name"], desc=it["desc"], url=it["url"],
                stars=it.get("stars", "N/A"), category=cat,
            ))
    return out


def list_categories() -> List[str]:
    return list(RESOURCES.keys())


def get_category_resources(category: str) -> List[Resource]:
    return [r for r in _resource_objects() if r.category == category]


def _matches(resource: Resource, query: str, mode: str) -> float:
    """匹配评分。返回 0 = 不匹配，>0 = 匹配（越大越好）。"""
    q = query.lower().strip()
    if not q:
        return 0.0
    fields = [resource.name.lower(), resource.desc.lower(),
              resource.category.lower()]

    # exact substring：所有字段中找 substring
    sub_hits = sum(1 for f in fields if q in f)

    if mode == "substring":
        return float(sub_hits)

    # fuzzy: split query 成 tokens，看每个 token 在每个 field 出现次数
    q_tokens = [t for t in q.replace("-", " ").split() if t]
    if not q_tokens:
        return float(sub_hits)
    token_hits = 0
    for t in q_tokens:
        for f in fields:
            if t in f:
                token_hits += 1
                break
    score = sub_hits + token_hits * 0.5
    # name 命中加分
    if any(t in resource.name.lower() for t in q_tokens):
        score += 0.5
    return float(score)


def search_resources(query: str, limit: int = 10,
                      mode: str = "fuzzy",
                      sort_by: str = "relevance") -> List[Resource]:
    """搜索资源。

    Parameters
    ----------
    query : 搜索词（支持空格分多 token）
    limit : 返回数量
    mode : "substring" 严格子串 / "fuzzy" 多 token 匹配
    sort_by : "relevance"（默认）/ "stars"（按 stars 数）
    """
    if mode not in ("substring", "fuzzy"):
        raise ValueError(f"mode 必须 substring / fuzzy，得到 {mode}")
    if sort_by not in ("relevance", "stars"):
        raise ValueError(f"sort_by 必须 relevance / stars，得到 {sort_by}")
    if limit <= 0:
        raise ValueError("limit 必须 > 0")

    all_resources = _resource_objects()
    scored = [(r, _matches(r, query, mode)) for r in all_resources]
    matched = [(r, s) for r, s in scored if s > 0]

    if sort_by == "relevance":
        # 主键 relevance，次键 stars
        matched.sort(key=lambda rs: (-rs[1], -_parse_stars(rs[0].stars)))
    else:
        matched.sort(key=lambda rs: (-_parse_stars(rs[0].stars), -rs[1]))

    return [r for r, _ in matched[:limit]]


def top_starred(limit: int = 10) -> List[Resource]:
    """直接按 stars 排序的 top N，不需要 query。"""
    return sorted(_resource_objects(),
                  key=lambda r: -_parse_stars(r.stars))[:limit]
