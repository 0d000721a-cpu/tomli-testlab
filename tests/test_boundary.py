"""边界值分析测试 — 数值/日期/字符串在边界处的行为。

边界值公式：区间 [a, b] 测 a-1, a, a+1, b-1, b, b+1。
对于 TOML 解析器，边界值存在于数字范围、日期范围、字符串长度等处。
"""

from datetime import date, datetime, time
from sys import maxsize

import pytest


class TestIntegerBoundaries:
    """整数边界值"""

    def test_int_min(self, loads):
        """边界：最小整数"""
        result = loads(f"n = {-maxsize - 1}")
        assert result["n"] == -maxsize - 1

    def test_int_max(self, loads):
        """边界：最大整数"""
        result = loads(f"n = {maxsize}")
        assert result["n"] == maxsize

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
        assert result["n"] == 0.0  # -0.0 == 0.0 在 Python 中

    def test_float_smallest_positive(self, loads):
        """边界：最小正浮点数"""
        result = loads("n = 5e-324")
        assert result["n"] > 0

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

    def test_string_newline_in_basic(self, loads):
        """边界：普通字符串不能包含换行符（应报错）"""
        import tomli
        with pytest.raises(tomli.TOMLDecodeError):
            loads('x = "line1\nline2"')


class TestTableBoundaries:
    """表格边界值"""

    def test_table_array_empty(self, loads):
        """边界：空表数组"""
        result = loads("")  # 没有 [[items]]
        assert result == {}

    def test_single_table_array(self, loads):
        """边界：只有一个元素的表数组"""
        result = loads('[[item]]\nname = "only"')
        assert len(result["item"]) == 1

    def test_table_name_max_nesting(self, loads):
        """边界：深嵌套"""
        result = loads("[a]\n[b]\n[c]\n[d]\nval = 1")
        assert result["d"]["val"] == 1


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
