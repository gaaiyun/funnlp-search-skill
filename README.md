# funNLP-Search

中文 NLP 资源检索助手，基于 funNLP (79.1k stars) 项目。

## 功能

- 自然语言搜索 NLP 资源
- 多类别资源汇总
- 显示项目 Stars 和描述
- 直接访问 GitHub 链接

## 快速开始

### 搜索资源
```bash
python scripts/search.py "中文分词"
python scripts/search.py "知识图谱" --limit 5
```

### 列出分类
```bash
python scripts/search.py --list-categories
```

### 浏览分类
```bash
python scripts/search.py --category "LLM/ChatGPT"
```

### JSON 输出
```bash
python scripts/search.py "BERT" --json
```

## 资源分类

- LLM/ChatGPT
- 中文分词
- 知识图谱
- 预训练模型
- 情感分析
- 词库

## 依赖

```bash
pip install requests beautifulsoup4 pyyaml
```

## 数据源

基于 [funNLP](https://github.com/fighting41love/funNLP) 项目整理。

## License

Apache 2.0
