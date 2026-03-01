# funNLP-Search - 中文NLP资源检索助手

## 描述

基于 funNLP (79.1k stars) 项目的资源检索助手，提供快速搜索和访问 60+ 类别的中文 NLP 资源。

## 功能

- 自然语言搜索 NLP 资源
- 分类浏览（LLM、词库、预训练模型、知识图谱等）
- 资源详情展示（描述、链接、Stars）
- 支持关键词匹配和模糊搜索

## 使用方法

### 搜索资源
```bash
python scripts/search.py "中文分词"
python scripts/search.py "知识图谱" --limit 5
```

### 列出分类
```bash
python scripts/search.py --list-categories
```

### 浏览特定分类
```bash
python scripts/search.py --category "LLM/ChatGPT"
```

## 数据源

- funNLP README.md (60+ 类别资源汇总)
- 定期更新同步上游项目

## 依赖

- Python 3.8+
- requests
- beautifulsoup4
- pyyaml

## 配置

参考 `config/default.yaml` 和 `references/.env.example`
