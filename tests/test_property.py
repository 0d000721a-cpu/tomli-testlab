"""基于属性的测试 — 用 hypothesis 生成随机 TOML 输入。

传统测试写有限个例子，属性测试描述不变量，
让计算机生成无数随机输入来验证这些不变量是否被违反。
"""

import pytest
import tomli
from hypothesis import given, strategies as st, settings, assume


# ── 策略定义 ──

# 安全的裸键名（不含特殊字符，且自动保证唯一性）
# 用 indexing (i0, i1, i2...) 避免重复键的问题
index_key = st.integers(min_value=0, max_value=9999).map(lambda i: f"k{i}")

# 安全的字符串值（不含换行、双引号）
safe_str = st.text(
    alphabet=st.characters(
        whitelist_categories=("Ll", "Lu", "Nd", "P", "Z"),
        max_codepoint=127,
    ),
    max_size=50,
).filter(
    lambda s: '"' not in s
    and "'" not in s
    and "\n" not in s
    and "\\" not in s
)

# 整数（TOML v1.0 用 64 位有符号）
toml_int = st.integers(min_value=-(2**63), max_value=2**63 - 1)

# 浮点数（不要 inf/nan，因为 TOML 特殊值不适合常规策略）
toml_float = st.floats(
    min_value=-1e308,
    max_value=1e308,
    allow_infinity=False,
    allow_nan=False,
    allow_subnormal=False,
)


@given(st.lists(st.tuples(index_key, toml_int), min_size=0, max_size=10, unique_by=lambda kv: kv[0]))
@settings(max_examples=100)
def test_parse_simple_kv_pairs(key_values):
    """不变量：key=integer 的 TOML 总是解析为 dict[str, int]。"""
    lines = [f'{k} = {v}' for k, v in key_values]
    toml_str = "\n".join(lines)
    result = tomli.loads(toml_str)

    assert isinstance(result, dict)
    for k, v in key_values:
        assert k in result
        assert isinstance(result[k], int)
        assert result[k] == v


@given(st.lists(st.tuples(index_key, safe_str), min_size=0, max_size=10, unique_by=lambda kv: kv[0]))
@settings(max_examples=100)
def test_parse_simple_strings(key_values):
    """不变量：key=string 的 TOML 解析为 dict[str, str]。"""
    lines = [f'{k} = "{v}"' for k, v in key_values]
    toml_str = "\n".join(lines)
    result = tomli.loads(toml_str)

    assert isinstance(result, dict)
    for k, v in key_values:
        assert result[k] == v


@given(st.lists(st.tuples(index_key, toml_float), min_size=0, max_size=10, unique_by=lambda kv: kv[0]))
@settings(max_examples=100)
def test_parse_float_returns_float(key_values):
    """不变量：float 值解析后类型是 float。"""
    lines = [f'{k} = {v}' for k, v in key_values]
    toml_str = "\n".join(lines)
    result = tomli.loads(toml_str)

    assert isinstance(result, dict)
    for k, v in key_values:
        assert isinstance(result[k], float)
        assert result[k] == pytest.approx(v, rel=1e-10)


@given(st.lists(toml_int, min_size=0, max_size=8))
@settings(max_examples=50)
def test_array_of_ints(elements):
    """不变量：int 数组的解析结果。"""
    array_str = "[" + ", ".join(str(v) for v in elements) + "]"
    toml_str = f"arr = {array_str}"
    result = tomli.loads(toml_str)

    assert isinstance(result["arr"], list)
    assert all(isinstance(x, int) for x in result["arr"])
    assert result["arr"] == list(elements)


@given(st.text(min_size=0, max_size=100))
@settings(max_examples=200)
def test_arbitrary_text_never_crashes(raw_text):
    """不变量：任何字符串输入都不会导致非 TOMLDecodeError 的崩溃。"""
    try:
        result = tomli.loads(raw_text)
        assert isinstance(result, dict)
    except tomli.TOMLDecodeError:
        pass  # 解析器拒绝无效 TOML 是正常行为
    except Exception as e:
        raise AssertionError(f"非预期的异常: {type(e).__name__}: {e}")
