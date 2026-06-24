"""边界值分析测试 — 数值/日期/字符串边界。

Modification Record (2026-06-24):
  - Reviewed: Boundary values for int (64-bit min/max/0/±1),
    float (0.0/-0.0/subnormal/max), date (epoch/leap/future),
    time (midnight/end-of-day), string (empty/single/whitespace),
    array (single/large), table (single/deeply nested)
  - Status: No source changes needed
  - Skill source: test-case-generator
"""

import math
from datetime import date, datetime, time

import pytest

# TOML v1.0 整数范围: 64-bit signed
TOML_MIN_INT = -(2**63)
TOML_MAX_INT = 2**63 - 1


class TestIntegerBoundaries:
    """整数边界值"""

    def test_int_min(self, loads):
        """边界：TOML 64-bit 最小值"""
        result = loads(f"n = {TOML_MIN_INT}")
        assert result["n"] == TOML_MIN_INT

    def test_int_max(self, loads):
        """边界：TOML 64-bit 最大值"""
        result = loads(f"n = {TOML_MAX_INT}")
        assert result["n"] == TOML_MAX_INT

    def test_int_zero(self, loads):
        """边界值：0"""
        result = loads("n = 0")
        assert result["n"] == 0

    def test_int_negative_one(self, loads):
        """边界值：-1"""
        result = loads("n = -1")
        assert result["n"] == -1

    def test_int_positive_one(self, loads):
        """边界值：1"""
        result = loads("n = 1")
        assert result["n"] == 1

    def test_underscore_boundary(self, loads):
        """带下划线的整数"""
        result = loads("n = 1_000_000")
        assert result["n"] == 1_000_000


class TestFloatBoundaries:
    """浮点数边界值"""

    def test_float_zero(self, loads):
        result = loads("n = 0.0")
        assert result["n"] == 0.0

    def test_float_negative_zero(self, loads):
        result = loads("n = -0.0")
        assert result["n"] == 0.0
        # 验证负零的符号被正确保留了
        assert math.copysign(1, result["n"]) == -1

    def test_float_smallest_positive(self, loads):
        """边界：最小正浮点数"""
        result = loads("n = 5e-324")
        assert result["n"] == 5e-324

    def test_float_largest(self, loads):
        """边界：最大浮点数"""
        result = loads("n = 1.7976931348623157e+308")
        assert float("inf") > result["n"] > 0

    def test_float_trailing_zero(self, loads):
        """边界：末尾有0"""
        result = loads("n = 1.0")
        assert result["n"] == 1.0


class TestDateBoundaries:
    """日期边界值"""

    def test_date_epoch(self, loads):
        """边界：Unix epoch"""
        result = loads("d = 1970-01-01")
        assert result["d"] == date(1970, 1, 1)

    def test_date_before_epoch(self, loads):
        """边界：epoch 之前"""
        result = loads("d = 1969-12-31")
        assert result["d"] == date(1969, 12, 31)

    def test_date_leap_year(self, loads):
        """边界：闰年 2 月 29 日"""
        result = loads("d = 2024-02-29")
        assert result["d"] == date(2024, 2, 29)

    def test_date_new_year(self, loads):
        """边界：元旦"""
        result = loads("d = 2025-01-01")
        assert result["d"] == date(2025, 1, 1)

    def test_date_far_future(self, loads):
        """边界：远未来"""
        result = loads("d = 9999-12-31")
        assert result["d"] == date(9999, 12, 31)

    def test_time_midnight(self, loads):
        """边界：午夜"""
        result = loads("t = 00:00:00")
        assert result["t"] == time(0, 0)

    def test_time_end_of_day(self, loads):
        """边界：一天结束"""
        result = loads("t = 23:59:59")
        assert result["t"] == time(23, 59, 59)


class TestStringBoundaries:
    """字符串边界值"""

    def test_string_single_char(self, loads):
        """边界：单字符"""
        result = loads('x = "a"')
        assert result["x"] == "a"

    def test_string_empty(self, loads):
        """边界：空字符串"""
        result = loads('x = ""')
        assert result["x"] == ""

    def test_string_whitespace_only(self, loads):
        """边界：仅空格"""
        result = loads('x = "   "')
        assert result["x"] == "   "

    def test_string_newline_in_basic(self, loads, TOMLDecodeError):
        """边界：普通字符串不能包含换行符（应报错）"""
        with pytest.raises(TOMLDecodeError):
            loads('x = "line1\nline2"')


class TestTableBoundaries:
    """表格边界值"""

    def test_single_table_array(self, loads):
        """边界：只有一个元素的表数组"""
        result = loads('[[item]]\nname = "only"')
        assert len(result["item"]) == 1

    def test_deeply_nested_tables(self, loads):
        """边界：多级嵌套表"""
        result = loads("[a.b.c.d]\nval = 1")
        assert result["a"]["b"]["c"]["d"]["val"] == 1


class TestArrayBoundaries:
    """数组边界值"""

    def test_array_single_element(self, loads):
        """边界：单元素数组"""
        result = loads("x = [1]")
        assert result["x"] == [1]

    def test_array_hundred_elements(self, loads):
        """边界：大数组"""
        elements = ", ".join(str(i) for i in range(100))
        result = loads(f"x = [{elements}]")
        assert len(result["x"]) == 100
        assert result["x"][0] == 0
        assert result["x"][-1] == 99
