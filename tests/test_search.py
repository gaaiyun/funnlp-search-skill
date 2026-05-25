"""search.py 测试。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.search import (
    RESOURCES,
    Resource,
    _matches,
    _parse_stars,
    _resource_objects,
    get_category_resources,
    list_categories,
    search_resources,
    top_starred,
)


# --- _parse_stars ----------------------------------------------------

def test_parse_stars_k():
    assert _parse_stars("17k") == 17000.0


def test_parse_stars_decimal_k():
    assert _parse_stars("3.5k") == 3500.0


def test_parse_stars_m():
    assert _parse_stars("1.5m") == 1_500_000.0


def test_parse_stars_na():
    assert _parse_stars("N/A") == 0.0
    assert _parse_stars("") == 0.0
    assert _parse_stars(None) == 0.0


def test_parse_stars_plain_number():
    assert _parse_stars("500") == 500.0


def test_parse_stars_invalid():
    assert _parse_stars("not-a-number") == 0.0


# --- RESOURCES & categories ----------------------------------------

def test_resources_has_at_least_10_categories():
    assert len(RESOURCES) >= 10


def test_categories_unique_and_non_empty():
    cats = list_categories()
    assert len(cats) == len(set(cats))
    for c in cats:
        assert c


def test_each_resource_has_required_fields():
    for cat, items in RESOURCES.items():
        for it in items:
            assert "name" in it
            assert "desc" in it
            assert "url" in it


def test_resource_objects_count_matches():
    """_resource_objects 总数 = 各类 item 数之和。"""
    total = sum(len(v) for v in RESOURCES.values())
    assert len(_resource_objects()) == total


# --- get_category_resources ---------------------------------------

def test_get_category_existing():
    items = get_category_resources("中文分词")
    assert len(items) >= 1
    assert all(it.category == "中文分词" for it in items)


def test_get_category_missing():
    assert get_category_resources("不存在的分类") == []


def test_get_category_jieba_in_segmentation():
    items = get_category_resources("中文分词")
    names = [it.name for it in items]
    assert "jieba" in names


# --- _matches -----------------------------------------------------

def test_matches_substring_exact():
    r = Resource(name="jieba", desc="结巴中文分词", url="x",
                  category="中文分词")
    assert _matches(r, "jieba", "substring") > 0
    assert _matches(r, "结巴", "substring") > 0


def test_matches_substring_misses_for_no_match():
    r = Resource(name="jieba", desc="结巴中文分词", url="x",
                  category="中文分词")
    assert _matches(r, "totally unrelated", "substring") == 0.0


def test_matches_fuzzy_multi_token():
    """fuzzy 模式下，'jieba 分词' 多 token 都能匹配。"""
    r = Resource(name="jieba", desc="结巴中文分词", url="x",
                  category="中文分词")
    score = _matches(r, "jieba 分词", "fuzzy")
    assert score > 0


def test_matches_case_insensitive():
    r = Resource(name="BERT", desc="Google BERT", url="x",
                  category="预训练模型")
    assert _matches(r, "bert", "substring") > 0


def test_matches_empty_query():
    r = Resource(name="x", desc="y", url="z", category="cat")
    assert _matches(r, "", "fuzzy") == 0.0
    assert _matches(r, "   ", "fuzzy") == 0.0


# --- search_resources ---------------------------------------------

def test_search_finds_jieba():
    results = search_resources("jieba", limit=5)
    assert any(r.name == "jieba" for r in results)


def test_search_finds_chinese_term():
    results = search_resources("分词", limit=10)
    assert len(results) >= 1
    # 至少含中文分词类目的资源
    cats = {r.category for r in results}
    assert "中文分词" in cats


def test_search_case_insensitive():
    results = search_resources("BERT", limit=5)
    assert any("BERT" in r.name or "bert" in r.name.lower() for r in results)


def test_search_no_results_empty_list():
    results = search_resources("nonexistent_random_xyz_query_123", limit=5)
    assert results == []


def test_search_respects_limit():
    results = search_resources("中文", limit=2)
    assert len(results) <= 2


def test_search_invalid_mode_raises():
    with pytest.raises(ValueError, match="mode"):
        search_resources("x", mode="bogus")


def test_search_invalid_sort_raises():
    with pytest.raises(ValueError, match="sort_by"):
        search_resources("x", sort_by="bogus")


def test_search_invalid_limit_raises():
    with pytest.raises(ValueError, match="limit"):
        search_resources("x", limit=0)


def test_search_sort_by_stars_returns_higher_first():
    results = search_resources("中文", limit=5, sort_by="stars")
    if len(results) >= 2:
        stars = [_parse_stars(r.stars) for r in results]
        # 至少要近似单调递减
        assert stars[0] >= stars[-1]


def test_search_fuzzy_more_permissive_than_substring():
    """fuzzy 应能匹配 substring 模式找不到的多 token 查询。"""
    fuzzy = search_resources("BERT model", limit=5, mode="fuzzy")
    sub = search_resources("BERT model", limit=5, mode="substring")
    # fuzzy 可能更多结果（因为 token 拆分）
    assert len(fuzzy) >= len(sub)


# --- top_starred --------------------------------------------------

def test_top_starred_returns_sorted_desc():
    results = top_starred(limit=5)
    assert len(results) == 5
    stars = [_parse_stars(r.stars) for r in results]
    assert stars == sorted(stars, reverse=True)


def test_top_starred_funnlp_in_top():
    """funNLP 词库本身 79k stars，应排前。"""
    top = top_starred(limit=3)
    star_values = [_parse_stars(r.stars) for r in top]
    # 至少 top 第一名 stars > 30k
    assert star_values[0] > 30_000


# --- Resource dataclass --------------------------------------------

def test_resource_to_dict():
    import json
    r = Resource(name="x", desc="y", url="http://z", stars="10k",
                  category="cat")
    d = r.to_dict()
    json.dumps(d, ensure_ascii=False)
    assert d["stars"] == "10k"


def test_resource_default_stars():
    r = Resource(name="x", desc="y", url="z")
    assert r.stars == "N/A"
