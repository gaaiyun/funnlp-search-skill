#!/usr/bin/env python3
"""
funNLP-Search - 中文NLP资源检索助手
基于 funNLP 项目的资源搜索工具
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional

# 资源数据库（从 funNLP README.md 提取）
RESOURCES = {
    "LLM/ChatGPT": [
        {
            "name": "LLM Survey",
            "desc": "大语言模型综述论文",
            "url": "https://github.com/RUCAIBox/LLMSurvey",
            "stars": "9.5k"
        },
        {
            "name": "Awesome-LLM",
            "desc": "LLM 资源汇总",
            "url": "https://github.com/Hannibal046/Awesome-LLM",
            "stars": "17k"
        }
    ],
    "中文分词": [
        {
            "name": "jieba",
            "desc": "结巴中文分词",
            "url": "https://github.com/fxsjy/jieba",
            "stars": "33k"
        },
        {
            "name": "pkuseg",
            "desc": "北大中文分词工具",
            "url": "https://github.com/lancopku/pkuseg-python",
            "stars": "6.5k"
        }
    ],
    "知识图谱": [
        {
            "name": "OpenKG",
            "desc": "中文开放知识图谱",
            "url": "http://openkg.cn",
            "stars": "N/A"
        },
        {
            "name": "Agriculture_KnowledgeGraph",
            "desc": "农业知识图谱",
            "url": "https://github.com/qq547276542/Agriculture_KnowledgeGraph",
            "stars": "3.5k"
        }
    ],
    "预训练模型": [
        {
            "name": "BERT",
            "desc": "Google BERT 预训练模型",
            "url": "https://github.com/google-research/bert",
            "stars": "38k"
        },
        {
            "name": "Chinese-BERT-wwm",
            "desc": "中文 BERT-wwm 预训练模型",
            "url": "https://github.com/ymcui/Chinese-BERT-wwm",
            "stars": "9k"
        }
    ],
    "情感分析": [
        {
            "name": "SnowNLP",
            "desc": "中文情感分析库",
            "url": "https://github.com/isnowfy/snownlp",
            "stars": "6.5k"
        }
    ],
    "词库": [
        {
            "name": "funNLP 词库",
            "desc": "30万词典、停用词、人名库、公司名等",
            "url": "https://github.com/fighting41love/funNLP/tree/master/data",
            "stars": "79k"
        }
    ]
}

CATEGORIES = list(RESOURCES.keys())


def search_resources(query: str, limit: int = 10) -> List[Dict]:
    """搜索资源"""
    results = []
    query_lower = query.lower()
    
    for category, items in RESOURCES.items():
        for item in items:
            # 关键词匹配
            if (query_lower in category.lower() or 
                query_lower in item["name"].lower() or 
                query_lower in item["desc"].lower()):
                results.append({
                    "category": category,
                    **item
                })
    
    return results[:limit]


def list_categories() -> List[str]:
    """列出所有分类"""
    return CATEGORIES


def get_category_resources(category: str) -> List[Dict]:
    """获取特定分类的资源"""
    return RESOURCES.get(category, [])


def format_result(result: Dict) -> str:
    """格式化输出结果"""
    return f"""
[{result['category']}] {result['name']} ({result['stars']} stars)
  {result['desc']}
  {result['url']}
"""


def main():
    parser = argparse.ArgumentParser(description="funNLP 资源检索助手")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=10, help="返回结果数量")
    parser.add_argument("--list-categories", action="store_true", help="列出所有分类")
    parser.add_argument("--category", help="浏览特定分类")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    args = parser.parse_args()
    
    # 列出分类
    if args.list_categories:
        print("Available categories:")
        for i, cat in enumerate(list_categories(), 1):
            print(f"  {i}. {cat}")
        return
    
    # 浏览分类
    if args.category:
        resources = get_category_resources(args.category)
        if not resources:
            print(f"Category not found: {args.category}")
            return
        
        if args.json:
            print(json.dumps(resources, ensure_ascii=False, indent=2))
        else:
            print(f"\n=== {args.category} ===\n")
            for res in resources:
                print(format_result({"category": args.category, **res}))
        return
    
    # 搜索
    if not args.query:
        parser.print_help()
        return
    
    results = search_resources(args.query, args.limit)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print(f"No results found for: {args.query}")
        else:
            print(f"\nFound {len(results)} results for '{args.query}':\n")
            for res in results:
                print(format_result(res))


if __name__ == "__main__":
    main()
